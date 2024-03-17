from datetime import date, time
from fastapi import UploadFile
from pydantic import BaseModel
from schemas.pendeta import PendetaCreate,PendetaRequest,PendetaUpdate
from schemas.category import CategoryCreate
from schemas.user import User,UserInDB,UserRequest,UserResponse,Token,TokenData
from schemas.church import ChurchCreate, ChurchRequest,ChurchUpdate

class JadwalBase(BaseModel):
    title: str
    content: str
    tanggal_mulai: date
    waktu_mulai: time
    content_img: str
    pendeta_id: str




