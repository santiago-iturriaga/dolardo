'''
Created on Oct 16, 2009

@author: santiago
'''

from bottle.bottle import route, template

@route('/error')
def error():
    return template('error.html')