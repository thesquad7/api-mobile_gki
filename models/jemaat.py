from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, ForeignKey,Column,Integer, String, Text,DATE
from config.db import Base
class Jemaats(Base):
    __tablename__= 'jemaats'

    id = Column(Integer,primary_key=True, index=True)
    jemaat_id= Column(String(80))
    jemaat_img= Column(Text)
    pendeta_id=Column(Integer, ForeignKey("pendetas.id"))
    name = Column(String(50))
    tempat_lahir = Column(String(100))
    tanggal_lahir = Column(DATE)
    nama_bapak = Column(String(80))
    nama_ibu = Column(String(80))
    nama_baptis= Column(String(80))
    alamat = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
    pendeta = relationship("Pendeta", back_populates="jemaats")

