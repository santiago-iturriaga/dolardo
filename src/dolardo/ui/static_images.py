'''
Created on Oct 14, 2009

@author: santiago
'''

from bottle.bottle import route, send_file

@route('/images/:filename')
def static_images(filename):
    send_file(filename, root='images')