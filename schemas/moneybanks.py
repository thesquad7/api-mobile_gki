from datetime import date, time
from pydantic import BaseModel

class MoneyTFRequest(BaseModel):
    name : str
    status : str
class MoneyTFCreate(BaseModel):
    content_img : str

class MoneyTFUpdate(BaseModel):
    from_inv: str = None
    total : int

    