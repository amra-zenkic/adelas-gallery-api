from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, HTTPException
from starlette.middleware.cors import CORSMiddleware
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import UserRegisterSchema, AdminDetails
import services
import fastapi.security as _security
from models import Photo, CategoriesAndPhotos, Category
from schemas import PhotoUpload, CategoriesAndPhotoUpload
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
from typing import Annotated
from PIL import Image

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


