"""
WSGI config for employee project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import subprocess
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "employee.settings")

application = get_wsgi_application()
batch_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'batch.py')
command1 = subprocess.Popen(['python', batch_path])
