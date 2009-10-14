'''
Created on Oct 13, 2009

@author: santiago
'''

from bottle.bottle import route, template, redirect

IMAGEN_SUBE = '/images/up_64.png'
IMAGEN_BAJA = '/images/down_64.png'
IMAGEN_IGUAL = '/images/left_64.png'
DEBUG_HTML = "<div style='text-align:right; font-size:x-small; color: #777777;'>[ Modo DEBUG ]</div>" 

from dolardo import url_brou, DEBUG
from dolardo import dolardo_graficar

default_days = 30
default_height = 700
default_width = 400

@route('/')
def index():
    redirect("/default")

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
        
    cotizaciones = dolardo_graficar.graficar_cotizaciones(int_dias, int_height, int_width)
    
    if DEBUG:
        print cotizaciones

    (fecha_inicio, fecha_fin, url_grafica, compra, venta, delta) = cotizaciones
           
    if DEBUG:
        debug_html = DEBUG_HTML
    else:
        debug_html = ""
        
    if delta > 0:
        imagen_cotizacion = IMAGEN_SUBE
    elif delta < 0:
        imagen_cotizacion = IMAGEN_BAJA
    else:
        imagen_cotizacion = IMAGEN_IGUAL
    
    return template('index.html', 
                    url_brou=url_brou,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    grafico=url_grafica,
                    compra=compra,
                    venta=venta,
                    variacion=delta,
                    img_variacion=imagen_cotizacion,
                    debug=debug_html)
