from pydantic import BaseModel, EmailStr, constr
from datetime import date
from typing import Optional

class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    photo_path: str | None = None
    instagram_url: str | None = None
    facebook_url: str | None = None
    linkedin_url: str | None = None

    class Config:
        orm_mode = True

class PhotoUpload(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    date: Optional[date] = None

class CategoryUpload(BaseModel):
    category_name: str

class CategoriesAndPhotoUpload(BaseModel):
    list_id_category: str

class GalleryUpload(BaseModel):
    gallery_name: str

class GalleryAndPhotoUpload(BaseModel):
    list_id_gallery: str

class AdminDetails(BaseModel):
    username: str
    email: EmailStr
    description: str | None = None
    photo_path: str | None = None
    instagram_url: str | None = None
    facebook_url: str | None = None
    linkedin_url: str | None = None
