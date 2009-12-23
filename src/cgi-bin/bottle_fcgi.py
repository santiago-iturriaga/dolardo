#!/usr/bin/python
'''
Created on Oct 15, 2009

@author: santiago
'''

import os
import sys

sys.path.append('/home/santiag0/www/dolardo.ituland.com')
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/flup-1.0.1-py2.4.egg')
sys.path.insert(0, '/home/santiag0/python/wsgiref-0.1.2-py2.4.egg')
os.chdir('/home/santiag0/www/dolardo.ituland.com')

try:
    from bottle import bottle
    from dolardo.ui import index, static, error
        
    if __name__ == '__main__':
        from flup.server.fcgi import WSGIServer
        WSGIServer(bottle.default_app()).run()
except:
    from dolardo import error_reporting
    
    (type, value, traceback) = sys.exc_info()
    error_reporting.write_log("Type: %s\nValue: %s\nTraceback: %s\n" % (type, value, traceback))
    