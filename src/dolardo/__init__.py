#coding: utf-8
'''
Created on Aug 15, 2009

@author: santiago
'''

DEBUG = False

url_brou = "brou-cotizaciones.html"
nombre_moneda = u'Dólar'

log_file = 'dolardo.log'
smpt_host = 'mail.ituland.com'
smpt_port = 26
smpt_user = 'santiago+ituland.com'
smpt_password = 'kadath1'
smpt_from = 'santiago@ituland.com'
smpt_to = ['santiago@ituland.com']
smpt_subject = "[Dolardo]"

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
