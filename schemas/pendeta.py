from pydantic import BaseModel

class PendetaRequest(BaseModel):
    name : str
    status : str
class PendetaCreate(BaseModel):
    profile_img : str

class PendetaUpdate(BaseModel):
    name: str = None
    status: str = None
    profile_img: str = None