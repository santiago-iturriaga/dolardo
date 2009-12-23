'''
Created on Oct 13, 2009

@author: santiago
'''

from bottle.bottle import run
from dolardo import sql_connection
from dolardo.ui import index, static, error

if __name__ == '__main__':
    sql_connection = "mysql://santiago@localhost/dolardo"
    run(host='localhost', port=8080)