#encoding: utf-8
'''
Created on Aug 15, 2009

@author: santiago
'''

import sys
from datetime import datetime, date

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import cast
from sqlalchemy import create_engine, Date
from sqlalchemy.orm import sessionmaker

from dolardo import DEBUG, parse_moneda_list, brou, sql_connection
from dolardo.entities import Base
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

        db_engine = create_engine(sql_connection)
        db_session = sessionmaker(bind=db_engine)
        Base.metadata.create_all(db_engine)

        for nombre_moneda in parse_moneda_list:
            session = db_session()

            try:
                if nombre_moneda in cotizaciones:
                    (buy, sell) = cotizaciones[nombre_moneda]
                    
                    if DEBUG:
                        print "Cotización %s: %s / %s." % (nombre_moneda, buy, sell)               
    
                    try:
                        monedas = session.query(Moneda).filter(Moneda.nombre == nombre_moneda).all()
        
                        if not monedas:
                            if DEBUG:
                                print "No hay moneda para la cotizacion de %s, creo la moneda y la cotización." % nombre_moneda
                            
                            moneda = Moneda(nombre_moneda)
                            session.add(moneda)
                            
                            cotizacion = Cotizacion(datetime.now(), buy, sell)
                            cotizacion.moneda = moneda
                            session.add(cotizacion)
                        else:
                            moneda = monedas[0]
                        
                            resultado = session.query(Cotizacion).filter(cast(Cotizacion.fecha, Date) == date.today()).filter(Cotizacion.moneda_id == moneda.moneda_id).all()
                            
                            if not resultado:
                                if DEBUG:
                                    print "No hay cotizacion del dia de %s, creo una nueva cotización." % nombre_moneda
                                cotizacion = Cotizacion(datetime.now(), buy, sell)
                                cotizacion.moneda = moneda
                                session.add(cotizacion)
                            else:
                                cotizacion = resultado[0]
                                if cotizacion.compra != buy or cotizacion.venta != sell:
                                    if DEBUG:
                                        print "Se encontró la cotización de %s, cambió la cotizacion del dia." % nombre_moneda
                                    cotizacion.compra = buy
                                    cotizacion.venta = sell
                                    cotizacion.fecha = datetime.now()
                                    session.add(cotizacion)                    
                                else:
                                    if DEBUG:
                                        print "Se encontró la cotización de %s, pero no cambió la cotizacion del dia." % nombre_moneda
                    except:
                        raise
                else:
                    error_reporting.report("Error leyendo la cotización de la moneda %s." % nombre_moneda)
        
                session.commit()
            except:
                session.rollback()
                raise                
    except:
        info = sys.exc_info()
        error_reporting.report_error(info)
        print info
    
