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
    send_file(filename, root='.')
    
@route('/sitemap.xml')
def static_css(filename):
    send_file('sitemap.xml', root='.')
    
@route('/robots.txt')
def static_css(filename):
    send_file('robots.txt', root='.')