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
        "Disponibilizar infraestrutura nacional segura, interoperável e escalável para integração "
        "de dados clínicos e operação de serviços digitais, incluindo telemedicina e Inteligência "
        "Artificial (IA), de modo a fortalecer a coordenação do cuidado às condições crônicas na "
        "Atenção Primária à Saúde (APS)."
    )

    st.markdown("### Governança e parcerias")
    st.write("- Ministério da Saúde (articulação institucional para integração à RNDS e políticas de saúde digital)")
    st.write("- Secretarias Estaduais e Municipais de Saúde (implementação e validação da infraestrutura em ambiente real do SUS)")
    st.write("- Instituições de Ciência e Tecnologia (desenvolvimento metodológico, interoperabilidade e avaliação científica aplicada à APS)")
    st.write("- Organizações internacionais e ecossistema de inovação (cooperação técnica, escalabilidade e difusão de boas práticas no SUS)")

    st.markdown("### Conceito I³")
    st.markdown(
        """
        <style>
          .sobre-concept-head {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
          }
          .sobre-concept-head svg {
            width: 20px;
            height: 20px;
            flex: 0 0 auto;
          }
          .sobre-concept-head h4 {
            margin: 0;
            font: 690 1.02rem "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
            color: #2f3342;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown(
                """
                <div class="sobre-concept-head">
                  <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#1f6fb5" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M10.5 13.5l3-3"></path>
                    <path d="M7.8 16.2a3 3 0 0 1 0-4.2l2-2a3 3 0 0 1 4.2 4.2l-.7.7"></path>
                    <path d="M16.2 7.8a3 3 0 0 1 0 4.2l-2 2a3 3 0 1 1-4.2-4.2l.7-.7"></path>
                  </svg>
                  <h4>Interoperabilidade</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("Integração de sistemas e dados para continuidade do cuidado.")
    with c2:
        with st.container(border=True):
            st.markdown(
                """
                <div class="sobre-concept-head">
                  <svg viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="3" y="12" width="4" height="9" fill="#22c55e"></rect>
                    <rect x="10" y="8" width="4" height="13" fill="#0ea5e9"></rect>
                    <rect x="17" y="5" width="4" height="16" fill="#64748b"></rect>
                  </svg>
                  <h4>Informação</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("Dados qualificados para vigilância, gestão e pesquisa aplicada.")
    with c3:
        with st.container(border=True):
            st.markdown(
                """
                <div class="sobre-concept-head">
                  <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#e26aa3" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M8 6c-2 0-3.5 1.7-3.5 3.7 0 1.4.7 2.6 1.8 3.2-.6 2 .4 4.1 2.5 4.8"></path>
                    <path d="M16 6c2 0 3.5 1.7 3.5 3.7 0 1.4-.7 2.6-1.8 3.2.6 2-.4 4.1-2.5 4.8"></path>
                    <path d="M9 8.8c1 .6 2 .9 3 .9s2-.3 3-.9"></path>
                    <path d="M12 9.7v8.1"></path>
                    <path d="M9 13h6"></path>
                  </svg>
                  <h4>Inteligência</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("Modelos analíticos e IA para apoiar decisões em tempo oportuno.")
