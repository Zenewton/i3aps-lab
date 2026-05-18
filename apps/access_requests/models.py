from django.conf import settings
from django.db import models
from django.urls import reverse


class AccessRequestQuerySet(models.QuerySet):
    def visible_to(self, user):
        if user.is_staff:
            return self
        return self.filter(responsavel_email__iexact=user.email)


class AccessRequest(models.Model):
    STATUS_EM_ANALISE = "em_analise"
    STATUS_APROVADO = "aprovado"
    STATUS_EM_EXECUCAO = "em_execucao"
    STATUS_FINALIZADO = "finalizado"
    STATUS_REJEITADO = "rejeitado"

    STATUS_CHOICES = [
        (STATUS_EM_ANALISE, "Em análise"),
        (STATUS_APROVADO, "Aprovado"),
        (STATUS_EM_EXECUCAO, "Em execução"),
        (STATUS_FINALIZADO, "Finalizado"),
        (STATUS_REJEITADO, "Rejeitado"),
    ]

    REQUEST_TYPE_CHOICES = [
        ("reuniao_inicial", "Reunião inicial"),
        ("uso_infraestrutura", "Uso da infraestrutura multiusuária"),
        ("apoio_tecnico", "Apoio técnico em interoperabilidade ou governança de dados"),
        ("validacao_tecnica", "Validação técnica de solução digital"),
        ("cooperacao_cientifica", "Cooperação científica ou projeto de pesquisa"),
        ("projeto_institucional", "Projeto institucional com secretaria ou serviço de saúde"),
        ("outro", "Outro"),
    ]

    INSTITUTION_PROFILE_CHOICES = [
        ("secretaria_estadual", "Secretaria estadual de saúde"),
        ("secretaria_municipal", "Secretaria municipal de saúde"),
        ("servico_publico", "Serviço de saúde público"),
        ("servico_privado_filantropico", "Serviço de saúde privado ou filantrópico"),
        ("pesquisa_pos", "Programa de pós-graduação / grupo de pesquisa"),
        ("empresa_startup", "Empresa / startup / healthtech"),
        ("terceiro_setor", "Organização do terceiro setor"),
        ("outro", "Outro"),
    ]

    DATA_SYSTEMS_CHOICES = [
        ("sim_identificados", "Sim, já existem dados/sistemas identificados"),
        ("sim_mapear", "Sim, mas ainda precisamos mapear"),
        ("nao_orientacao", "Não, é uma demanda inicial de orientação"),
        ("nao_sei", "Não sei informar"),
    ]

    URGENCY_CHOICES = [
        ("conversa_inicial", "Apenas conversa inicial"),
        ("30_dias", "Próximos 30 dias"),
        ("1_3_meses", "1 a 3 meses"),
        ("3_6_meses", "3 a 6 meses"),
        ("sem_prazo", "Sem prazo definido"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="access_requests",
    )
    project_name = models.CharField("nome do projeto ou iniciativa", max_length=255)
    tipo_solicitacao = models.CharField("tipo de solicitação", max_length=64, choices=REQUEST_TYPE_CHOICES)
    infraestrutura = models.CharField("infraestrutura desejada", max_length=255)
    instituicao_nome = models.CharField("nome da instituição", max_length=255)
    perfil_instituicao = models.CharField(
        "perfil da instituição solicitante",
        max_length=64,
        choices=INSTITUTION_PROFILE_CHOICES,
    )
    objetivos_solicitacao = models.JSONField("objetivos da solicitação", default=list)
    demanda_descricao = models.TextField("descrição da demanda")
    dados_sistemas_envolvidos = models.CharField(
        "dados clínicos ou sistemas envolvidos",
        max_length=64,
        choices=DATA_SYSTEMS_CHOICES,
    )
    detalhes_tecnicos = models.TextField("detalhes técnicos adicionais", blank=True)
    prazo_urgencia = models.CharField("prazo ou urgência", max_length=32, choices=URGENCY_CHOICES)
    data_inicio = models.DateField("data início")
    data_fim = models.DateField("data fim")
    responsavel_nome = models.CharField("nome do responsável", max_length=255)
    responsavel_email = models.EmailField("email do responsável", db_index=True)
    concorda_lgpd = models.BooleanField("concorda com LGPD")
    concorda_etica = models.BooleanField("concorda com uso ético")
    status = models.CharField("status", max_length=32, choices=STATUS_CHOICES, default=STATUS_EM_ANALISE, db_index=True)
    notas_admin = models.TextField("notas administrativas", blank=True)
    created_at = models.DateTimeField("data de envio", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    objects = AccessRequestQuerySet.as_manager()

    class Meta:
        verbose_name = "solicitação de acesso"
        verbose_name_plural = "solicitações de acesso"
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["responsavel_email", "-created_at"]),
        ]

    def __str__(self) -> str:
        return f"#{self.pk} - {self.project_name}"

    def get_absolute_url(self):
        return reverse("dashboards:user_dashboard")
