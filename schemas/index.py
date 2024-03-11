from datetime import date, time
from pydantic import BaseModel

class JadwalBase(BaseModel):
    title: str
    content: str
    tanggal_mulai: date
    waktu_mulai: time
    content_img: str
    pendeta_id: str

class UserBase(BaseModel):
    username : str
    name : str
    password : str

class UserResponse(BaseModel):
    id : int
    username : str
    name : str
    user_pic : str
    password : str