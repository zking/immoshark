'''
Created on Aug 21, 2012

@author: zking
'''
from sqlalchemy import Column, Integer, String, DateTime
from immoshark import config
from datetime import datetime


class RealEstateObject(config.db_base):
    '''
    Real Estate Object
    '''
    
    __tablename__ = 'object'
    __mapper_args__ = {'column_prefix': __tablename__+'_'}
    
    ##############################################################################
    # COLUMNS
    ##############################################################################
    id =            Column(String(255), primary_key=True)
    url =           Column(String(1024))
    affiliate =     Column(String(255), primary_key=True)
    created =       Column(DateTime)
    updated =       Column(DateTime, default=datetime.now())
    
    
    def __repr__(self):
        return "<RealEstateObject('%s', '%s')>" % (self.id, self.affiliate)
    
