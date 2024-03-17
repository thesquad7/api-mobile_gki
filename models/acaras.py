from sqlalchemy import Column, ForeignKey, Integer, String, Text, Time,Date
from config.db import Base
from sqlalchemy.orm import relationship

class Acara(Base):
    __tablename__ = 'acaras'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    status = Column(Text)
    content_img = Column(Text)
    content = Column(Text)
    tanggal = Column(Date)
    category_id =Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="acaras")
