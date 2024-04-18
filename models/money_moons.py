from datetime import datetime,timezone
from pymysql import Date, Time
from sqlalchemy import Column, DateTime,Integer, String, Text
from config.db import Base
class Money(Base):
    __tablename__ = 'money_moons'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    code = Column(Integer)
    total = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)