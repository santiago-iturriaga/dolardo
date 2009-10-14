'''
Created on Oct 13, 2009

@author: santiago
'''

from bottle.bottle import run
import dolardo.ui.index
import dolardo.ui.static

if __name__ == '__main__':
    run(host='localhost', port=8080)