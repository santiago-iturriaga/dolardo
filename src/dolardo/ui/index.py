#encoding: utf-8
'''
Created on Oct 13, 2009

@author: santiago
'''

from bottle.bottle import route, template, redirect

IMAGEN_SUBE = '/images/up_64.png'
IMAGEN_BAJA = '/images/down_64.png'
IMAGEN_IGUAL = '/images/left_64.png'
DEBUG_HTML = '<div style="text-align:right; font-size:x-small; color: #777777;">[ Modo DEBUG ]</div>' 

from dolardo import url_brou, DEBUG
from dolardo import dolardo_graficar

default_days = 30
default_height = 700
default_width = 400

@route('/')
def index():
    redirect('/default')

@route('/default')
def default():
    return custom(default_height, default_width, default_days)

@route('/custom/:height/:width')
def custom(height, width):
    return custom(height, width, default_days)

@route('/custom/:dias')
def custom(dias):
    return custom(default_height, default_width, dias)

@route('/custom/:height/:width/:dias')
def custom(height, width, dias):
    selected30 = ''
    selected60 = ''
    selected120 = ''
    
    # Obtengo los parametros de visualización.
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

    if int_dias == 30:
        selected30 = 'selected'
    elif int_dias == 60:
        selected60 = 'selected'
    elif int_dias == 120:
        selected120 = 'selected'
        
    try:  
        # Generación de la gráfica.
        cotizaciones = dolardo_graficar.graficar_cotizaciones(int_dias, int_height, int_width)
        
        if DEBUG:
            print cotizaciones
    
        (rango_cotizaciones, url_grafica) = cotizaciones
               
        if len(rango_cotizaciones) > 0:   
            # Primer y ultima fecha de la lista de cotizaciones.
            fecha_inicio = rango_cotizaciones[0].fecha
            fecha_fin = rango_cotizaciones[-1].fecha
             
            # Ultima cotizacion de compra/venta.
            compra = rango_cotizaciones[-1].compra
            venta = rango_cotizaciones[-1].venta
            
            # Max. y min. cotizacion
            min_compra = rango_cotizaciones[0].compra
            max_compra = rango_cotizaciones[0].compra
            min_venta = rango_cotizaciones[0].venta
            max_venta = rango_cotizaciones[0].venta
            for cotizacion in rango_cotizaciones:
                if cotizacion.compra > max_compra:
                    max_compra = cotizacion.compra
                elif cotizacion.compra < min_compra:
                    min_compra = cotizacion.compra
                    
                if cotizacion.venta > max_venta:
                    max_venta = cotizacion.venta
                elif cotizacion.venta < min_venta:
                    min_venta = cotizacion.venta
                            
            # Variacion entre la ultima y penultima cotizacion.        
            if len(rango_cotizaciones) >= 2:
                delta = rango_cotizaciones[-1].compra - rango_cotizaciones[-2].compra
                delta_total = rango_cotizaciones[-1].compra - rango_cotizaciones[0].compra
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
                            
                            selected30=selected30,
                            selected60=selected60,
                            selected120=selected120,
                            debug=debug_html)
        else:
            redirect('/error')
    except:
        redirect('/error')
        