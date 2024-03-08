from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_address = "mysql+pymysql://root:123@localhost:3306/m_gki_data"

engine = create_engine(db_address)

LocalSession = sessionmaker(autocommit= False, autoflush=False, bind=engine)

Base=declarative_base() 

con=engine.connect()