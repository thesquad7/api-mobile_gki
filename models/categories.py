from sqlalchemy import Column, ForeignKey, Integer, String, Text, Time,Date
from config.db import Base
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    acaras = relationship("Acara", back_populates="category")


