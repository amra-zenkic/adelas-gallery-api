from fastapi import FastAPI, HTTPException, Depends
from starlette.middleware.cors import CORSMiddleware
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import UserRegisterSchema
from server.routers import adminCategory
import services
import fastapi.security as _security
from routers import admin, photos, adminPhotos, gallery

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def start_application():
    app = FastAPI()
    origins = ["http://localhost:3000", "https://medic-web-sigma.vercel.app"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    return app

app = start_application()

app.include_router(admin.router)
app.include_router(photos.router)
app.include_router(adminCategory.router)
app.include_router(adminPhotos.router)
app.include_router(gallery.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}



