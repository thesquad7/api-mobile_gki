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
    username: str
    username = str
    name = str
    password = str