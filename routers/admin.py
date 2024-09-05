from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, HTTPException
from starlette.middleware.cors import CORSMiddleware
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import UserChangePassword, UserEditSchema, UserRegisterSchema, AdminDetails
import services
import fastapi.security as _security
from models import Photo, CategoriesAndPhotos, Category, User
from schemas import PhotoUpload, CategoriesAndPhotoUpload
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
from typing import Annotated
from PIL import Image
import passlib.hash as _hash


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
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

@router.post("/register") # for registration, adds new user to db, returns token
async def create_user(
    user: UserRegisterSchema, db: Session = Depends(get_db)
):
    db_user = await services.get_user_by_email(user.username, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already in use")

    user = await services.create_user(user, db)

    return user

@router.post("/login") # for admin login
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(services.get_db),
):
    user = await services.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Admin Credentials")

    token = await services.create_token(user)
    return token

@router.get("/me", response_model=AdminDetails) # returns currenly logged in user, if not then 401
async def get_user(user: AdminDetails = Depends(services.get_current_user)):
    return user

@router.put("/update/{user_id}")
async def update_user(user_id: int, user: UserEditSchema, db: Session = Depends(get_db), user2: AdminDetails = Depends(services.get_current_user)):
    new_user = db.query(User).filter(User.id_user == user_id).first()
    if not new_user:
        raise HTTPException(status_code=404, detail="User not found")
    new_user.username = user.username
    new_user.email = user.email
    new_user.description = user.description
    new_user.instagram_url = user.instagram_url
    new_user.facebook_url  = user.facebook_url
    new_user.linkedin_url = user.linkedin_url
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put('/update/password/{user_id}')
async def update_user_password(
    user_id: int, 
    changeDetails: UserChangePassword, 
    db: Session = Depends(get_db), 
    user: AdminDetails = Depends(services.get_current_user)
):
    new_user = db.query(User).filter(User.id_user == user_id).first()
    if not new_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify current password
    if not _hash.bcrypt.verify(changeDetails.current_password, new_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    # Update password
    new_user.password = _hash.bcrypt.hash(changeDetails.new_password)
    db.commit()
    db.refresh(new_user)
    return {"msg": "Password updated successfully"}

@router.put('/update/photo/{user_id}')
async def update_user_photo(
    user: user_dependencies,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    new_user = db.query(User).filter(User.id_user == user.id_user).first()
    if not new_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not check_file_type(file):
        raise HTTPException(status_code=400, detail="Error: Images Only!")
    
    photo_name = "admin" + str(new_user.id_user) + Path(file.filename).suffix
    
    # Ensure file path is saved as a string
    file_path = UPLOAD_DIR / photo_name

    # Save the file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convert file_path to a relative path string with the desired format
    relative_path = f"/{file_path.as_posix()}"
    new_user.photo_path = relative_path
    db.commit()
    db.refresh(new_user)
    
    return new_user


