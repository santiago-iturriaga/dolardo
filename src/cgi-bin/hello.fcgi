#!/usr/bin/python
'''
Created on Oct 16, 2009

@author: santiago
'''

import os
import sys

sys.path.append('/home/santiag0/www/dolardo.ituland.com')
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/MySQL_python-1.2.3c1-py2.4-linux-i686.egg')
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/setuptools-0.6c6-py2.4.egg')
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/flup-1.0.1-py2.4.egg')
#sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/flup-0.5-py2.4.egg')
os.chdir('/home/santiag0/www/dolardo.ituland.com')

def myapp(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Hello World!\n']

if __name__ == '__main__':
    from flup.server.fcgi import WSGIServer
    WSGIServer(myapp).run()

