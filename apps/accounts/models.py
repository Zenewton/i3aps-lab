from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    USER_TYPES = [
        ("gestor_sus", "Gestor SUS"),
        ("pesquisador", "Pesquisador"),
        ("empresa", "Empresa"),
        ("outro", "Outro"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    institution = models.CharField("instituição", max_length=255)
    user_type = models.CharField("tipo de usuário", max_length=32, choices=USER_TYPES)
    created_at = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        verbose_name = "perfil de usuário"
        verbose_name_plural = "perfis de usuário"

    def __str__(self) -> str:
        return f"{self.user.get_full_name() or self.user.email} - {self.institution}"
