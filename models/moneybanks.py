from datetime import datetime,timezone
from pymysql import Date, Time
from sqlalchemy import Column, DateTime,Integer, String, Text
from config.db import Base

class MoneyBank(Base):
    __tablename__ = 'moneybanks'
    
    id = Column(Integer,primary_key=True, index=True)
    from_inv = Column(String(50))
    total = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)