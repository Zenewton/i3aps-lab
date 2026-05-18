from datetime import date

from django import forms

from apps.public_site.content import INFRASTRUCTURE_RESOURCES

from .models import AccessRequest


OBJECTIVE_CHOICES = [
    ("Integrar dados clínicos", "Integrar dados clínicos"),
    ("Avaliar linha de cuidado", "Avaliar linha de cuidado"),
    ("Construir ou validar painel/indicador", "Construir ou validar painel/indicador"),
    ("Testar interoperabilidade", "Testar interoperabilidade"),
    ("Validar solução digital", "Validar solução digital"),
    ("Apoiar telemonitoramento ou cuidado remoto", "Apoiar telemonitoramento ou cuidado remoto"),
    ("Realizar pesquisa aplicada", "Realizar pesquisa aplicada"),
    ("Discutir parceria institucional", "Discutir parceria institucional"),
    ("Outro", "Outro"),
]


class AccessRequestForm(forms.ModelForm):
    objetivos_solicitacao = forms.MultipleChoiceField(
        label="Objetivo da solicitação",
        choices=OBJECTIVE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )
    infraestrutura = forms.ChoiceField(
        label="Infraestrutura desejada",
        choices=[(item["title"], item["title"]) for item in INFRASTRUCTURE_RESOURCES],
    )
    concorda_lgpd = forms.BooleanField(label="Concordo com LGPD")
    concorda_etica = forms.BooleanField(label="Concordo com uso ético")

    class Meta:
        model = AccessRequest
        fields = [
            "tipo_solicitacao",
            "project_name",
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
        ]
        widgets = {
            "data_inicio": forms.DateInput(attrs={"type": "date"}),
            "data_fim": forms.DateInput(attrs={"type": "date"}),
            "demanda_descricao": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": (
                        "Ex.: Secretaria municipal deseja avaliar perda de seguimento "
                        "de hipertensos usando dados do PEC e registros locais da rede."
                    ),
                }
            ),
            "detalhes_tecnicos": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Ex.: PEC, e-SUS APS, prontuário hospitalar, FHIR, RNDS, painel existente...",
                }
            ),
        }
        labels = {
            "demanda_descricao": "Descreva brevemente sua demanda",
            "detalhes_tecnicos": "Detalhes técnicos adicionais (opcional)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._remove_blank_choices()
        self.fields["tipo_solicitacao"].initial = "reuniao_inicial"
        self.fields["perfil_instituicao"].initial = "secretaria_estadual"
        self.fields["dados_sistemas_envolvidos"].initial = "sim_identificados"
        self.fields["prazo_urgencia"].initial = "conversa_inicial"
        self.fields["data_inicio"].initial = date.today
        self.fields["data_fim"].initial = date.today

        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.setdefault("class", "form-check-input")
            else:
                field.widget.attrs.setdefault("class", "form-control")
        self.fields["tipo_solicitacao"].widget.attrs["class"] = "form-select"
        self.fields["infraestrutura"].widget.attrs["class"] = "form-select"
        self.fields["perfil_instituicao"].widget.attrs["class"] = "form-select"
        self.fields["dados_sistemas_envolvidos"].widget.attrs["class"] = "form-select"
        self.fields["prazo_urgencia"].widget.attrs["class"] = "form-select"

    def _remove_blank_choices(self) -> None:
        """Mantém selects com o mesmo comportamento do Streamlit: primeira opção válida selecionada."""
        for field_name in [
            "tipo_solicitacao",
            "perfil_instituicao",
            "dados_sistemas_envolvidos",
            "prazo_urgencia",
        ]:
            field = self.fields[field_name]
            field.choices = [(value, label) for value, label in field.choices if value != ""]

    def clean(self):
        cleaned = super().clean()
        data_inicio = cleaned.get("data_inicio")
        data_fim = cleaned.get("data_fim")
        if data_inicio and data_fim and data_fim < data_inicio:
            self.add_error("data_fim", "A data fim não pode ser anterior à data início.")
        return cleaned


class AccessRequestStatusForm(forms.ModelForm):
    class Meta:
        model = AccessRequest
        fields = ["status", "notas_admin"]
        widgets = {"notas_admin": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].widget.attrs["class"] = "form-select"
        self.fields["notas_admin"].widget.attrs["class"] = "form-control"
