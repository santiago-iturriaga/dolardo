#!/usr/bin/python
'''
Created on Aug 16, 2009

@author: santiago
'''

import os
import sys
import cgi
import cgitb

cgitb.enable()

LIB_PATH = ".."
BASE_PATH = "../dolardo"
TEMPLATE_FILE = '../dolardo_html.template'
IMAGEN_SUBE = '../images/basic/up_64.png'
IMAGEN_BAJA = '../images/basic/down_64.png'
IMAGEN_IGUAL = '../images/basic/left_64.png'
DEBUG_HTML = "<div style='text-align:right; font-size:x-small; color: #777777;'>[ Modo DEBUG ]</div>" 

current_path = "/home/santiag0/www/dolardo.ituland.com/cgi-bin"
sys.path.append(os.path.join(current_path, LIB_PATH))
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/MySQL_python-1.2.3c1-py2.4-linux-i686.egg')
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/setuptools-0.6c6-py2.4.egg')
os.chdir(os.path.join(current_path, BASE_PATH))

#print sys.path

from dolardo import url_brou, DEBUG
from dolardo import dolardo_graficar

def main():
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers

    cotizaciones = dolardo_graficar.graficar_cotizaciones()
    
    if DEBUG:
    	print cotizaciones

    (fecha_inicio, fecha_fin, url_grafica, compra, venta, delta) = cotizaciones
    
    template_handle = open(TEMPLATE_FILE,'r')
    template = template_handle.read()
    template_handle.close()
        
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
        
    print template % (fecha_inicio, fecha_fin, url_brou, url_grafica, compra, venta, imagen_cotizacion, debug_html)
        
main()