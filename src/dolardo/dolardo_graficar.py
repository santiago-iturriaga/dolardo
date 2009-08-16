#encoding: utf-8
'''
Created on Aug 15, 2009

@author: santiago
'''

import sys
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dolardo import brou, nombre_moneda, Base, DEBUG, sql_connection
from dolardo.entities.cotizacion import Cotizacion
from dolardo.entities.moneda import Moneda

from pygooglechart.pygooglechart import Chart
from pygooglechart.pygooglechart import XYLineChart
from pygooglechart.pygooglechart import Axis

def graficar_cotizaciones():
    # Represento 30 días en la gráfica. 
    rango = timedelta(30)
    
    fin_rango = datetime.now()
    inicio_rango = fin_rango - rango
    
    db_engine = create_engine(sql_connection)
    db_session = sessionmaker(bind=db_engine)
    
    #Base.metadata.create_all(db_engine)        
    
    session = db_session()
    try:
        if DEBUG:
            print "Leyendo cotizaciones..."
            print "Inicio: %s" % inicio_rango
            print "Fin: %s" % fin_rango
        
        moneda = session.query(Moneda).filter(Moneda.nombre == nombre_moneda).one()
        if not moneda:
            raise Exception('Error, no se encontró la moneda {0}.'.format(nombre_moneda))
        
        #if DEBUG:
        #    print "Moneda: %s (%s)" % (moneda.nombre, moneda.moneda_id)

        # Falta order by y unique fecha
        rango_cotizaciones = session.query(Cotizacion). \
            filter(Cotizacion.moneda_id == moneda.moneda_id). \
            filter(Cotizacion.fecha <= fin_rango). \
            filter(Cotizacion.fecha >= inicio_rango). \
            order_by(Cotizacion.fecha).all()

        if DEBUG:
            print "Rango: %s" % rango_cotizaciones        
    
        session.commit()
    except:
        info = sys.exc_info()
        error_reporting.report_error(info)
        print info
        
        session.rollback()
        
        raise
    
    url = generar_grafica(inicio_rango, fin_rango, rango_cotizaciones)
    
    if len(rango_cotizaciones) >= 2:
        delta = rango_cotizaciones[-1].compra - rango_cotizaciones[-2].compra
    else:
        delta = 0
        
    return (rango_cotizaciones[0].fecha.strftime("%d/%m/%Y"), rango_cotizaciones[-1].fecha.strftime("%d/%m/%Y"), 
            url, 
            rango_cotizaciones[-1].compra, rango_cotizaciones[-1].venta, delta)
        
def generar_grafica(inicio, fin, cotizaciones):
    formato_fecha_humano = "%d/%m/%Y"
    formato_fecha_axis = "%y%m%d"
    
    def get_buy(c): return c.compra
    cotizaciones_buy = map(get_buy, cotizaciones) 
    
    def get_sell(c): return c.venta
    cotizaciones_sell = map(get_sell, cotizaciones)
    
    def fechas(c): return int(c.fecha.strftime(formato_fecha_axis))
    cotizaciones_fechas = map(fechas, cotizaciones)
    
    max_cotizaciones_buy = max(cotizaciones_buy)
    max_cotizaciones_sell = max(cotizaciones_sell)
    max_cotizaciones = max(max_cotizaciones_buy, max_cotizaciones_sell)    
    
    chart = XYLineChart(700, 400,
                        x_range=(min(cotizaciones_fechas), max(cotizaciones_fechas)), 
                        y_range=(0, int(max_cotizaciones)+5))

    x_axis = []
    x = []
    y = []
    x2 = []
    y2 = []
    for cotizacion in cotizaciones:
        x.append(int(cotizacion.fecha.strftime(formato_fecha_axis)))
        y.append(float(cotizacion.compra))
        
        x2.append(int(cotizacion.fecha.strftime(formato_fecha_axis)))
        y2.append(float(cotizacion.venta))
        
        if len(cotizaciones_buy) >= 5:
            if len(x) % (len(cotizaciones_buy)/5) == 0:
                x_axis.append(cotizacion.fecha.strftime(formato_fecha_humano))
            else:
                x_axis.append('')
        else:
            x_axis.append(cotizacion.fecha.strftime(formato_fecha_humano))
    
    x_data_index = chart.add_data(x)
    y_data_index = chart.add_data(y)
    x2_data_index = chart.add_data(x2)
    y2_data_index = chart.add_data(y2)

    # Y axis labels
    left_axis = range(0, int(max_cotizaciones)+5, 5)
    left_axis[0] = ''
    left_axis_index = chart.set_axis_labels(Axis.LEFT, left_axis)
    
    # X axis labels
    bottom_axis_index = chart.set_axis_labels(Axis.BOTTOM, x_axis)
    
    titulo = "Cotización del Dólar entre %s y %s" % (cotizaciones[0].fecha.strftime(formato_fecha_humano), 
                                                     cotizaciones[-1].fecha.strftime(formato_fecha_humano))
    title_axis_index = chart.set_axis_labels(Axis.BOTTOM, [titulo])
    chart.set_axis_style(title_axis_index, '202020', font_size=10, alignment=0)
    chart.set_axis_positions(title_axis_index, [50])
  
    # Set the line colour to blue
    chart.set_colours(['0000FF', '00FF00'])

    # Set the vertical stripes
    chart.fill_linear_stripes(Chart.CHART, 0, 'CCCCCC', 0.1, 'FFFFFF', 0.1)

    # Set the horizontal dotted lines
    chart.set_grid(0, 25, 5, 5)
    
    chart.set_legend(['Compra', 'Venta'])
    
    if DEBUG:
        chart.download('cotizacion.png')
        
    return chart.get_url()
    
    