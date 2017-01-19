"""
WSGI config for djproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

#sys.path.append("/Users/lichen/Documents/workspace/djproject/src/djproject")
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djproject.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "djproject.settings"

application = get_wsgi_application()
