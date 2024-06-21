from datetime import date, datetime, time
from pydantic import BaseModel

class JadwalRequest(BaseModel):
    name : str
    status : str
class JadwalCreate(BaseModel):
    content_img : str

class JadwalUpdate(BaseModel):
    title: str = None
    content: str = None
    content_img : str or None
    waktu_mulai : time
    tanggal_mulai : date
    pendeta_id : int
    category_id : int
    church_id : int
    updated_at: datetime = None

class JadwalUpdateNoImage(BaseModel):
    title: str = None
    content: str = None
    waktu_mulai : time
    tanggal_mulai : date
    pendeta_id : int
    category_id : int
    church_id : int
    updated_at: datetime = None
        