from datetime import date, datetime, time
from pydantic import BaseModel

class MoneyTFRequest(BaseModel):
    name : str
    status : str
class MoneyTFCreate(BaseModel):
    content_img : str

class MoneyTFUpdate(BaseModel):
    from_inv: str = None
    total : int
class MoneyTFUpdatePUT(BaseModel):
    from_inv: str = None
    total : int
    updated_at: datetime = None

    