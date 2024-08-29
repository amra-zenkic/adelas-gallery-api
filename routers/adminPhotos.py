from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, HTTPException
from database import SessionLocal
from models import Photo, CategoriesAndPhotos, Category, GalleryAndPhotos
from schemas import PhotoUpload, CategoriesAndPhotoUpload, GalleryAndPhotoUpload
import services
from typing import Annotated
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
    prefix="/admin/photos",
    tags=["admin photos"],
    responses={404: {"description": "Not found"}},
)

user_dependencies = Annotated[dict, Depends(services.get_current_user)]

# Set up the upload directory
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png", "gif"}

# Utility function to check file type
def check_file_type(file: UploadFile) -> bool:
    try:
        # Open the file using PIL to check if it is a valid image
        image = Image.open(file.file)
        if image.format.lower() in ALLOWED_EXTENSIONS:
            file.file.seek(0)  # Reset file pointer to the beginning
            return True
    except Exception:
        return False
    return False

# Endpoint to upload an image
@router.post("/photo/upload")
async def upload_file(
    user: user_dependencies,
    file: UploadFile = File(...), 
    request: PhotoUpload = Depends(),
    categories: CategoriesAndPhotoUpload = Depends(),
    db: SessionLocal = Depends(get_db)):
    # Check if the file is a valid image
    if not check_file_type(file):
        raise HTTPException(status_code=400, detail="Error: Images Only!")
    
    # Generate a unique file name
    file_extension = Path(file.filename).suffix
    
    # path where file is saved is '/uploads/<file_name>' :
    file_name = f"{file.filename.split('.')[0]}-{Path(file.filename).stem}-{Path(file.filename).suffix}"
    file_path = UPLOAD_DIR / file_name

    # Save the file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_photo = Photo(
        photo_path = f"/uploads/{file_name}",
        title = request.title,
        description = request.description,
        location = request.location,
        date = request.date
    )
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)

    categoriesList = categories.list_id_category.split(",")

    for id_category in categoriesList:
        new_category_and_photo = CategoriesAndPhotos(
            id_photo = new_photo.id_photo,
            id_category = int(id_category)
        )
        db.add(new_category_and_photo)
        db.commit()
        db.refresh(new_category_and_photo)

    return {"id_photo": new_photo.id_photo}

@router.put("/photo/update-details/{photo_id}")
async def update_photo(photo_id: int, request: PhotoUpload, db: SessionLocal = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id_photo == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    photo.title = request.title
    photo.description = request.description
    photo.location = request.location
    photo.date = request.date
    db.commit()
    return {"message": "Photo updated successfully"}

@router.put("/photo/update-category/{photo_id}")
async def update_photo(photo_id: int, categories: CategoriesAndPhotoUpload, db: SessionLocal = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id_photo == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    db.query(CategoriesAndPhotos).filter_by(id_photo=photo_id).delete()
    db.commit()

    categoriesList = categories.list_id_category.split(",")

    for category_id in categoriesList:
        new_category_and_photo = CategoriesAndPhotos(
            id_photo = photo_id,
            id_category = category_id
        )
        db.add(new_category_and_photo)
        db.commit()
        db.refresh(new_category_and_photo)

    return {"message": "Photo updated successfully"}

@router.put('/photo/update-gallery/{photo_id}')
async def update_photo(photo_id: int, galleries: GalleryAndPhotoUpload, db: SessionLocal = Depends(get_db)):
    galleriesList = galleries.list_id_gallery.split(",")

    db.query(GalleryAndPhotos).filter_by(id_photo=photo_id).delete()
    db.commit()
    for gallery_id in galleriesList:
        new_gallery_and_photo = GalleryAndPhotos(
            id_photo = photo_id,
            id_gallery = gallery_id
        )
        db.add(new_gallery_and_photo)
        db.commit()
        db.refresh(new_gallery_and_photo)
        
    return {"message": "Photo updated successfully"}


@router.delete("/photo/delete/{photo_id}")
async def delete_photo(photo_id: int, db: SessionLocal = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id_photo == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    db.delete(photo)
    db.commit()
    return {"message": "Photo deleted successfully"}




