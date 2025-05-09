
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eccomerce_api.settings.base')

application = get_asgi_application()
