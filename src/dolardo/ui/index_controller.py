#encoding: utf-8

'''
Created on Dec 23, 2009

@author: santiago
'''

import sys
import cgi

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
from dolardo.error_reporting import report_error, write_log

class Dia:
    def __init__(self, url, descripcion):
        self.url = url
        self.descripcion = descripcion
        
class Moneda:
    def __init__(self, url, nombre):
        self.url = url
        self.nombre = nombre

class MonedaCotizacion:
    def __init__(self):
        pass
    
def index():
    redirect('/default/')

def default():
    return custom(grafico_default_monedas, grafico_default_height, \
                  grafico_default_width, grafico_default_days)

def custom_monedas(monedas):
    return custom(grafico_default_monedas, grafico_default_height, \
                  grafico_default_width, grafico_default_days)

def custom_size(height, width):
    return custom(grafico_default_monedas, height, width, default_days)

def custom_lapso(dias):
    return custom(grafico_default_monedas, default_height, default_width, \
                  dias)
   
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
            monedas_cotizaciones = []
            fecha_inicio = datetime.now() 
            fecha_fin = datetime.now()
            
            for (moneda, rango_cotizacion) in rango_cotizaciones:
                moneda_cotizacion = MonedaCotizacion()
                moneda_cotizacion.nombre_moneda = escape_html(moneda.nombre)
                
                if len(rango_cotizacion) > 0:
                    # Primer y ultima fecha de la lista de cotizaciones.
                    moneda_cotizacion.fecha_inicio = rango_cotizacion[0].fecha
                    moneda_cotizacion.fecha_fin = rango_cotizacion[-1].fecha
                    
                    fecha_inicio = min(moneda_cotizacion.fecha_inicio, fecha_inicio)
                     
                    # Ultima cotizacion de compra/venta.
                    moneda_cotizacion.compra = rango_cotizacion[-1].compra
                    moneda_cotizacion.venta = rango_cotizacion[-1].venta
                    
                    # Max. y min. cotizacion
                    min_compra = rango_cotizacion[0].compra
                    max_compra = rango_cotizacion[0].compra
                    min_venta = rango_cotizacion[0].venta
                    max_venta = rango_cotizacion[0].venta
                    for cotizacion in rango_cotizacion:
                        if cotizacion.compra > max_compra:
                            max_compra = cotizacion.compra
                        elif cotizacion.compra < min_compra:
                            min_compra = cotizacion.compra
                            
                        if cotizacion.venta > max_venta:
                            max_venta = cotizacion.venta
                        elif cotizacion.venta < min_venta:
                            min_venta = cotizacion.venta
                               
                    moneda_cotizacion.min_compra = min_compra
                    moneda_cotizacion.max_compra = max_compra
                    moneda_cotizacion.min_venta = min_venta
                    moneda_cotizacion.max_venta = max_venta
                                   
                    # Variacion entre la ultima y penultima cotizacion.        
                    if len(rango_cotizacion) >= 2:
                        moneda_cotizacion.delta = rango_cotizacion[-1].compra - rango_cotizacion[-2].compra
                        moneda_cotizacion.delta_total = rango_cotizacion[-1].compra - rango_cotizacion[0].compra
                    else:
                        moneda_cotizacion.delta = 0
                        moneda_cotizacion.delta_total = 0
                                      
                    if moneda_cotizacion.delta > 0:
                        moneda_cotizacion.imagen_cotizacion = IMAGEN_SUBE
                    elif moneda_cotizacion.delta < 0:
                        moneda_cotizacion.imagen_cotizacion = IMAGEN_BAJA
                    else:
                        moneda_cotizacion.imagen_cotizacion = IMAGEN_IGUAL
                
                    if DEBUG: write_log("Formateando fecha...")
                    moneda_cotizacion.fecha = moneda_cotizacion.fecha_fin.strftime('%d/%m/%Y %H:%M')
                    monedas_cotizaciones.append(moneda_cotizacion)
            
            # Si no hay url de imagen muestro una imagen de error.
            if len(url_grafica) == 0:
                url_grafica = '/images/out-of-order.jpg'
            
            if DEBUG:
                debug_html = DEBUG_HTML
            else:
                debug_html = ""

            if DEBUG: write_log("Generando links")

            # Genero los links para mostrar en la página.
            (links_dias, links_monedas) = render_links(db_monedas, int_monedas, int_height, int_width, int_dias)
    
            if DEBUG: write_log("Todo OK. Genero el template.")
        
            # Genero el template HTML.
            return template('index.html', 
                            
                            url_brou = url_brou,
                            fecha_inicio = fecha_inicio.strftime('%d/%m/%Y'),
                            fecha_fin = fecha_fin.strftime('%d/%m/%Y'),
                            grafico = url_grafica,

                            monedas_cotizaciones = monedas_cotizaciones,

                            links_dias = links_dias,
                            links_monedas = links_monedas,

                            debug = debug_html)
        else:
            redirect('/error')
    except:
        report_error(sys.exc_info())
        redirect('/error')
    
def escape_html(input):
    if (type(input) == unicode):
        return cgi.escape(input).encode('ascii', 'xmlcharrefreplace')
    else:
        return cgi.escape(input)
        
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
    #url_link = '/custom/{monedas}/{height}/{width}/{dias}/'
    url_link = '/custom/%(monedas)s/%(height)s/%(width)s/%(dias)s/'
    
    found_dias = False
    lista_dias = []
    for (cantidad, descripcion) in grafico_dias:
        if current_dias == cantidad:
            item_dia = Dia('', escape_html(descripcion))
            item_dia.css = 'selected'
            lista_dias.append(item_dia)
            found_dias = True
        else:
            item_dia = Dia(url_link % {'monedas':reduce(lambda x,y: str(x) + '&' + str(y), current_monedas), \
                                       'height':current_height, \
                                       'width':current_width, \
                                       'dias':cantidad}, escape_html(descripcion))
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
                item_moneda = Moneda('', escape_html(dbmoneda.nombre))
            else:
                monedas_sin_current = [item for item in current_monedas if item != dbmoneda.moneda_id]
                monedas_sin_current_link = reduce(lambda x,y: str(x) + '&' + str(y), monedas_sin_current)

                item_moneda = Moneda(url_link % {'monedas':monedas_sin_current_link, \
                                                'height':current_height, \
                                                'width':current_width, \
                                                'dias':current_dias}, escape_html(dbmoneda.nombre))                
            item_moneda.css = 'selected'
            lista_monedas.append(item_moneda)
        else:
            monedas_con_current = [item for item in current_monedas]
            monedas_con_current.append(dbmoneda.moneda_id)
            monedas_con_current_link = reduce(lambda x,y: str(x) + '&' + str(y), monedas_con_current)
            
            item_moneda = Moneda(url_link % {'monedas':monedas_con_current_link, \
                                            'height':current_height, \
                                            'width':current_width, \
                                            'dias':current_dias}, escape_html(dbmoneda.nombre))                
            item_moneda.css = ''
            lista_monedas.append(item_moneda)
                
    return (lista_dias, lista_monedas)
