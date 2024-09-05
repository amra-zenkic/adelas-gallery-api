from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, HTTPException
from database import SessionLocal
from models import Service
from schemas import ServicesRequest
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
    prefix="/admin/services",
    tags=["admin services"],
    responses={404: {"description": "Not found"}},
)

user_dependencies = Annotated[dict, Depends(services.get_current_user)]

@router.get('/count')
async def get_count_services(db: SessionLocal = Depends(get_db)):
    services = db.query(Service).count()
    return services

@router.get('/all')
async def get_all_services(db: SessionLocal = Depends(get_db)):
    services = db.query(Service).all()
    return services

@router.post('/create')
async def create_service(service: ServicesRequest, user: user_dependencies, db: SessionLocal = Depends(get_db)):
    new_service = Service(
        service_name = service.service_name,
        description = service.description,
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

@router.put('/update/{service_id}')
async def update_service(service_id: int, user: user_dependencies, service: ServicesRequest, db: SessionLocal = Depends(get_db)):
    new_service = db.query(Service).filter(Service.id_service == service_id).first()
    if not new_service:
        raise HTTPException(status_code=404, detail="Service not found")
    new_service.service_name = service.service_name
    new_service.description = service.description
    db.commit()
    db.refresh(new_service)
    return new_service

@router.delete('/delete/{service_id}')
async def delete_service(service_id: int, db: SessionLocal = Depends(get_db)):
    service = db.query(Service).filter(Service.id_service == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(service)
    db.commit()
    return service