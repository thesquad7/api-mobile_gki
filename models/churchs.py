from datetime import datetime, timezone
from sqlalchemy import Column, DateTime,Integer, String, Text
from config.db import Base
from sqlalchemy.orm import relationship
class Church(Base):
    __tablename__ = 'churchs'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    content_img = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
    visit = relationship("ChurchVisitor", back_populates="church")
    jadwals = relationship("Jadwal", back_populates="church")