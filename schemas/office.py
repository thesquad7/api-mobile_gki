from datetime import date, datetime, time
from pydantic import BaseModel

class OfficeTimeRequest(BaseModel):
    name : str
    status : str
class OfficeTimeCreate(BaseModel):
    content_img : str

class OfficeTimeUpdate(BaseModel):
    name: str = None
    status: bool = None
    start : time or None
    end: time or None
    updated_at: datetime = None

    