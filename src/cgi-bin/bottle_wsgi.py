'''
Created on Oct 14, 2009

@author: santiago
'''

import os
import sys

sys.path.append('/var/www/dolardo')
os.chdir('/var/www/dolardo')

import bottle
import dolardo.ui.index
import dolardo.ui.static

application = bottle.bottle.default_app()