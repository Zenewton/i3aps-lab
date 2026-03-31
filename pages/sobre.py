"""Página institucional sobre o Laboratório Multiusuário I³ APS."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


def _resolve_about_figure() -> Path | None:
    """Localiza figura institucional da seção Sobre."""
    candidates = [
        Path("capa_i3_aps.svg"),
        Path("assets/capa_i3_aps.svg"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def render() -> None:
    """Renderiza conteúdo institucional e conceito I³."""
    st.title(
        "Sobre o Laboratório Multiusuário I³ APS"
    )

    st.markdown("### Descrição do laboratório")
    st.write(
        "O Laboratório Multiusuário I³ APS é uma estrutura operacional vinculada ao Centro "
        "Nacional de Interoperabilidade, Informação e Inteligência na Atenção Primária à "
        "Saúde. Seu papel é oferecer ambientes compartilhados para integração de dados, "
        "análise e desenvolvimento de soluções em saúde digital para a APS."
    )

    st.markdown("### Visão integrada da plataforma")
    about_figure = _resolve_about_figure()
    if about_figure:
        left, center, right = st.columns([1, 8, 1])
        with center:
            st.image(str(about_figure), use_container_width=True)
            st.caption(
                "Fluxo de integração entre rede assistencial, dados clínicos e administrativos, "
                "camada analítica e suporte à decisão na APS, operado no laboratório."
            )
    else:
        st.warning("Figura institucional não encontrada.")

    st.markdown("### Missão")
    st.write(
        "Disponibilizar infraestrutura multiusuária com agendamento transparente para apoiar "
        "interoperabilidade, qualificação de dados e uso responsável de IA no cuidado e na "
        "gestão da APS."
    )

    st.markdown("### Governança e parcerias")
    st.write("- Ministério da Saúde (placeholder)")
    st.write("- Secretarias Estaduais e Municipais de Saúde (placeholder)")
    st.write("- Instituições de Ciência e Tecnologia (placeholder)")
    st.write("- Organizações internacionais e ecossistema de inovação (placeholder)")

    st.markdown("### Conceito I³")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("#### 🔗 Interoperabilidade")
            st.write("Integração de sistemas e dados para continuidade do cuidado.")
    with c2:
        with st.container(border=True):
            st.markdown("#### 📊 Informação")
            st.write("Dados qualificados para vigilância, gestão e pesquisa aplicada.")
    with c3:
        with st.container(border=True):
            st.markdown("#### 🧠 Inteligência")
            st.write("Modelos analíticos e IA para apoiar decisões em tempo oportuno.")
