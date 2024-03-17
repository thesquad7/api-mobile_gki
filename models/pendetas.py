from pymysql import Date, Time
from sqlalchemy import Column,Integer, String, Text
from config.db import Base
from sqlalchemy.orm import relationship

class Pendeta(Base):
    __tablename__ = 'pendetas'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50), )
    status = Column(Text,)
    profile_img = Column(Text)
    jadwals = relationship("Jadwal", back_populates="pendeta")
    jemaats= relationship("Jemaats", back_populates="pendeta")