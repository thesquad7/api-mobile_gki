from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Time,Date
from config.db import Base
from sqlalchemy.orm import relationship

class Jadwal(Base):
    __tablename__ = 'jadwals'
    
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String(50))
    content = Column(Text)
    content_img = Column(Text)
    category_id =Column(Integer, ForeignKey("categories.id"))
    church_id =Column(Integer, ForeignKey("churchs.id"))
    waktu_mulai = Column(Time)
    tanggal_mulai = Column(Date)
    pendeta_id = Column('pendeta_id',Integer(),ForeignKey("pendetas.id") )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
    pendeta = relationship("Pendeta", back_populates="jadwals")
    church = relationship("Church", back_populates="jadwals")
    category = relationship("Category", back_populates="jadwals")
