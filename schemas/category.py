from datetime import datetime
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name :str
    use_id :str
    color_id :str
    
class CategoryUpdate(BaseModel):
    name :str
    updated_at : datetime = None