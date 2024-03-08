from sqlalchemy import Table,Column,Boolean,Integer,String,Text,Date, Time
from config.db import Base

class Jadwal(Base):
    __tablename__ = 'jadwals'
    
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String(50))
    content = Column(Text)
    content_img = Column(Text)
    waktu_mulai = Column(Time)
    tanggal_mulai = Column(Date)
    pendeta_id = Column(String(12))

