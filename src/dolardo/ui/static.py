'''
Created on Oct 14, 2009

@author: santiago
'''

from bottle.bottle import route, send_file

@route('/images/:filename')
def static_images(filename):
    send_file(filename, root='images')
    
@route('/css/:filename')
def static_css(filename):
    send_file(filename, root='css')

@route('/css/images/:filename')
def static_css(filename):
    send_file(filename, root='css/images')

@route('/js/:filename')
def static_css(filename):
    send_file(filename, root='js')
    
@route('/sitemap.xml')
def sitemap():
    send_file('sitemap.xml', root='.')

@route('/sitemap.xsl')
def sitemap():
    send_file('sitemap.xsl', root='.')
    
@route('/robots.txt')
def robots():
    send_file('robots.txt', root='.')

