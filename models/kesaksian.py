
from sqlalchemy import Column,Integer, String, Text,DATE
from config.db import Base

class Kesaksian(Base):
    __tablename__ = 'kesaksians'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    status = Column(Text)
    date =Column(DATE)
    content_img = Column(Text)
    user_id = Column(String(12))
