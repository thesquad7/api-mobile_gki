
from sqlalchemy import Table,Column,Boolean,Integer,String,Text,DateTime, Time
from config.db import Base

class User(Base):
    __tablename__= 'users'

    id = Column(Integer,primary_key=True, index=True)
    username = Column(String(50), unique=True)


