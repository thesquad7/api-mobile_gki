from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Time,Date
from config.db import Base
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    use_id = Column(String(50))
    color_id = Column(String(50))
    acaras = relationship("Acara", back_populates="category")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
    renungan = relationship("Renungan", back_populates="category")
    jadwals = relationship("Jadwal", back_populates="category")

