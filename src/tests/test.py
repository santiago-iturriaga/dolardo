'''
Created on Oct 13, 2009

@author: santiago
'''

from bottle.bottle import run
import dolardo.ui.index
import dolardo.ui.static
import dolardo.ui.error

if __name__ == '__main__':
    dolardo.sql_connection = "mysql://santiago@localhost/dolardo"
    run(host='localhost', port=8080)