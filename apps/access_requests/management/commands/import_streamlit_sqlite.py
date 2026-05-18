from __future__ import annotations

import sqlite3
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.access_requests.models import AccessRequest


REQUEST_TYPE_MAP = {
    "Reunião inicial": "reuniao_inicial",
    "Uso da infraestrutura multiusuária": "uso_infraestrutura",
    "Apoio técnico em interoperabilidade ou governança de dados": "apoio_tecnico",
    "Validação técnica de solução digital": "validacao_tecnica",
    "Cooperação científica ou projeto de pesquisa": "cooperacao_cientifica",
    "Projeto institucional com secretaria ou serviço de saúde": "projeto_institucional",
}

STATUS_MAP = {
    "Em análise": AccessRequest.STATUS_EM_ANALISE,
    "Aprovado": AccessRequest.STATUS_APROVADO,
    "Em execução": AccessRequest.STATUS_EM_EXECUCAO,
    "Finalizado": AccessRequest.STATUS_FINALIZADO,
    "Rejeitado": AccessRequest.STATUS_REJEITADO,
}


class Command(BaseCommand):
    help = "Importa usuários e solicitações do SQLite legado do Streamlit."

    def add_arguments(self, parser):
        parser.add_argument("--db", default="data/i3_aps.db", help="Caminho do SQLite legado.")

    def handle(self, *args, **options):
        db_path = Path(options["db"])
        if not db_path.exists():
            raise CommandError(f"Banco legado não encontrado: {db_path}")

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        users_created = 0
        requests_created = 0

        for row in conn.execute("SELECT * FROM users").fetchall():
            email = row["email"].strip().lower()
            user, created = User.objects.get_or_create(
                username=email,
                defaults={"email": email, "first_name": row["name"].split(maxsplit=1)[0]},
            )
            if created:
                user.set_unusable_password()
                user.save(update_fields=["password"])
                users_created += 1
            profile = user.profile
            profile.institution = row["institution"]
            profile.user_type = self._profile_type(row["user_type"])
            profile.save(update_fields=["institution", "user_type"])

        for row in conn.execute("SELECT * FROM requests").fetchall():
            legacy_key = f"streamlit-{row['id']}"
            if AccessRequest.objects.filter(notas_admin__contains=legacy_key).exists():
                continue
            email = (row["responsavel_email"] or "").strip().lower()
            user = User.objects.filter(email__iexact=email).first()
            notes = row["notas_admin"] or ""
            notes = f"{notes}\n\nImportado do Streamlit: {legacy_key}".strip()
            AccessRequest.objects.create(
                user=user,
                project_name=row["project_name"] or row["infraestrutura"],
                tipo_solicitacao=REQUEST_TYPE_MAP.get(row["tipo_solicitacao"], "outro"),
                infraestrutura=row["infraestrutura"],
                instituicao_nome=row["instituicao_nome"],
                perfil_instituicao=self._institution_profile(row["perfil_instituicao"] or row["instituicao_tipo"]),
                objetivos_solicitacao=self._split_objectives(row["objetivos_solicitacao"]),
                demanda_descricao=row["demanda_descricao"] or row["finalidade"],
                dados_sistemas_envolvidos="nao_sei",
                detalhes_tecnicos=row["dados_sistemas_envolvidos"] or "",
                prazo_urgencia=self._urgency(row["prazo_urgencia"]),
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                responsavel_nome=row["responsavel_nome"],
                responsavel_email=email,
                concorda_lgpd=bool(row["concorda_lgpd"]),
                concorda_etica=bool(row["concorda_etica"]),
                status=STATUS_MAP.get(row["status"], AccessRequest.STATUS_EM_ANALISE),
                notas_admin=notes,
                created_at=timezone.now(),
            )
            requests_created += 1

        self.stdout.write(self.style.SUCCESS(f"Importação concluída: {users_created} usuários, {requests_created} solicitações."))

    def _split_objectives(self, raw_value: str | None) -> list[str]:
        if not raw_value:
            return []
        return [item.strip() for item in raw_value.split(";") if item.strip()]

    def _profile_type(self, raw_value: str) -> str:
        normalized = raw_value.strip().lower()
        if "gestor" in normalized:
            return "gestor_sus"
        if "pesquis" in normalized:
            return "pesquisador"
        if "empresa" in normalized:
            return "empresa"
        return "outro"

    def _institution_profile(self, raw_value: str) -> str:
        normalized = raw_value.strip().lower()
        if "estadual" in normalized:
            return "secretaria_estadual"
        if "municipal" in normalized:
            return "secretaria_municipal"
        if "públic" in normalized or "public" in normalized:
            return "servico_publico"
        if "empresa" in normalized or "startup" in normalized:
            return "empresa_startup"
        if "pesquisa" in normalized or "pós" in normalized or "pos" in normalized:
            return "pesquisa_pos"
        return "outro"

    def _urgency(self, raw_value: str | None) -> str:
        normalized = (raw_value or "").strip().lower()
        if "30" in normalized:
            return "30_dias"
        if "1 a 3" in normalized:
            return "1_3_meses"
        if "3 a 6" in normalized:
            return "3_6_meses"
        if "sem prazo" in normalized:
            return "sem_prazo"
        return "conversa_inicial"
