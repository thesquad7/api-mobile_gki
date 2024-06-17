from datetime import datetime
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name :str
    use_id :str
    color_id :int
    
class CategoryUpdate(BaseModel):
    name :str
    use_id :str
    color_id :int
    updated_at : datetime = None

class CategoryResponse(BaseModel):
    name :str
    color_id :str or None