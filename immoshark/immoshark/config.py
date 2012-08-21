'''
Created on Aug 21, 2012

@author: zking
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

##################################################################################
# HTTP
##################################################################################
http_request_retries = 3
http_request_sleep = 0.5


##################################################################################
# DATABASE
##################################################################################
db_base = declarative_base()
db_engine = create_engine('sqlite:///:memory:', echo=True)
db_session = sessionmaker(bind=db_engine)
db_base.metadata.create_all(db_engine)