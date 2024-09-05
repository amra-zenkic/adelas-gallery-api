from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Gallery
from schemas import GalleryUpload
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
    prefix="/admin/gallery",
    tags=["admin gallery"],
    responses={404: {"description": "Not found"}},
)

@router.get('/all')
async def get_all_galleries(db: Session = Depends(get_db)):
    gallery = db.query(Gallery).all()
    return gallery

@router.get('/count')
async def get_count_galleries(db: Session = Depends(get_db)):
    gallery = db.query(Gallery).count()
    return gallery

@router.post('/add')
def add_gallery(request: GalleryUpload, db: Session = Depends(get_db)):
    new_gallery = Gallery(
        gallery_name = request.gallery_name
    )
    db.add(new_gallery)
    db.commit()
    db.refresh(new_gallery)
    return new_gallery

@router.put('/update/{gallery_id}')
def update_gallery(gallery_id: int, request: GalleryUpload, db: Session = Depends(get_db)):
    gallery = db.query(Gallery).filter(Gallery.id_gallery == gallery_id).first()
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")
    gallery.gallery_name = request.gallery_name
    db.commit()
    db.refresh(gallery)
    return gallery

@router.delete('/delete/{gallery_id}')
def delete_gallery(gallery_id: int, db: Session = Depends(get_db)):
    gallery = db.query(Gallery).filter(Gallery.id_gallery == gallery_id).first()
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")
    db.delete(gallery)
    db.commit()
    return {"message": "Gallery deleted successfully"}