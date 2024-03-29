from pydantic import BaseModel
from datetime import date
class KesaksianRequest(BaseModel):
    name : str
    status : str
class KesaksianCreate(BaseModel):
    profile_img : str

class KesaksianUpdate(BaseModel):
    name: str = None
    status: str = None
    content_img: str = None
    date: date
    user_id: int = None