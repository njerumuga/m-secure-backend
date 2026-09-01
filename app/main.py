import cloudinary
import cloudinary.uploader
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from  app.routers import products, auth, categories
from app.core.database import engine, Base
import os

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="M-Secure Computers API",
    description="E-Commerce API for M-Secure Computers - Branding & Printing",
    version="1.0.0",
)

# Cloudinary Configuration
cloudinary.config( 
  cloud_name = "dsn3ubhdq", 
  api_key = "674323722557894", 
  api_secret = "L7RywDxb4qqihAdiuCSoXd5ilB4",
  secure = True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])


@app.get("/")
def root():
    return {"message": "M-Secure Computers API is live 🚀", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}