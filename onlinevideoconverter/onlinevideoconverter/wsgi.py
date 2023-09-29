"""
WSGI config for onlinevideoconverter project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

# Настройка WSGI-сервера для запуска Django приложения
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinevideoconverter.settings')

application = get_wsgi_application()
