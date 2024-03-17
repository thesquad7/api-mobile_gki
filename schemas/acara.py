from datetime import date, time
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
    category_id : int

    