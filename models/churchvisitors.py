from sqlalchemy import Column, Date, ForeignKey, Integer, Time,Boolean
from config.db import Base
from sqlalchemy.orm import relationship

class ChurchVisitor(Base):
    __tablename__ = 'churchvisitors'
    
    id = Column(Integer,primary_key=True, index=True)
    church_id = Column(Integer, ForeignKey("churchs.id"))
    w_jemaat = Column(Integer)
    p_jemaat = Column(Integer)
    w_visit = Column(Integer)
    p_visit =Column(Integer)
    jemaat_t = Column(Date)
    stream = Column(Boolean)
    stream_count = Column(Integer)
    church = relationship("Church", back_populates="visit")
