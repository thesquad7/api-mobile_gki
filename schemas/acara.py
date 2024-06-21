from datetime import date, datetime, time
from pydantic import BaseModel

class AcaraRequest(BaseModel):
    name : str
    status : str
class AcaraCreate(BaseModel):
    content_img : str

class AcaraUpdate(BaseModel):
    name: str = None
    status: str = None
    content: str = None
    content_img : str or None
    tanggal : date
    jam_acara : time
    category_id : int
    updated_at: datetime = None

class AcaraUpdateNoImage(BaseModel):
    name: str = None
    status: str = None
    content: str = None
    tanggal : date
    jam_acara : time
    category_id : int
    updated_at: datetime = None
    