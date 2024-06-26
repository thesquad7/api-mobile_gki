from datetime import datetime, timezone
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Time,Boolean
from config.db import Base
from sqlalchemy.orm import relationship

class ChurchVisitor(Base):
    __tablename__ = 'churchvisitors'
    
    id = Column(Integer,primary_key=True, index=True)
    jadwal_id = Column(Integer, ForeignKey("jadwals.id"))
    w_jemaat = Column(Integer)
    p_jemaat = Column(Integer)
    w_visit = Column(Integer)
    p_visit =Column(Integer)
    stream = Column(Boolean)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
    stream_count = Column(Integer, nullable=True)
    jadwals = relationship("Jadwal", back_populates="visit",uselist=False)
