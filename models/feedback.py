from pymysql import Date, Time
from sqlalchemy import Column,Integer, String, Text
from config.db import Base

class Feedback(Base):
    __tablename__ = 'feeds'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    content = Column(Text)
    content_img = Column(Text)
