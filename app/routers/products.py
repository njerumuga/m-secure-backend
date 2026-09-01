from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional, List
import cloudinary
import cloudinary.uploader
from app.core.database import get_db
from app.core.config import settings
from app.models.models import Product, Category
from app.schemas import schemas  # Updated path
from app.routers.auth import get_current_admin

router = APIRouter()

# Configure Cloudinary
if settings.CLOUDINARY_CLOUD_NAME:
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
    )


@router.get("/", response_model=schemas.ProductListResponse)
def get_products(
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,  # Matches ?category=slug from Navbar
        category_id: Optional[int] = None,
        is_featured: Optional[bool] = None,
        search: Optional[str] = None,
        db: Session = Depends(get_db),
):
    query = db.query(Product).join(Category).filter(Product.is_active == True)

    # Filter by Category Slug (from Navbar)
    if category:
        query = query.filter(Category.slug == category)

    # Filter by Numeric ID (from Admin)
    if category_id:
        query = query.filter(Product.category_id == category_id)

    if is_featured is not None:
        query = query.filter(Product.is_featured == is_featured)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    total = query.count()
    products = query.offset(skip).limit(limit).all()

    return {"total": total, "products": products}


@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=schemas.ProductOut)
def create_product(
        product: schemas.ProductCreate,
        db: Session = Depends(get_db),
        current_admin=Depends(get_current_admin),
):
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(
        product_id: int,
        product_update: schemas.ProductUpdate,
        db: Session = Depends(get_db),
        current_admin=Depends(get_current_admin),
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{product_id}")
def delete_product(
        product_id: int,
        db: Session = Depends(get_db),
        current_admin=Depends(get_current_admin),
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if db_product.cloudinary_public_id and settings.CLOUDINARY_CLOUD_NAME:
        cloudinary.uploader.destroy(db_product.cloudinary_public_id)

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}


@router.post("/{product_id}/upload-image")
async def upload_product_image(
        product_id: int,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_admin=Depends(get_current_admin),
):
    if not settings.CLOUDINARY_CLOUD_NAME:
        raise HTTPException(status_code=400, detail="Cloudinary not configured")

    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if db_product.cloudinary_public_id:
        cloudinary.uploader.destroy(db_product.cloudinary_public_id)

    contents = await file.read()
    result = cloudinary.uploader.upload(
        contents,
        folder="msecure_products",
        transformation=[{"width": 800, "height": 800, "crop": "fill", "quality": "auto"}],
    )

    db_product.image_url = result["secure_url"]
    db_product.cloudinary_public_id = result["public_id"]
    db.commit()

    return {"image_url": result["secure_url"], "public_id": result["public_id"]}