from datetime import date, time
from pydantic import BaseModel

class RenunganRequest(BaseModel):
    name : str
    status : str
class RenunganCreate(BaseModel):
    content_img : str

class RenunganUpdate(BaseModel):
    name: str = None
    content: str = None
    content_img : str or None
    tanggal : date
    category_id : int

    