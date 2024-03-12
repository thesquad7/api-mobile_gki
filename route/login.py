from fastapi import Depends, FastAPI, HTTPException, UploadFile, status, APIRouter
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timedelta
from jose import JWTError,jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated
import models.index
from config.db import LocalSession
from passlib.context import CryptContext
from schemas.index import UserResponse, Token, TokenData, UserInDB, UserRequest, User
import config.upload
from config.setting import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MUNITES,ALGORITHM

route_login = APIRouter(prefix="/api/v1", tags=['Login'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/token")
def get_db():
    db= LocalSession()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

async def get_user_active(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User tidak ter validasi')
        return{'detail': 'you have access'}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User tidak dapat diketahui')

user_refs = Annotated[dict, Depends(get_user_active)]

@route_login.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_refs, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Auth Gagal')
    return {"User": user}
