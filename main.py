from fastapi import FastAPI,HTTPException,Depends,status, UploadFile
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from config.db import engine, LocalSession, Base
from sqlalchemy.orm import Session
from datetime import date, time, timedelta
from route.auth import route_auth
from route.login import route_login
import json
import os
import models.index
import config.upload
import schemas.index
import hashlib

app=FastAPI()
Base.metadata.create_all(bind=engine)

def get_password_hash(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db():
    db= LocalSession()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

app.include_router(router=route_auth)
app.include_router(router=route_login)


@app.post("/jadwal",status_code=status.HTTP_201_CREATED)
async def create_jadwal(title_i: str, content_i:str,tanggal_mulai_i:date, waktu_mulai_i:time,pendeta_id_i:str, file: UploadFile, db: db_dependency):
    path = f'{config.upload.JADWAL_IMG_DIR}{file.filename}'
    with open(path, "wb") as buffer:
        buffer.write(await file.read())
    db_jadwal= models.index.Jadwal(title = title_i, content = content_i,tanggal_mulai=tanggal_mulai_i,waktu_mulai= waktu_mulai_i,pendeta_id=pendeta_id_i,content_img=path )
    db.add(db_jadwal)
    db.commit()
    return{"detail": "Jadwal di upload"}

@app.get("/jadwal/{jadwal_id}", status_code=status.HTTP_200_OK)
async def read_jadwal(jadwal_id: int, db : db_dependency):
    jadwal=db.query(models.index.Jadwal).filter(models.index.Jadwal == jadwal_id).first
    if jadwal is None:
        raise HTTPException(status_code=404, detail="Jadwal Tidak Ditemukan")
    return jadwal


@app.delete("/jadwal/{jadwal_id}", status_code=status.HTTP_200_OK)
async def delete_jadwal(jadwal_id: int, db:db_dependency):
    db_jadwal=db.query(models.index.Jadwal).filter(models.index.Jadwal.id).first()
    if jadwal_id is None:
        raise HTTPException(status_code=404, detail="Jadwal tidak ditemukan")
    db.delete(db_jadwal)
    db.commit()

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.index.User, db: db_dependency):
    db_user= models.index.User(**user.dict())
    db.add(db_user)
    db.commit()

@app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query (models.index.User).filter(models.index.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User Tidak Ditemukan")
    return user
