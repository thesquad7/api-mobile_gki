from sqlalchemy import create_engine,MetaData

engine = create_engine('mysql+pymysql://root@localhost:3306/m_gki_data')
meta= MetaData()
con=engine.connect()