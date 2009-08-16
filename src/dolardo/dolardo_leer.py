#encoding: utf-8
'''
Created on Aug 15, 2009

@author: santiago
'''

import sys
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dolardo import DEBUG, nombre_moneda, brou, Base, sql_connection
from dolardo.entities.cotizacion import Cotizacion
from dolardo.entities.moneda import Moneda
from dolardo import error_reporting

def leer_cotizaciones():
    try:
        if DEBUG:
            print "Iniciando..."
            
        cotizaciones = brou.leer_cotizaciones()

        if DEBUG:
            print "Cotizaciones leidas."
        
        if nombre_moneda in cotizaciones:
            (buy, sell) = cotizaciones[nombre_moneda]
            
            if DEBUG:
                print "Cotización: %s / %s." % (buy, sell)
            
            print "1"
            db_engine = create_engine(sql_connection)
            print "2"
            db_session = sessionmaker(bind=db_engine)
            print "3"
            Base.metadata.create_all(db_engine)        
            print "4"
            session = db_session()
            try:
                print "5"
                monedas = session.query(Moneda).filter(Moneda.nombre == nombre_moneda).all()
                print "6"
                if not monedas:
                    moneda = Moneda(nombre_moneda)
                    session.add(moneda)
                else:
                    moneda = monedas[0]
                    
                cotizacion = Cotizacion(datetime.now(), buy, sell)
                cotizacion.moneda = moneda
                session.add(cotizacion)
                
                session.commit()
                error_reporting("Lectura de cotizacion: OK!.")
            except:
                session.rollback()
                raise
        else:
            print 'Error leyendo la cotización.'            
            
    except:
        info = sys.exc_info()
        error_reporting.report_error(info)
        print info
    