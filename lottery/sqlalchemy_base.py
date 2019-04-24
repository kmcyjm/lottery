from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://eason:ouN]jol3@34.252.90.15:3306/lottery', echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()
