from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


# --- Category Schemas ---
class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int
    image_url: Optional[str] = None
    cloudinary_public_id: Optional[str] = None
    stock: int = 0
    is_active: bool = True
    is_featured: bool = False
    sizes: Optional[str] = None
    colors: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    cloudinary_public_id: Optional[str] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    sizes: Optional[str] = None
    colors: Optional[str] = None


class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional[CategoryOut] = None

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    total: int
    products: List[ProductOut]


# --- Auth Schemas ---
class AdminCreate(BaseModel):
    username: str
    email: str
    password: str


class AdminLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class AdminOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True
