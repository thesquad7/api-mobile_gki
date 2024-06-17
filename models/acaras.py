from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Time,Date
from config.db import Base
from sqlalchemy.orm import relationship

class Acara(Base):
    __tablename__ = 'acaras'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    status = Column(Text)
    content_img = Column(Text)
    content = Column(Text)
    location = Column(Text)
    tanggal = Column(Date)
    jam_acara = Column(Time)
    category_id =Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
    category = relationship("Category", back_populates="acaras")
