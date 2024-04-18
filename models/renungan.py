from datetime import datetime,timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Time,Date
from config.db import Base
from sqlalchemy.orm import relationship

class Renungan(Base):
    __tablename__ = 'renungans'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(Text)
    content_img = Column(Text)
    content = Column(Text)
    tanggal = Column(Date)
    category_id =Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="renungan")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
