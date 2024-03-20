from fastapi import Depends, HTTPException, UploadFile, status, APIRouter
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timedelta
from jose import jwt
from sqlalchemy.orm import Session
from typing import Annotated
from ModelIndex import Users
from config.db import LocalSession
from passlib.context import CryptContext
from SchemasIndex import Token, UserRequest
import config.upload
from .login import user_refs

route_auth = APIRouter(prefix="/api/v1", tags=['Auth'])

SECRET_KEY = "148bebf7123c3b4a2fa9acde2bae7f367d590b5708d9bac268953cde72a86f6a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MUNITES = 30

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db= LocalSession()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(username: str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(username:str , user_id:str, expires_delta: timedelta):
    encode= {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

db_dependency = Annotated[Session, Depends(get_db)]

@route_auth.post("/register",response_model=UserRequest)
async def register_user(username:str, password:str, name:str,file: UploadFile, db: db_dependency):
    existing_user = db.query(Users).filter(Users.username == username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed_password = bcrypt_context.hash(password)
    path = f'{config.upload.USER_IMG_DIR}{file.filename}'
    with open(path, "wb") as buffer:
        buffer.write(await file.read())
    db_user = Users(username=username, name=name, password=hashed_password, user_img=path)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
                                       

@route_auth.post("/token", response_model=Token)
async def login_for_access_token(formdata: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(formdata.username, formdata.password, db)
    usex = db.query(Users).filter(Users.username == formdata.username).first()
    cred = usex.id
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Tidak Valid")
    token = create_access_token(user.username, user.id, timedelta(minutes=30))
    return {'credential':cred, 'access_token': token, 'token_type': 'bearer'}

@route_auth.get("/user/{user_id}")
async def user_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(Users).filter(Users.id == api_id).first()
    pic = db_show.user_img
    uname= db_show.name
    return {'name': uname, 'pic':pic}
