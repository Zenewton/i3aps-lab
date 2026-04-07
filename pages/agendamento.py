"""Página de agendamento e solicitação de uso de infraestrutura."""

from __future__ import annotations

from datetime import date

import streamlit as st

from database import create_request
from pages.catalogo import RESOURCES


def _resource_titles() -> list[str]:
    return [r["title"] for r in RESOURCES]


def _render_icon_heading(title: str, icon_name: str) -> None:
    icons = {
        "solicitacao": """
            <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#1f6fb5" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
              <path d="M8 3h8l4 4v14H4V3h4z"></path><path d="M8 11h8M8 15h6"></path>
            </svg>
        """,
        "instituicao": """
            <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#0c7f66" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 10 12 4l9 6"></path><path d="M5 10v9h14v-9"></path><path d="M9 19v-5h6v5"></path>
            </svg>
        """,
        "escopo": """
            <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#0d5e86" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 3h7v7"></path><path d="M10 14 21 3"></path><path d="M4 7h7v7H4z"></path>
            </svg>
        """,
        "periodo": """
            <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#6b7280" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="5" width="18" height="16" rx="2"></rect><path d="M16 3v4M8 3v4M3 10h18"></path>
            </svg>
        """,
        "responsavel": """
            <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#7c3aed" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="8" r="3.5"></circle><path d="M5 20a7 7 0 0 1 14 0"></path>
            </svg>
        """,
        "termos": """
            <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#15803d" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 6 9 17l-5-5"></path>
            </svg>
        """,
    }
    icon_svg = icons.get(icon_name, "")
    st.markdown(
        f"""
        <style>
          .form-section-head {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 10px 0 6px 0;
          }}
          .form-section-head svg {{
            width: 18px;
            height: 18px;
            flex: 0 0 auto;
          }}
          .form-section-head h3 {{
            margin: 0;
            font: 680 1.05rem "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
            color: #1f3650;
          }}
        </style>
        <div class="form-section-head">{icon_svg}<h3>{title}</h3></div>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    """Renderiza formulário principal de solicitações."""
    st.title("Agendar Uso do Laboratório")
    st.write(
        "Preencha o formulário abaixo para solicitar acesso e reservar uso dos "
        "recursos do Laboratório Multiusuário I³ APS."
    )

    infra_titles = _resource_titles()
    preselected = st.session_state.get("infra_preselecionada")
    default_idx = infra_titles.index(preselected) if preselected in infra_titles else 0
    auth_user = st.session_state.get("auth_user")

    default_responsavel_nome = auth_user["name"] if auth_user else ""
    default_responsavel_email = auth_user["email"] if auth_user else ""
    default_instituicao_nome = auth_user["institution"] if auth_user else ""

    with st.form("form_agendamento", clear_on_submit=False):
        _render_icon_heading("Dados da Solicitação", "solicitacao")
        project_name = st.text_input(
            "Nome do projeto",
            placeholder="Ex.: Monitoramento longitudinal de condições crônicas na APS",
        )
        tipo_uso = st.selectbox(
            "Tipo de uso",
            [
                "Acesso a ambiente",
                "Integração de sistema",
                "Análise de dados",
                "Teste de solução",
                "Implantação assistencial",
            ],
        )

        infraestrutura = st.selectbox("Infraestrutura desejada", infra_titles, index=default_idx)

        _render_icon_heading("Instituição", "instituicao")
        col_i1, col_i2 = st.columns(2)
        instituicao_nome = col_i1.text_input(
            "Nome da instituição",
            value=default_instituicao_nome,
        )
        instituicao_tipo = col_i2.selectbox(
            "Tipo da instituição",
            ["SUS municipal", "estadual", "ICT", "empresa", "MS", "Anvisa"],
        )

        finalidade = st.text_area("Finalidade", placeholder="Descreva o objetivo do uso da infraestrutura.")

        _render_icon_heading("Escopo técnico", "escopo")
        col_e1, col_e2 = st.columns(2)
        escopo_dados = col_e1.selectbox("Tipo de dados", ["clínico", "administrativo", "ambos"])
        uso_ia = col_e2.radio("Uso de IA", ["sim", "não"], horizontal=True)

        _render_icon_heading("Período", "periodo")
        col_p1, col_p2 = st.columns(2)
        data_inicio = col_p1.date_input("Data início", value=date.today())
        data_fim = col_p2.date_input("Data fim", value=date.today())

        _render_icon_heading("Responsável", "responsavel")
        col_r1, col_r2 = st.columns(2)
        responsavel_nome = col_r1.text_input(
            "Nome do responsável",
            value=default_responsavel_nome,
        )
        responsavel_email = col_r2.text_input(
            "Email do responsável",
            value=default_responsavel_email,
        )

        _render_icon_heading("Termos", "termos")
        concorda_lgpd = st.checkbox("Concordo com LGPD")
        concorda_etica = st.checkbox("Concordo com uso ético")

        submitted = st.form_submit_button("Enviar solicitação", use_container_width=True)

    if submitted:
        if not all([project_name, instituicao_nome, finalidade, responsavel_nome, responsavel_email]):
            st.error("Preencha todos os campos textuais obrigatórios.")
            return
        if data_fim < data_inicio:
            st.error("A data fim não pode ser anterior à data início.")
            return
        if not concorda_lgpd or not concorda_etica:
            st.error("É necessário concordar com LGPD e uso ético para enviar.")
            return

        payload = {
            "project_name": project_name,
            "tipo_uso": tipo_uso,
            "infraestrutura": infraestrutura,
            "instituicao_nome": instituicao_nome,
            "instituicao_tipo": instituicao_tipo,
            "finalidade": finalidade,
            "escopo_dados": escopo_dados,
            "uso_ia": uso_ia,
            "data_inicio": data_inicio.isoformat(),
            "data_fim": data_fim.isoformat(),
            "responsavel_nome": responsavel_nome,
            "responsavel_email": responsavel_email,
            "concorda_lgpd": concorda_lgpd,
            "concorda_etica": concorda_etica,
        }

        request_id = create_request(payload)
        st.success(f"Solicitação enviada com sucesso. Protocolo #{request_id}.")
        st.session_state.pop("infra_preselecionada", None)
