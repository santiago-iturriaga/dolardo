#encoding: utf-8
'''
Created on Oct 13, 2009

@author: santiago
'''

import sys

from datetime import datetime
from bottle.bottle import route, template, redirect

IMAGEN_SUBE = '/images/up_64.png'
IMAGEN_BAJA = '/images/down_64.png'
IMAGEN_IGUAL = '/images/left_64.png'
DEBUG_HTML = '<div style="text-align:right; font-size:x-small; color: #777777;">[ Modo DEBUG ]</div>' 

from dolardo import url_brou, DEBUG, grafico_default_monedas, grafico_default_days, \
                    grafico_default_height, grafico_default_width, grafico_colores, \
                    grafico_dias
from dolardo import dolardo_graficar
from dolardo.error_reporting import report_error

class Dia:
    def __init__(self, url, descripcion):
        self.url = url
        self.descripcion = descripcion
        
class Moneda:
    def __init__(self, url, nombre):
        self.url = url
        self.nombre = nombre

@route('/')
def index():
    redirect('/default/')

@route('/default/')
def default():
    return custom(grafico_default_monedas, grafico_default_height, \
                  grafico_default_width, grafico_default_days)

@route('/custom/:monedas/')
def custom(monedas):
    return custom(grafico_default_monedas, grafico_default_height, \
                  grafico_default_width, grafico_default_days)

@route('/custom/:monedas/:height/:width/')
def custom(height, width):
    return custom(grafico_default_monedas, height, width, default_days)

@route('/custom/:monedas/:dias/')
def custom(dias):
    return custom(grafico_default_monedas, default_height, default_width, \
                  dias)
   
@route('/custom/:monedas/:height/:width/:dias/')
def custom(monedas, height, width, dias):
    # Obtengo los parametros de visualización.
    (int_dias, int_height, int_width, int_monedas) = parse_input(monedas, height, width, dias)
                
    try:  
        # Generación de la gráfica.
        cotizaciones = dolardo_graficar.graficar_cotizaciones(int_monedas, int_dias, int_height, int_width)
        
        if DEBUG:
            print cotizaciones
    
        (rango_cotizaciones, url_grafica, db_monedas) = cotizaciones
               
        if len(rango_cotizaciones) > 0:   
            # Primer y ultima fecha de la lista de cotizaciones.
            fecha_inicio = datetime.now() #rango_cotizaciones[0].fecha
            fecha_fin = datetime.now() #rango_cotizaciones[-1].fecha
             
            # Ultima cotizacion de compra/venta.
            compra = '' #rango_cotizaciones[-1].compra
            venta = '' #rango_cotizaciones[-1].venta
            
            # Max. y min. cotizacion
            min_compra = '' #rango_cotizaciones[0].compra
            max_compra = '' #rango_cotizaciones[0].compra
            min_venta = '' #rango_cotizaciones[0].venta
            max_venta = '' #rango_cotizaciones[0].venta
            #for cotizacion in rango_cotizaciones:
            #    if cotizacion.compra > max_compra:
            #        max_compra = cotizacion.compra
            #    elif cotizacion.compra < min_compra:
            #        min_compra = cotizacion.compra
            #        
            #    if cotizacion.venta > max_venta:
            #        max_venta = cotizacion.venta
            #    elif cotizacion.venta < min_venta:
            #        min_venta = cotizacion.venta
                            
            # Variacion entre la ultima y penultima cotizacion.        
            if len(rango_cotizaciones) >= 2:
                delta = 0 #rango_cotizaciones[-1].compra - rango_cotizaciones[-2].compra
                delta_total = 0 #rango_cotizaciones[-1].compra - rango_cotizaciones[0].compra
            else:
                delta = 0
                delta_total = 0
                              
            if delta > 0:
                imagen_cotizacion = IMAGEN_SUBE
            elif delta < 0:
                imagen_cotizacion = IMAGEN_BAJA
            else:
                imagen_cotizacion = IMAGEN_IGUAL
            
            # Si no hay url de imagen muestro una imagen de error.
            if len(url_grafica) == 0:
                url_grafica = '/images/out-of-order.jpg'
            
            if DEBUG:
                debug_html = DEBUG_HTML
            else:
                debug_html = ""

            # Genero los links para mostrar en la página.
            (links_dias, links_monedas) = render_links(db_monedas, int_monedas, int_height, int_width, int_dias)
            
            # Genero el template HTML.
            return template('index.html', 
                            
                            url_brou=url_brou,
                            fecha_inicio=fecha_inicio.strftime('%d/%m/%Y'),
                            fecha_fin=fecha_fin.strftime('%d/%m/%Y'),
                            grafico=url_grafica,
                            
                            fecha=fecha_fin.strftime('%d/%m/%Y %H:%M'),
                            compra=compra,
                            venta=venta,
                            variacion=delta,
                            variacion_total=delta_total,
                            img_variacion=imagen_cotizacion,
                            max_compra=max_compra,
                            min_compra=min_compra,
                            max_venta=max_venta,
                            min_venta=min_venta,

                            links_dias=links_dias,
                            links_monedas=links_monedas,

                            debug=debug_html)
        else:
            redirect('/error')
    except:
        report_error(sys.exc_info())
        redirect('/error')
        
def parse_input(monedas, height, width, dias):
    int_dias = 0
    try:
        int_dias = int(dias)
    except:
        int_dias = default_days
        
    int_height = 0
    try:
        int_height = int(height)
    except:
        int_height = default_height
        
    int_width = 0
    try:
        int_width = int(width)
    except:
        int_width = default_width
        
    int_monedas = []
    for moneda in monedas.split('&'):
        try:
            int_monedas.append(int(moneda))
        except:
            if DEBUG:
                print "No fue posible converir a int la moneda %s" % moneda
                
    return (int_dias, int_height, int_width, int_monedas)

def render_links(list_dbmonedas, current_monedas, current_height, current_width, current_dias):
    url_link = '/custom/{monedas}/{height}/{width}/{dias}/'
    
    found_dias = False
    lista_dias = []
    for (cantidad, descripcion) in grafico_dias:
        if current_dias == cantidad:
            item_dia = Dia('', descripcion)
            item_dia.css = 'selected'
            lista_dias.append(item_dia)
            found_dias = True
        else:
            item_dia = Dia(url_link.format(monedas=reduce(lambda x,y: str(x) + '&' + str(y), current_monedas), \
                                           height=current_height, \
                                           width=current_width, \
                                           dias=cantidad), descripcion)
            item_dia.css = ''
            lista_dias.append(item_dia)
    
    item_custom_dia = Dia('', 'Custom')
    if found_dias: 
        item_custom_dia.css = ''
    else:
        item_custom_dia.css = 'selected' 
    lista_dias.insert(0, item_custom_dia)
    
    lista_monedas = []
    for dbmoneda in list_dbmonedas:
        if dbmoneda.moneda_id in current_monedas:
            if (len(current_monedas) == 1):
                item_moneda = Moneda('', dbmoneda.nombre)
            else:
                monedas_sin_current = [item for item in current_monedas if item != dbmoneda.moneda_id]
                monedas_sin_current_link = reduce(lambda x,y: str(x) + '&' + str(y), monedas_sin_current)
                
                item_moneda = Moneda(url_link.format(monedas=monedas_sin_current_link, \
                                                     height=current_height, \
                                                     width=current_width, \
                                                     dias=current_dias), dbmoneda.nombre)
            item_moneda.css = 'selected'
            lista_monedas.append(item_moneda)
        else:
            monedas_con_current = [item for item in current_monedas]
            monedas_con_current.append(dbmoneda.moneda_id)
            monedas_con_current_link = reduce(lambda x,y: str(x) + '&' + str(y), monedas_con_current)
            
            item_moneda = Moneda(url_link.format(monedas=monedas_con_current_link, \
                                                 height=current_height, \
                                                 width=current_width, \
                                                 dias=current_dias), dbmoneda.nombre)
            item_moneda.css = ''
            lista_monedas.append(item_moneda)
                
    return (lista_dias, lista_monedas)
