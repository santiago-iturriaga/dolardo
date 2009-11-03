#coding: utf-8
'''
Created on Aug 15, 2009

@author: santiago
'''

DEBUG = True

sql_connection = "mysql://santiag0_santiag:santiag0@localhost/santiag0_dolardo"

url_brou = "http://www.portal.brou.com.uy/web/guest/institucional/cotizaciones"
parse_moneda_list = (u'Dólar',u'Peso Argentino',u'Real',u'Euro')


url_brou = "http://www.portal.brou.com.uy/web/guest/institucional/cotizaciones"
parse_moneda_list = (u'Dólar',u'Peso Argentino',u'Real',u'Euro')

grafico_default_monedas = '1'
grafico_default_days = 30
grafico_default_height = 700
grafico_default_width = 400
grafico_colores = ['0000FF','00FF00','FF0000','770000','007700','000077','7700FF','77FF77']
grafico_dias = [(30,'30 días'),(60,'60 días'),(120,'120 días')]

log_file = 'dolardo.log'

smtp_enabled = False
smpt_host = 'mail.ituland.com'
smpt_port = 26
smpt_user = 'santiago+ituland.com'
smpt_password = 'kadath1'
smpt_from = 'santiago@ituland.com'
smpt_to = ['santiago@ituland.com']
smpt_subject = "[Dolardo]"

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
