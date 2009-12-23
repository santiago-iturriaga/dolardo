'''
Created on Oct 13, 2009

@author: santiago
'''

from bottle.bottle import run
from dolardo import PRODUCTION
from dolardo.ui import index, static, error

if __name__ == '__main__':
    PRODUCTION = False
    run(host='localhost', port=8080)