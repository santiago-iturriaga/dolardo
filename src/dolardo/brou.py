#coding: utf-8
'''
Created on Aug 15, 2009

@author: santiago
'''

import urllib
from decimal import Decimal
from HTMLParser import HTMLParser

from dolardo import url_brou, DEBUG

class BROUHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.tag_cotizaciones = False
       
        self.current_value = None
        self.currency = None
        self.buy = None
        self.sale = None

        self.cotizaciones = {}
    
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'table'.lower():
            for (id, value) in attrs:
                if id.lower() == 'title'.lower() and value.lower() == 'Cotizaciones'.lower():
                    self.tag_cotizaciones = True
        else:
            if self.tag_cotizaciones and tag.lower() == 'td'.lower():
                for (id, value) in attrs:
                    if id.lower() == 'class'.lower():
                        if value.lower() == 'currency'.lower():
                            self.tag_current = tag
                        if value.lower() == 'buy'.lower():
                            self.tag_current = tag
                        if value.lower() == 'sale'.lower():
                            self.tag_current = tag
                            
                        self.current_value = value.lower()
        
    def handle_endtag(self, tag):
        if self.tag_cotizaciones:
            if self.currency and self.buy and self.sale:
                self.cotizaciones[self.currency] = (self.buy, self.sale)
                self.currency = None
                self.buy = None
                self.sale = None
        
        if tag == 'table':
            self.tag_cotizaciones = False
        
    def handle_data(self, data):
        if self.tag_cotizaciones:
            if self.current_value == 'currency'.lower():
                if DEBUG:
                    print "Conviritendo DATA"
                value = data.strip().decode("utf-8", "ignore")
                
                if DEBUG:
                    #print "'%s'" % value
                    print data
                    
                if DEBUG:
                    print "Conviritendo DATA (listo)"    
                                
                self.currency = value
                self.current_value = None
            elif self.current_value == 'buy'.lower():
                if DEBUG:
                    print data.strip()
                
                if data.strip() == '':
                    self.buy = Decimal(0)
                else:    
                    self.buy = Decimal(data.strip())
                self.current_value = None
            elif self.current_value == 'sale'.lower():
                if DEBUG:
                    print data.strip()
                
                self.sale = Decimal(data.strip())
                self.current_value = None

def leer_cotizaciones():
    # Obtengo el html de cotizaciones
    if DEBUG:
        print "Leyendo html..."
    
    html_handle = urllib.urlopen(url_brou)
    html = html_handle.read()
    html_handle.close()

    if DEBUG:
        print "Parseando html... (1)"
    
    parser = BROUHTMLParser()
    
    if DEBUG:
        print "Parseando html... (2)"
        
    parser.feed(html)
   
    if DEBUG:
       print "Parseando html listo..."
    
    return parser.cotizaciones
    