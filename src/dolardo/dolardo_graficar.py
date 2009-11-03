#encoding: utf-8
'''
Created on Aug 15, 2009

@author: santiago
'''

import sys
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dolardo import brou, Base, DEBUG, sql_connection, grafico_colores
from dolardo.entities.cotizacion import Cotizacion
from dolardo.entities.moneda import Moneda
from dolardo import error_reporting

from pygooglechart.pygooglechart import Chart
from pygooglechart.pygooglechart import XYLineChart
from pygooglechart.pygooglechart import Axis
from pygooglechart.pygooglechart import SimpleLineChart

def graficar_cotizaciones(monedas_id, dias, height, width):
    # Represento 30 días en la gráfica. 
    rango = timedelta(dias)
    
    fin_rango = datetime.now()
    inicio_rango = fin_rango - rango
    
    db_engine = create_engine(sql_connection)
    db_session = sessionmaker(bind=db_engine)
    
    Base.metadata.create_all(db_engine)
    
    session = db_session()
    try:
        if DEBUG:
            print "Leyendo cotizaciones..."
            print "Inicio: %s" % inicio_rango
            print "Fin: %s" % fin_rango
        
        rango_cotizaciones = []
        
        monedas = session.query(Moneda).all()
        
        for moneda in monedas:
            if (moneda.moneda_id in monedas_id):
                un_rango_cotizaciones = session.query(Cotizacion). \
                    filter(Cotizacion.moneda_id == moneda.moneda_id). \
                    filter(Cotizacion.fecha <= fin_rango). \
                    filter(Cotizacion.fecha >= inicio_rango). \
                    order_by(Cotizacion.fecha).all()
    
                if DEBUG:
                    print "Rango: %s" % un_rango_cotizaciones
                    
                rango_cotizaciones.append((moneda, un_rango_cotizaciones))        
    
        session.commit()
    except:
        info = sys.exc_info()
        error_reporting.report_error(info)
        print info

        session.rollback()
        raise
    
    try:
        url = generar_grafica(inicio_rango, fin_rango, rango_cotizaciones, height, width)
    except:
        info = sys.exc_info()
        error_reporting.report_error(info)
        print info
        
        url = ""
           
    return (rango_cotizaciones, url, monedas)
        
def split_compra_venta(cotizaciones):
    '''
    Dado una lista de cotizaciones retorna 3 listas:
    Una con las fechas de estas cotizaciones, otra con las cotizaciones de compra
    y otras con las cotizaciones de venta.
    '''
    def get_buy(c): return float(c.compra)
    cotizaciones_buy = map(get_buy, cotizaciones) 
    
    def get_sell(c): return float(c.venta)
    cotizaciones_sell = map(get_sell, cotizaciones)
    
    def fechas(c): return c.fecha
    cotizaciones_fechas = map(fechas, cotizaciones)
    
    return (cotizaciones_fechas, cotizaciones_buy, cotizaciones_sell)
        
def generar_grafica(inicio, fin, cotizaciones, height, width):
    # Formato de fechas.
    formato_fecha_humano = "%d/%m/%Y"
    formato_fecha_axis = "%y%m%d"

    # Máximo valor de todas las cotizaciones.
    max_cotizaciones = 0    
    # Mínimo valor de todas las cotizaciones.
    min_cotizaciones = sys.maxint
    # Mayor cantidad de cotizaciones entre todas las monedas.
    max_count_cotizaciones = 0
    # Mayor rango de fechas entre todas las monedas.
    rango_fechas = []
    
    # Colección de cotizaciones pocesadas.
    cotizaciones_procesadas = []
    for cotizacion in cotizaciones:
        (moneda, rango_cotizaciones) = cotizacion
        (cotizaciones_fechas, cotizaciones_buy, cotizaciones_sell) = split_compra_venta(rango_cotizaciones)

        max_cotizaciones = max(max_cotizaciones, max(max(cotizaciones_buy), max(cotizaciones_sell)))
        min_cotizaciones = min(min_cotizaciones, min(min(cotizaciones_buy), min(cotizaciones_sell)))
        max_count_cotizaciones = max(max_count_cotizaciones, len(cotizacion))
        
        if len(cotizaciones_fechas) > len(rango_fechas):
            rango_fechas = cotizaciones_fechas
        
        cotizaciones_procesadas.append((moneda, rango_cotizaciones, cotizaciones_fechas, cotizaciones_buy, cotizaciones_sell))
 
    if DEBUG:
        print int(min_cotizaciones)-1
        print int(max_cotizaciones)+1

    # Proceso el eje X con las fechas.
    rango_fechas_axis = []
    rango_fechas_humano = []
    for fecha in rango_fechas:
        rango_fechas_axis.append(int(fecha.strftime(formato_fecha_axis)))
        
        if len(rango_fechas) >= 5:
            if len(rango_fechas_axis) % (len(rango_fechas)/5) == 0:
                rango_fechas_humano.append(fecha.strftime(formato_fecha_humano))
            else:
                rango_fechas_humano.append('')
        else:
            rango_fechas_humano.append(fecha.strftime(formato_fecha_humano))

    chart = SimpleLineChart(height, width, y_range=(int(min_cotizaciones)-1, int(max_cotizaciones)+1))

    # Normalizo las cotizaciones (si hay monedas con mas cantidad de valores que otras les agrego valores vacios)
    cotizaciones_normalizadas = []
    for cotizacion_procesada in cotizaciones_procesadas:
        (moneda, rango_cotizaciones, cotizaciones_fechas, cotizaciones_buy, cotizaciones_sell) = cotizacion_procesada
        
        if len(cotizaciones_fechas) < len(rango_fechas):
            for item in range(0, len(rango_fechas) - len(cotizaciones_fechas)):
                cotizaciones_buy.insert(0, None)
                cotizaciones_sell.insert(0, None)
                
        cotizaciones_normalizadas.append((moneda, rango_cotizaciones, cotizaciones_fechas, cotizaciones_buy, cotizaciones_sell))

    leyendas = []

    # Genero los datos necesario para
    for cotizacion_normalizada in cotizaciones_normalizadas:
        (moneda, rango_cotizaciones, cotizaciones_fechas, cotizaciones_buy, cotizaciones_sell) = cotizacion_normalizada
        
        x_compra = []
        y_compra = []
        x_venta = []
        y_venta = []
                
        for index in range(0, len(rango_fechas_axis)):
            cotizacion_buy = cotizaciones_buy[index]
            cotizacion_sell = cotizaciones_sell[index]
            fecha_axis = rango_fechas_axis[index]
            
            x_compra.append(index)
            y_compra.append(cotizacion_buy)
            
            x_venta.append(fecha_axis)
            y_venta.append(cotizacion_sell)

        if DEBUG:
            print x_compra
            print y_compra

        y_compra_index = chart.add_data(y_compra)
        y_venta_index = chart.add_data(y_venta)

        leyendas.append(str(moneda.nombre) + ' compra')
        leyendas.append(str(moneda.nombre) + ' venta')
        
    # Y axis labels
    left_axis = range(int(min_cotizaciones)-1, int(max_cotizaciones)+1+1, 1)
    left_axis[0] = ''
    left_axis_index = chart.set_axis_labels(Axis.LEFT, left_axis)

    # X axis labels
    bottom_axis_index = chart.set_axis_labels(Axis.BOTTOM, rango_fechas_humano)
    
    # Set the line legends.
    chart.set_legend(leyendas)

    # Set the line colours
    chart.set_colours(grafico_colores)
    
    # Set the vertical stripes
    chart.fill_linear_stripes(Chart.CHART, 0, 'CCCCCC', 0.1, 'FFFFFF', 0.1)

    # Set the horizontal dotted lines
    chart.set_grid(0, 25, 5, 5)    
   
    if DEBUG:
        chart.download('cotizacion.png')

    return chart.get_url()
    
