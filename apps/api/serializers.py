from django.contrib.auth.models import User
from rest_framework import serializers

from apps.access_requests.models import AccessRequest
from apps.accounts.models import UserProfile
from apps.public_site.content import INFRASTRUCTURE_RESOURCES, SERVICE_OFFERINGS


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["institution", "user_type"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "profile"]


class AccessRequestSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    tipo_solicitacao_label = serializers.CharField(source="get_tipo_solicitacao_display", read_only=True)

    class Meta:
        model = AccessRequest
        fields = [
            "id",
            "project_name",
            "tipo_solicitacao",
            "tipo_solicitacao_label",
            "infraestrutura",
            "instituicao_nome",
            "perfil_instituicao",
            "objetivos_solicitacao",
            "demanda_descricao",
            "dados_sistemas_envolvidos",
            "detalhes_tecnicos",
            "prazo_urgencia",
            "data_inicio",
            "data_fim",
            "responsavel_nome",
            "responsavel_email",
            "concorda_lgpd",
            "concorda_etica",
            "status",
            "status_label",
            "notas_admin",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["status", "notas_admin", "created_at", "updated_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        if user.is_authenticated:
            validated_data["user"] = user
        return super().create(validated_data)


class ServiceOfferingSerializer(serializers.Serializer):
    title = serializers.CharField()
    summary = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    problem = serializers.CharField(required=False)
    examples = serializers.ListField(child=serializers.CharField(), required=False)
    users = serializers.CharField(required=False)
    infra = serializers.CharField(required=False)
    cta = serializers.CharField(required=False)
    use_cases = serializers.CharField(required=False)


class MetricsSerializer(serializers.Serializer):
    total_requests = serializers.IntegerField()
    total_institutions = serializers.IntegerField()
    status_counts = serializers.DictField(child=serializers.IntegerField())


def service_catalog_payload():
    return {
        "services": SERVICE_OFFERINGS,
        "infrastructure": INFRASTRUCTURE_RESOURCES,
    }
