from datetime import datetime
from pydantic import BaseModel

class PendetaRequest(BaseModel):
    name : str
    status : str
class PendetaRequestEntity(BaseModel):
    name : str
    id : int
class PendetaCreate(BaseModel):
    profile_img : str

class PendetaUpdate(BaseModel):
    name: str = None
    status: str = None
    profile_img: str = None
    updated_at: datetime = None