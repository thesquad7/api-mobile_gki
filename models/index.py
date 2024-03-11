from sqlalchemy import Table,Column,Boolean,Integer,String,Text,Date, Time,ForeignKey
from config.db import Base
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))

    acaras = relationship("Acara", back_populates="category")

class Church(Base):
    __tablename__ = 'churchs'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    content_img = Column(Text)
    churchvisitors = relationship("ChurchVisitor", back_populates="church")

class Pendeta(Base):
    __tablename__ = 'pendetas'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    status = Column(Text)
    profile_img = Column(Text)
    jadwals = relationship("Jadwal", back_populates="pendeta")

class Acara(Base):
    __tablename__ = 'acaras'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    status = Column(Text)
    content_img = Column(Text)
    content = Column(Text)
    category_id =Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="acaras")

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

    church = relationship("Church", back_populates="churchvisitors")

class Feedback(Base):
    __tablename__ = 'feeds'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    content = Column(Text)
    content_img = Column(Text)

class Jadwal(Base):
    __tablename__ = 'jadwals'
    
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String(50))
    content = Column(Text)
    content_img = Column(Text)
    waktu_mulai = Column(Time)
    tanggal_mulai = Column(Date)
    pendeta_id = Column(Integer,ForeignKey("pendetas.id") )

    pendeta = relationship("Pendeta", back_populates="jadwals")

class Kesaksian(Base):
    __tablename__ = 'kesaksians'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    status = Column(Text)
    content_img = Column(Text)
    user_id = Column(String(12))

class MoneyBank(Base):
    __tablename__ = 'moneybanks'
    
    id = Column(Integer,primary_key=True, index=True)
    from_inv = Column(String(50))
    total = Column(Integer)

class Money(Base):
    __tablename__ = 'money_moons'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    code = Column(Integer)
    total = Column(Integer)

class Office(Base):
    __tablename__ = 'offices'
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50))
    start = Column(Time)
    end = Column(Time)
    status = Column(Boolean)

class User(Base):
    __tablename__= 'users'

    id = Column(Integer,primary_key=True, index=True)
    username = Column(String(50), unique=True)
    user_img = Column(Text)
    name = Column(String(60))
    password = Column(String(255))



