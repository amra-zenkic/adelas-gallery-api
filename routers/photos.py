from fastapi import APIRouter, HTTPException, Depends
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/photos",
    tags=["photos"],
    responses={404: {"description": "Not found"}},
)



