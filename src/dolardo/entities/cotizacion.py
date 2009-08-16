'''
Created on Aug 15, 2009

@author: santiago
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relation, backref

from dolardo import Base
from dolardo.entities.moneda import Moneda

class Cotizacion(Base):

    __tablename__ = 'cotizaciones' 

    cotizacion_id = Column(Integer, primary_key=True)
    
    moneda_id = Column(Integer, ForeignKey(Moneda.moneda_id), nullable=False)
    moneda = relation(Moneda)
    
    fecha = Column(DateTime, nullable=False, unique=True)
    compra = Column(Numeric, nullable=True)
    venta = Column(Numeric, nullable=False)

    def __init__(self, fecha, compra, venta):
        #self.moneda_id = moneda_id
        self.fecha = fecha
        self.compra = compra
        self.venta = venta
       
    def __repr__(self):
        return "<Cotizacion(%s, %s, %s)>" % (self.fecha, self.compra, self.venta)
    
    def __unicode__(self):
        return 
        