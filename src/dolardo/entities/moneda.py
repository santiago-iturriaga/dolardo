'''
Created on Aug 15, 2009

@author: santiago
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import relation, backref

from dolardo import Base

class Moneda(Base):

    __tablename__ = 'monedas'

    moneda_id = Column(Integer, primary_key=True)
    nombre = Column(String)

    def __init__(self, nombre):
        self.nombre = nombre
        
    def __repr__(self):
        return "<Moneda(%s,%s)>" % (self.moneda_id, self.nombre)
    
    def __unicode__(self):
        return nombre
        