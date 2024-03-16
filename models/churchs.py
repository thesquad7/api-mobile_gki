from sqlalchemy import Column,Integer, String, Text
from config.db import Base
from sqlalchemy.orm import relationship
class Church(Base):
    __tablename__ = 'churchs'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    content_img = Column(Text)
    visit = relationship("ChurchVisitor", back_populates="church")