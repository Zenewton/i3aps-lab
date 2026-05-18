"""WSGI config for the I3 APS platform."""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "i3aps_platform.settings.prod")

application = get_wsgi_application()
