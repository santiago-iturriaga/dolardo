#encoding: utf-8
'''
Created on Oct 13, 2009

@author: santiago
'''

from bottle.bottle import route, template, redirect

@route('/')
def index():
    import index_controller
    index_controller.index()

@route('/default/')
def default():
    import index_controller
    return index_controller.default()

@route('/custom/:monedas/')
def custom_monedas(monedas):
    import index_controller
    return index_controller.custom_monedas(monedas)


@route('/custom/:monedas/:height/:width/')
def custom_size(height, width):
    import index_controller
    return index_controller.custom_size(height, width)

@route('/custom/:monedas/:dias/')
def custom_lapso(dias):
    import index_controller
    return index_controller.custom_lapso(dias)
   
@route('/custom/:monedas/:height/:width/:dias/')
def custom(monedas, height, width, dias):
    import index_controller
    return index_controller.custom(monedas, height, width, dias)
    