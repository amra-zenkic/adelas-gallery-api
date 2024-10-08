from pydantic import BaseModel, EmailStr, constr
from datetime import date
from typing import Optional

class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    description: str | None = None
    photo_path: str | None = None
    instagram_url: str | None = None
    facebook_url: str | None = None
    linkedin_url: str | None = None

    class Config:
        orm_mode = True

class UserEditSchema(BaseModel):
    username: str
    email: EmailStr
    description: str | None = None
    instagram_url: str | None = None
    facebook_url: str | None = None
    linkedin_url: str | None = None

    class Config:
        orm_mode = True

class PhotoUpload(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    date: Optional[str] = None

class CategoryUpload(BaseModel):
    category_name: str

class CategoriesAndPhotoUpload(BaseModel):
    list_id_category: str

class GalleryUpload(BaseModel):
    gallery_name: str

class GalleryAndPhotoUpload(BaseModel):
    list_id_gallery: str

class AdminDetails(BaseModel):
    id_user: int
    username: str
    email: EmailStr
    description: str | None = None
    photo_path: str | None = None
    instagram_url: str | None = None
    facebook_url: str | None = None
    linkedin_url: str | None = None

class UserChangePassword(BaseModel):
    current_password: str
    new_password: str

class ServicesRequest(BaseModel):
    service_name: str
    description: str | None = None


class PhotoBase(BaseModel):
    id_photo: int
    photo_path: str
    title: Optional[str]
    description: Optional[str]
    location: Optional[str]
    date: Optional[date]

    class Config:
        orm_mode = True

class GalleryBase(BaseModel):
    id_gallery: int
    gallery_name: str

    class Config:
        orm_mode = True

class GalleryAndPhotosBase(BaseModel):
    id_gallery: int
    id_photo: int
    gallery: Optional[GalleryBase]
    photo: Optional[PhotoBase]

    class Config:
        orm_mode = True
