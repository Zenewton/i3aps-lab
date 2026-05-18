from django.db.models import Count
from rest_framework import permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.access_requests.models import AccessRequest

from .serializers import AccessRequestSerializer, service_catalog_payload


class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.responsavel_email.lower() == request.user.email.lower()


class AccessRequestViewSet(viewsets.ModelViewSet):
    serializer_class = AccessRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filterset_fields = ["status", "tipo_solicitacao", "infraestrutura"]
    search_fields = ["project_name", "instituicao_nome", "responsavel_email"]
    ordering_fields = ["created_at", "updated_at", "status"]

    def get_queryset(self):
        return AccessRequest.objects.visible_to(self.request.user).select_related("user")

    @action(detail=False, methods=["get"])
    def metrics(self, request):
        queryset = self.get_queryset()
        return Response(
            {
                "total_requests": queryset.count(),
                "total_institutions": queryset.values("instituicao_nome").distinct().count(),
                "status_counts": dict(queryset.values_list("status").annotate(total=Count("id"))),
            }
        )


class ServiceCatalogAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(service_catalog_payload())


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def api_health(request):
    return Response({"status": "ok", "service": "i3aps-api"})
