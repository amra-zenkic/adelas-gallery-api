import fastapi
import database as _database, models as _models, schemas as _schemas
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import fastapi.security as _security
import datetime as _dt
from decouple import config
import jwt as _jwt

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/admin/login")
JWT_SECRET = config("JWT_SECRET")

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()

async def create_user(request: _schemas.UserRegisterSchema, db: _orm.Session):
    new_user = _models.User(
        username = request.username,
        email = request.email,
        password = _hash.bcrypt.hash(request.password),
        photo_path = request.photo_path,
        instagram_url = request.instagram_url,
        facebook_url = request.facebook_url,
        linkedin_url = request.linkedin_url
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not _hash.bcrypt.verify(password, user.password):
        return False
    return user

async def create_token(user: _models.User):
    user_obj = {"sub": user.username, 
                "email": user.email,
                "id": user.id_user, 
                "exp": _dt.datetime.utcnow() + _dt.timedelta(minutes=20),
                "iat": _dt.datetime.utcnow()} 
    
    token = _jwt.encode(user_obj, JWT_SECRET)
    
    return dict(access_token=token, token_type="bearer")

async def get_current_user(
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
        print("do user ", user.instagram_url)
        userReturn = _schemas.AdminDetails(
            username = user.username,
            email = user.email,
            description=user.description,
            photo_path = user.photo_path,
            instagram_url = user.instagram_url,
            facebook_url = user.facebook_url,
            linkedin_url = user.linkedin_url
        )
        return userReturn
    except Exception as e:
        raise fastapi.HTTPException(
            status_code=401, detail=f"Error: {e}"
        )