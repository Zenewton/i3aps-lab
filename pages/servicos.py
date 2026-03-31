"""Página institucional de serviços da infraestrutura I³ APS."""

import streamlit as st


SERVICOS = [
    (
        "Integração de dados clínicos interoperáveis",
        "Conexão segura entre sistemas do SUS com base em padrões nacionais e internacionais.",
    ),
    (
        "Inteligência para decisão clínica",
        "Suporte à estratificação de risco, predição de desfechos e coordenação do cuidado.",
    ),
    (
        "Telemedicina integrada",
        "Telemonitoramento, teleintervenção e apoio ao cuidado longitudinal.",
    ),
    (
        "Ambiente multiusuário",
        "Infraestrutura compartilhada para SUS, ICTs e empresas.",
    ),
]


def _render_service_card(title: str, description: str) -> None:
    with st.container(border=True):
        st.markdown(f"#### {title}")
        st.write(description)


def render() -> None:
    """Renderiza página de serviços institucionais."""
    st.title("Serviços da Infraestrutura I³ APS")
    st.write(
        "A plataforma oferece serviços digitais integrados para operação em escala nacional, "
        "com foco em interoperabilidade, cuidado longitudinal e suporte à Atenção Primária à Saúde."
    )

    c1, c2 = st.columns(2, gap="large")
    c3, c4 = st.columns(2, gap="large")

    with c1:
        _render_service_card(*SERVICOS[0])
    with c2:
        _render_service_card(*SERVICOS[1])
    with c3:
        _render_service_card(*SERVICOS[2])
    with c4:
        _render_service_card(*SERVICOS[3])
