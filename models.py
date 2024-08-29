from sqlalchemy import Column, ForeignKey, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)
    description = Column(Text)
    photo_path = Column(String(500))
    instagram_url = Column(String(500))
    facebook_url = Column(String(500))
    linkedin_url = Column(String(500))

class Photo(Base):
    __tablename__ = "photos"
    
    id_photo = Column(Integer, primary_key=True, index=True)
    photo_path = Column(String(300), nullable=False)
    title = Column(String(300))
    description = Column(String(300))
    location = Column(String(300))
    date = Column(Date)
    
    # Relationships
    categories = relationship("CategoriesAndPhotos", back_populates="photo", cascade="all, delete")
    featured_photos = relationship("FeaturedPhoto", back_populates="photo", cascade="all, delete")
    galleries = relationship("GalleryAndPhotos", back_populates="photo", cascade="all, delete")


class Category(Base):
    __tablename__ = "categories"
    
    id_category = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)
    
    # Relationships
    photos = relationship("CategoriesAndPhotos", back_populates="category")


class CategoriesAndPhotos(Base):
    __tablename__ = "categories_and_photos"
    
    id_category = Column(Integer, ForeignKey('categories.id_category', ondelete='CASCADE'), primary_key=True)
    id_photo = Column(Integer, ForeignKey('photos.id_photo', ondelete='CASCADE'), primary_key=True)
    
    # Relationships
    category = relationship("Category", back_populates="photos")
    photo = relationship("Photo", back_populates="categories")


class FeaturedPhoto(Base):
    __tablename__ = "featured_photos"
    
    id_photo = Column(Integer, ForeignKey('photos.id_photo', ondelete='CASCADE'), primary_key=True)
    featured_type = Column(String(20), primary_key=True)
    
    # Relationships
    photo = relationship("Photo", back_populates="featured_photos")


class Service(Base):
    __tablename__ = "services"
    
    id_service = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(300), nullable=False)
    description = Column(Text)
    icon = Column(String(500))


class Gallery(Base):
    __tablename__ = "gallery"
    
    id_gallery = Column(Integer, primary_key=True, index=True)
    gallery_name = Column(String(200))
    
    # Relationships
    photos = relationship("GalleryAndPhotos", back_populates="gallery")


class GalleryAndPhotos(Base):
    __tablename__ = "gallery_and_photos"
    
    id_gallery = Column(Integer, ForeignKey('gallery.id_gallery', ondelete='CASCADE'), primary_key=True)
    id_photo = Column(Integer, ForeignKey('photos.id_photo', ondelete='CASCADE'), primary_key=True)
    
    # Relationships
    gallery = relationship("Gallery", back_populates="photos")
    photo = relationship("Photo", back_populates="galleries")
