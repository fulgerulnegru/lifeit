import os
import sys

 
path = '/srv/www/lifeit'
if path not in sys.path:
    sys.path.insert(0, '/srv/www/lifeit')


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
