"""
Run this once to seed the database with default categories and sample products.
Usage: python seed.py
"""
from app.core.database import SessionLocal, engine, Base
from app.models.models import Category, Product, Admin
from app.core.security import get_password_hash

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Seed Categories
categories_data = [
    {"name": "T-Shirts", "slug": "t-shirts", "description": "Custom printed T-shirts for all occasions", "icon": "👕"},
    {"name": "Hoodies", "slug": "hoodies", "description": "Premium branded hoodies", "icon": "🧥"},
    {"name": "Caps", "slug": "caps", "description": "Stylish branded caps and hats", "icon": "🧢"},
    {"name": "Reflectors", "slug": "reflectors", "description": "Safety reflector vests and gear", "icon": "🦺"},
    {"name": "Aprons", "slug": "aprons", "description": "Custom printed and embroidered aprons", "icon": "👔"},
    {"name": "Overalls", "slug": "overalls", "description": "Custom branded overalls and workwear", "icon": "👷"},
]

for cat_data in categories_data:
    existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
    if not existing:
        db.add(Category(**cat_data))

db.commit()

# Get category IDs
tshirts = db.query(Category).filter(Category.slug == "t-shirts").first()
hoodies = db.query(Category).filter(Category.slug == "hoodies").first()
caps = db.query(Category).filter(Category.slug == "caps").first()
reflectors = db.query(Category).filter(Category.slug == "reflectors").first()

# Seed Sample Products
products_data = [
    {
        "name": "Classic Crew Neck T-Shirt",
        "description": "High-quality 100% cotton crew neck tee. Perfect for corporate branding and events. Available in bulk orders.",
        "price": 450,
        "category_id": tshirts.id,
        "stock": 100,
        "is_featured": True,
        "sizes": "S,M,L,XL,XXL",
        "colors": "White,Black,Navy,Green,Red",
        "image_url": "https://placehold.co/800x800/22C55E/ffffff?text=T-Shirt",
    },
    {
        "name": "Polo T-Shirt (Embroidered)",
        "description": "Premium polo shirt with embroidered logo. Professional look for corporate uniforms.",
        "price": 750,
        "category_id": tshirts.id,
        "stock": 80,
        "is_featured": True,
        "sizes": "S,M,L,XL,XXL",
        "colors": "White,Black,Navy,Green",
        "image_url": "https://placehold.co/800x800/22C55E/ffffff?text=Polo",
    },
    {
        "name": "Premium Pullover Hoodie",
        "description": "Heavyweight fleece hoodie with full front print. Great for teams and events.",
        "price": 1800,
        "category_id": hoodies.id,
        "stock": 50,
        "is_featured": True,
        "sizes": "S,M,L,XL,XXL",
        "colors": "Black,Grey,Navy,Green",
        "image_url": "https://placehold.co/800x800/EAB308/ffffff?text=Hoodie",
    },
    {
        "name": "Zip-Up Hoodie",
        "description": "Full zip fleece hoodie with embroidered or printed branding.",
        "price": 2200,
        "category_id": hoodies.id,
        "stock": 30,
        "sizes": "S,M,L,XL,XXL",
        "colors": "Black,Grey,Navy",
        "image_url": "https://placehold.co/800x800/EAB308/ffffff?text=Zip+Hoodie",
    },
    {
        "name": "Trucker Cap",
        "description": "Classic 5-panel trucker cap with custom embroidery or print patch.",
        "price": 600,
        "category_id": caps.id,
        "stock": 120,
        "is_featured": True,
        "sizes": "One Size",
        "colors": "Black,Navy,White,Green,Red",
        "image_url": "https://placehold.co/800x800/22C55E/ffffff?text=Cap",
    },
    {
        "name": "Dad Cap (Low Profile)",
        "description": "Soft unstructured low-profile cap with custom embroidery.",
        "price": 550,
        "category_id": caps.id,
        "stock": 90,
        "sizes": "One Size",
        "colors": "Black,Beige,Navy,Olive",
        "image_url": "https://placehold.co/800x800/22C55E/ffffff?text=Dad+Cap",
    },
    {
        "name": "Hi-Vis Reflector Vest",
        "description": "ANSI/ISEA compliant high visibility safety vest with custom branding. Essential for construction and logistics teams.",
        "price": 850,
        "category_id": reflectors.id,
        "stock": 200,
        "is_featured": True,
        "sizes": "S,M,L,XL,XXL",
        "colors": "Yellow,Orange",
        "image_url": "https://placehold.co/800x800/EAB308/ffffff?text=Reflector",
    },
    {
        "name": "Reflector Jacket",
        "description": "Full safety jacket with reflective strips and custom company branding.",
        "price": 2500,
        "category_id": reflectors.id,
        "stock": 40,
        "sizes": "M,L,XL,XXL",
        "colors": "Yellow,Orange",
        "image_url": "https://placehold.co/800x800/EAB308/ffffff?text=Jacket",
    },
]

for prod_data in products_data:
    existing = db.query(Product).filter(Product.name == prod_data["name"]).first()
    if not existing:
        db.add(Product(**prod_data))

db.commit()

# Seed default admin
existing_admin = db.query(Admin).filter(Admin.username == "munene").first()
if not existing_admin:
    admin = Admin(
        username="munene",
        email="admin@msecurecomputers.co.ke",
        hashed_password=get_password_hash("Admin@MSec2026"),
    )
    db.add(admin)
    db.commit()
    print("✅ Default admin created: username=munene, password=Admin@MSec2026")
    print("⚠️  CHANGE THIS PASSWORD IMMEDIATELY AFTER FIRST LOGIN!")

print("✅ Database seeded successfully!")
db.close()
