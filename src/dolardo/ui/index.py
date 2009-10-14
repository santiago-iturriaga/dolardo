'''
Created on Oct 13, 2009

@author: santiago
'''

from bottle.bottle import route, template

IMAGEN_SUBE = 'images/up_64.png'
IMAGEN_BAJA = 'images/down_64.png'
IMAGEN_IGUAL = 'images/left_64.png'
DEBUG_HTML = "<div style='text-align:right; font-size:x-small; color: #777777;'>[ Modo DEBUG ]</div>" 

from dolardo import url_brou, DEBUG
from dolardo import dolardo_graficar

@route('/')
def index():
    cotizaciones = dolardo_graficar.graficar_cotizaciones()
    
    if DEBUG:
        print cotizaciones

    (fecha_inicio, fecha_fin, url_grafica, compra, venta, delta) = cotizaciones
    
    #template_handle = open(TEMPLATE_FILE,'r')
    #template = template_handle.read()
    #template_handle.close()
        
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
