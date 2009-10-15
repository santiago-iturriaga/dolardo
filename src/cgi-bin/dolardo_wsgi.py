'''
Created on Oct 14, 2009

@author: santiago
'''

# File: /var/www/yourapp/app.wsgi

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__FILE__))

import bottle
# ... add or import your bottle app code here ...
# Do NOT use bottle.run() with mod_wsgi
application = bottle.default_app()