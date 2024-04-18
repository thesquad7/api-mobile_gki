from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DB Setting
db_mode = "mysql"
db_driver = "pymysql"
user="root"
password=""
db_originAddress= "localhost"
port="3306"
db_name="m_gki_data"
# =====================================

# jangan merubah variabel "db_address" dan isinya.
db_address = f"{db_mode}+{db_driver}://{user}:{password}@{db_originAddress}:{port}/{db_name}"
#=============================================================================================
engine = create_engine(db_address)

LocalSession = sessionmaker(autocommit= False, autoflush=False, bind=engine)

Base=declarative_base() 

con=engine.connect()