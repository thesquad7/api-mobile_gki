from datetime import datetime,timezone
from pymysql import Date, Time
from sqlalchemy import Column, DateTime,Integer, String, Text
from config.db import Base
class Users(Base):
    __tablename__= 'users'

    id = Column(Integer,primary_key=True, index=True)
    username = Column(String(50), unique=True)
    user_img = Column(Text)
    name = Column(String(60))
    password = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
