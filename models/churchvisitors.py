from sqlalchemy import Column, ForeignKey, Integer, Time,Boolean
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
    jemaat_t = Column(Time)
    visit_t = Column(Time)
    stream = Column(Boolean)

    church = relationship("Church", back_populates="visit")
