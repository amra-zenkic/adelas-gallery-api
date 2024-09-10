from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, HTTPException
from database import SessionLocal
from models import Gallery, Photo, CategoriesAndPhotos, Category, GalleryAndPhotos
from schemas import GalleryAndPhotosBase, GalleryUpload, PhotoUpload, CategoriesAndPhotoUpload, GalleryAndPhotoUpload
import services
from typing import Annotated, List
import shutil
from pathlib import Path
from PIL import Image
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/admin/gallery",
    tags=["admin gallery"],
    responses={404: {"description": "Not found"}},
)

user_dependencies = Annotated[dict, Depends(services.get_current_user)]

@router.get("/all-photos-and-gallery", response_model=List[GalleryAndPhotosBase]) # returns all photos and gallery but needs fixed
def get_all_photos_and_galleries(user: user_dependencies, db: Session = Depends(get_db)):
    photos = (
        db.query(GalleryAndPhotos)
        .join(Gallery, GalleryAndPhotos.id_gallery == Gallery.id_gallery)
        .outerjoin(Photo, GalleryAndPhotos.id_photo == Photo.id_photo)
        .all()
    )

    return photos  # This will automatically convert using Pydantic


@router.get('/all')
async def get_all_galleries(user: user_dependencies, db: Session = Depends(get_db)):
    gallery = db.query(Gallery).all()
    return gallery

@router.get('/count')
async def get_count_galleries( db: Session = Depends(get_db)):
    gallery = db.query(Gallery).count()
    return gallery

@router.post('/add')
def add_gallery(user: user_dependencies, request: GalleryUpload, db: Session = Depends(get_db)):
    new_gallery = Gallery(
        gallery_name = request.gallery_name
    )
    db.add(new_gallery)
    db.commit()
    db.refresh(new_gallery)
    return new_gallery

@router.put('/update/{gallery_id}')
def update_gallery(user: user_dependencies, gallery_id: int, request: GalleryUpload, db: Session = Depends(get_db)):
    gallery = db.query(Gallery).filter(Gallery.id_gallery == gallery_id).first()
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")
    gallery.gallery_name = request.gallery_name
    db.commit()
    db.refresh(gallery)
    return gallery

@router.delete('/delete/{gallery_id}')
def delete_gallery(user: user_dependencies, gallery_id: int, db: Session = Depends(get_db)):
    gallery = db.query(Gallery).filter(Gallery.id_gallery == gallery_id).first()
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")
    db.delete(gallery)
    db.commit()
    return {"message": "Gallery deleted successfully"}