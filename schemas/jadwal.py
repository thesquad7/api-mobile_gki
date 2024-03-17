from datetime import date, time
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

    