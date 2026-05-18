"""URL routing for the I3 APS Django platform."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core.views import health_check


urlpatterns = [
    path("admin/django/", admin.site.urls),
    path("health/", health_check, name="health_check"),
    path("", include("apps.public_site.urls")),
    path("conta/", include("apps.accounts.urls")),
    path("solicitacoes/", include("apps.access_requests.urls")),
    path("painel/", include("apps.dashboards.urls")),
    path("api/", include("apps.api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
