from pydantic import BaseModel
from datetime import date, datetime
class KesaksianRequest(BaseModel):
    name : str
    status : str
class KesaksianCreate(BaseModel):
    profile_img : str

class KesaksianUpdate(BaseModel):
    name: str = None
    author: str = None
    content_img: str = None
    content: str = None
    date: date
    user_id: int = None
    updated_at: datetime = None

class KesaksianUpdateNoImage(BaseModel):
    name: str = None
    author: str = None
    date: date
    content: str = None
    user_id: int = None
    updated_at: datetime = None

class ProfileBase(BaseModel):
    id: int
    profile_img: str
    name: str

    class Config:
        orm_mode = True