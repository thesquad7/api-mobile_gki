from sqlalchemy import Column, ForeignKey, Integer, String, Text, Time,Date
from config.db import Base
from sqlalchemy.orm import relationship

class Jadwal(Base):
    __tablename__ = 'jadwals'
    
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String(50))
    content = Column(Text)
    content_img = Column(Text)
    waktu_mulai = Column(Time)
    tanggal_mulai = Column(Date)
    pendeta_id = Column('pendeta_id',Integer(),ForeignKey("pendetas.id") )
    pendeta = relationship("Pendeta", back_populates="jadwals")
