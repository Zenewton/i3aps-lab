"""ASGI config for the I3 APS platform."""

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "i3aps_platform.settings.dev")

application = get_asgi_application()
