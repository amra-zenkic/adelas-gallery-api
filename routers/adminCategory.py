from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, HTTPException
from starlette.middleware.cors import CORSMiddleware
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import UserRegisterSchema, CategoryUpload
import services
import fastapi.security as _security
from models import Photo, CategoriesAndPhotos, Category
from schemas import PhotoUpload, CategoriesAndPhotoUpload
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
from PIL import Image

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/admin/category",
    tags=["admin category"],
    responses={404: {"description": "Not found"}},
)

@router.get('/all')
async def get_all_categories(db: SessionLocal = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

@router.post("/add")
async def add_category(category: CategoryUpload, db: SessionLocal = Depends(get_db)):
    new_category = Category(
        category_name = category.category_name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {"id_category": new_category.id_category}

@router.put("/update/{category_id}")
async def update_category(category_id: int, categoryUpload: CategoryUpload, db: SessionLocal = Depends(get_db)):
    category = db.query(Category).filter(Category.id_category == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.category_name = categoryUpload.category_name
    db.commit()
    db.refresh(category)
    return category

@router.delete("/delete/{category_id}")
async def delete_category(category_id: int, db: SessionLocal = Depends(get_db)):
    category = db.query(Category).filter(Category.id_category == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}