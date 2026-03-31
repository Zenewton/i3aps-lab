"""Página de agendamento e solicitação de uso de infraestrutura."""

from __future__ import annotations

from datetime import date

import streamlit as st

from database import create_request
from pages.catalogo import RESOURCES


def _resource_titles() -> list[str]:
    return [r["title"] for r in RESOURCES]


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
        st.markdown("### 🗂️ Dados da Solicitação")
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

        st.markdown("### 🏛️ Instituição")
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

        st.markdown("### ⚙️ Escopo técnico")
        col_e1, col_e2 = st.columns(2)
        escopo_dados = col_e1.selectbox("Tipo de dados", ["clínico", "administrativo", "ambos"])
        uso_ia = col_e2.radio("Uso de IA", ["sim", "não"], horizontal=True)

        st.markdown("### 📅 Período")
        col_p1, col_p2 = st.columns(2)
        data_inicio = col_p1.date_input("Data início", value=date.today())
        data_fim = col_p2.date_input("Data fim", value=date.today())

        st.markdown("### 👤 Responsável")
        col_r1, col_r2 = st.columns(2)
        responsavel_nome = col_r1.text_input(
            "Nome do responsável",
            value=default_responsavel_nome,
        )
        responsavel_email = col_r2.text_input(
            "Email do responsável",
            value=default_responsavel_email,
        )

        st.markdown("### ✅ Termos")
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
