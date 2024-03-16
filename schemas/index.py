from datetime import date, time
from fastapi import UploadFile
from pydantic import BaseModel

class JadwalBase(BaseModel):
    title: str
    content: str
    tanggal_mulai: date
    waktu_mulai: time
    content_img: str
    pendeta_id: str

class User(BaseModel):
    username : str
    name : str
    password : str


class UserResponse(BaseModel):
    id : int
    username : str
    name : str
    user_pic : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username : str or None = None


class UserInDB(User):
    password : str

class UserRequest(BaseModel):
    username: str
    password: str
    name : str

class PendetaRequest(BaseModel):
    name : str
    status : str
class PendetaCreate(BaseModel):
    profile_img : str

class CategoryCreate(BaseModel):
    name :str

class PendetaUpdate(BaseModel):
    name: str = None
    status: str = None
    profile_img: str = None