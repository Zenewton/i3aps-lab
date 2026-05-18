from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import AccessRequestViewSet, ServiceCatalogAPIView, api_health


app_name = "api"

router = DefaultRouter()
router.register("solicitacoes", AccessRequestViewSet, basename="access-request")

urlpatterns = [
    path("health/", api_health, name="health"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("catalogo/", ServiceCatalogAPIView.as_view(), name="service_catalog"),
    path("", include(router.urls)),
]
