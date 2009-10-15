'''
Created on Oct 14, 2009

@author: santiago
'''

import os
import sys

# ... add or import your bottle app code here ...
sys.path.append('/home/santiag0/www/dolardo.ituland.com')
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/MySQL_python-1.2.3c1-py2.4-linux-i686.egg')
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/setuptools-0.6c6-py2.4.egg')
os.chdir('/home/santiag0/www/dolardo.ituland.com/dolardo')

import bottle
import dolardo.ui.index
import dolardo.ui.static

bottle.run(server=bottle.CGIServer)