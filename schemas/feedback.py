from datetime import datetime
from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    name : str
    status : str
class FeedbackCreate(BaseModel):
    profile_img : str

class FeedbackUpdate(BaseModel):
    name: str = None
    content: str = None
    content_img: str = None
    updated_at: datetime = None