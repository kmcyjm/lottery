from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

with open('./lottery/data/config.json') as configfile:
    data = json.load(configfile)
    connection_string = 'mysql+pymysql://' + data['username'] + ':' + data['password'] + '@' + data['host'] + ':' + data['port'] + '/lottery'

engine = create_engine(connection_string, echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()
