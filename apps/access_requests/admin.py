from django.contrib import admin

from .models import AccessRequest


@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project_name",
        "instituicao_nome",
        "tipo_solicitacao",
        "status",
        "created_at",
    )
    list_filter = ("status", "tipo_solicitacao", "perfil_instituicao", "created_at")
    search_fields = ("project_name", "instituicao_nome", "responsavel_nome", "responsavel_email")
    readonly_fields = ("created_at", "updated_at")
