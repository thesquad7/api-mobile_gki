
from sqlalchemy import Column,Integer, String, Text, Boolean,Date,Time
from config.db import Base
class Office(Base):
    __tablename__ = 'offices'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    start = Column(Time)
    end = Column(Time)
    status = Column(Boolean)
