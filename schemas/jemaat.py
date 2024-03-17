from datetime import date, time
from pydantic import BaseModel

class JemaatRequest(BaseModel):
    name : str
    status : str
class JemaatCreate(BaseModel):
    content_img : str

class JemaatUpdate(BaseModel):
    jemaat_id:str or None
    name : str or None
    jemaat_img:str or None
    tempat_lahir : str or None
    tanggal_lahir: date or None
    nama_bapak: str or None
    nama_ibu: str or None
    nama_baptis: str or None
    alamat: str or None
    