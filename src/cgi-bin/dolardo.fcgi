#!/usr/bin/python
'''
Created on Oct 15, 2009

@author: santiago
'''

import os
import sys

sys.path.append('/home/santiag0/www/dolardo.ituland.com')
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/MySQL_python-1.2.3c1-py2.4-linux-i686.egg')
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/setuptools-0.6c6-py2.4.egg')
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/flup-1.0.1-py2.4.egg')
sys.path.insert(0, '/home/santiag0/python/wsgiref-0.1.2-py2.4.egg')
os.chdir('/home/santiag0/www/dolardo.ituland.com')

#sys.path.append('/var/www/dolardo')
#os.chdir('/var/www/dolardo')

from dolardo import error_reporting

try:
	#from bottle.bottle import default_app
	import bottle
	import dolardo.ui.index
	import dolardo.ui.static

	#application = default_app()
	application = bottle.bottle.default_app()
except:
	(type, value, traceback) = sys.exc_info()
	error_reporting.write_log("Type: %s\nValue: %s\nTraceback %s\n" % (type, value, traceback))

#import dolardo
#from dolardo import error_reporting
#import dolardo.ui.index
#import dolardo.ui.static

#if __name__ == '__main__':
#    from flup.server.fcgi import WSGIServer
#    WSGIServer(bottle.bottle.default_app()).run()

#application = bottle.bottle.default_app()

#error_reporting.write_log("hola")

def myapp(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Hello World!\n']

if __name__ == '__main__':
    from flup.server.fcgi import WSGIServer
    WSGIServer(myapp).run()

