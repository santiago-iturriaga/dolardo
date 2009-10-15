'''
Created on Oct 14, 2009

@author: santiago
'''

import os
import sys

# ... add or import your bottle app code here ...
current_path = "/home/santiag0/www/dolardo.ituland.com/cgi-bin"
sys.path.append(os.path.join(current_path, LIB_PATH))
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/MySQL_python-1.2.3c1-py2.4-linux-i686.egg')
sys.path.insert(0, '/usr/local/lib/python2.4/site-packages/setuptools-0.6c6-py2.4.egg')
os.chdir(os.path.join(current_path, BASE_PATH))

import bottle
import dolardo.ui.index
import dolardo.ui.static

bottle.run(server=bottle.CGIServer)