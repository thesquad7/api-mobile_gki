from datetime import date, datetime
from pydantic import BaseModel

class ChurchVRequest(BaseModel):
    name : str
    status : str
class ChurchVCreate(BaseModel):
    profile_img : str

class ChurchVUpdate(BaseModel):
    w_jemaat: int = None
    p_jemaat: int = None
    w_visit: int = None
    p_visit:int = None
    jemaat_t : date = None
    stream : bool = None
    stream_count : int = None
    church_id: int
    updated_at: datetime = None