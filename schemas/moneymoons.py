from datetime import date, time
from pydantic import BaseModel

class MoneyMoonRequest(BaseModel):
    name : str
    status : str
class MoneyMoonCreate(BaseModel):
    content_img : str

class MoneyMoonUpdate(BaseModel):
    name: str = None
    code : int or None
    total : int

    