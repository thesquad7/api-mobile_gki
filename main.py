from fastapi import FastAPI,HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from config.db import engine, LocalSession
from sqlalchemy.orm import Session
from datetime import date, timedelta
import models.index
from models.users import User
app=FastAPI()

models.index._Jadwal.metadata.create_all(bind=engine)
models.index._User.metadata.create_all(bind=engine)
class JadwalBase(BaseModel):
    title: str
    content: str
    tanggal_mulai: date
    waktu_mulai: timedelta
    pendeta_id: str

class UserBase(BaseModel):
    username: str

def get_db():
    db= LocalSession()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user= User(**user.dict())
    db.add(db_user)
    db.commit()

