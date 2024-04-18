from datetime import datetime
from pydantic import BaseModel

class ChurchRequest(BaseModel):
    name : str
    status : str
class ChurchCreate(BaseModel):
    content_img : str

class ChurchUpdate(BaseModel):
    name: str = None
    content_img: str = None
    updated_at: datetime = None