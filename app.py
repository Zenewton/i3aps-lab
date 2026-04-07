"""Aplicação Streamlit principal do Laboratório Multiusuário I³ APS."""

from pathlib import Path

import streamlit as st

from database import init_db
from pages import admin, agendamento, catalogo, dashboard, equipe, home, servicos, sobre


st.set_page_config(
    page_title="I³ APS",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_custom_style() -> None:
    """Aplica estilos visuais para reforçar identidade institucional moderna."""
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(180deg, #f4f8fb 0%, #ffffff 35%);
            }
            /* Remove o menu técnico automático do Streamlit (pages/). */
            [data-testid="stSidebarNav"] {
                display: none;
            }
            [data-testid="stSidebar"] {
                background: #0a2f4f;
            }
            [data-testid="stSidebar"] .sidebar-brand-logo {
                width: 84px;
                margin: 0 auto 0.35rem auto;
                opacity: 0.92;
            }
            [data-testid="stSidebar"] .sidebar-brand-logo svg {
                width: 100%;
                height: auto;
                display: block;
            }
            [data-testid="stSidebar"] .sidebar-brand-title {
                text-align: center;
                color: #f0f6fc;
                font-size: 1.3rem;
                font-weight: 760;
                letter-spacing: 0.3px;
                margin: 0 0 0.1rem 0;
            }
            [data-testid="stSidebar"] .sidebar-brand-subtitle {
                text-align: center;
                color: #d4e7f7;
                font-size: 0.88rem;
                font-weight: 620;
                margin: 0 0 0.05rem 0;
            }
            [data-testid="stSidebar"] .sidebar-brand-caption {
                text-align: center;
                color: #bfd8ea;
                font-size: 0.8rem;
                margin: 0 0 0.6rem 0;
            }
            [data-testid="stSidebar"] * {
                color: #f0f6fc;
            }
            /* Corrige contraste dos botões da sidebar com paleta institucional. */
            [data-testid="stSidebar"] .stButton > button {
                background: #e6f0f8;
                color: #0a2f4f !important;
                border: 1px solid #7ea6c2;
                border-radius: 10px;
                font-weight: 600;
                display: flex;
                align-items: center;
                justify-content: flex-start;
                gap: 10px;
            }
            [data-testid="stSidebar"] .stButton > button * {
                color: #0a2f4f !important;
            }
            [data-testid="stSidebar"] .stButton > button::before {
                content: "";
                width: 17px;
                height: 17px;
                flex: 0 0 17px;
                display: inline-block;
                background-color: currentColor;
                -webkit-mask-size: contain;
                mask-size: contain;
                -webkit-mask-repeat: no-repeat;
                mask-repeat: no-repeat;
                -webkit-mask-position: center;
                mask-position: center;
            }
            [data-testid="stSidebar"] .st-key-nav_home button::before {
                -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M12 3l9 8h-3v9h-5v-6H11v6H6v-9H3l9-8z'/%3E%3C/svg%3E");
                mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M12 3l9 8h-3v9h-5v-6H11v6H6v-9H3l9-8z'/%3E%3C/svg%3E");
            }
            [data-testid="stSidebar"] .st-key-nav_catalogo button::before {
                -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M4 6.5C4 5.7 4.7 5 5.5 5h13c.8 0 1.5.7 1.5 1.5S19.3 8 18.5 8h-13C4.7 8 4 7.3 4 6.5zm0 5C4 10.7 4.7 10 5.5 10h13c.8 0 1.5.7 1.5 1.5S19.3 13 18.5 13h-13c-.8 0-1.5-.7-1.5-1.5zm0 5c0-.8.7-1.5 1.5-1.5h13c.8 0 1.5.7 1.5 1.5S19.3 18 18.5 18h-13C4.7 18 4 17.3 4 16.5z'/%3E%3C/svg%3E");
                mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M4 6.5C4 5.7 4.7 5 5.5 5h13c.8 0 1.5.7 1.5 1.5S19.3 8 18.5 8h-13C4.7 8 4 7.3 4 6.5zm0 5C4 10.7 4.7 10 5.5 10h13c.8 0 1.5.7 1.5 1.5S19.3 13 18.5 13h-13c-.8 0-1.5-.7-1.5-1.5zm0 5c0-.8.7-1.5 1.5-1.5h13c.8 0 1.5.7 1.5 1.5S19.3 18 18.5 18h-13C4.7 18 4 17.3 4 16.5z'/%3E%3C/svg%3E");
            }
            [data-testid="stSidebar"] .st-key-nav_servicos button::before {
                -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M3 7.5A1.5 1.5 0 0 1 4.5 6h6A1.5 1.5 0 0 1 12 7.5v6a1.5 1.5 0 0 1-1.5 1.5h-6A1.5 1.5 0 0 1 3 13.5v-6zm9 3A1.5 1.5 0 0 1 13.5 9h6A1.5 1.5 0 0 1 21 10.5v6a1.5 1.5 0 0 1-1.5 1.5h-6A1.5 1.5 0 0 1 12 16.5v-6z'/%3E%3C/svg%3E");
                mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M3 7.5A1.5 1.5 0 0 1 4.5 6h6A1.5 1.5 0 0 1 12 7.5v6a1.5 1.5 0 0 1-1.5 1.5h-6A1.5 1.5 0 0 1 3 13.5v-6zm9 3A1.5 1.5 0 0 1 13.5 9h6A1.5 1.5 0 0 1 21 10.5v6a1.5 1.5 0 0 1-1.5 1.5h-6A1.5 1.5 0 0 1 12 16.5v-6z'/%3E%3C/svg%3E");
            }
            [data-testid="stSidebar"] .st-key-nav_agendamento button::before {
                -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M7 2a1 1 0 0 1 1 1v1h8V3a1 1 0 1 1 2 0v1h1a3 3 0 0 1 3 3v11a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3h1V3a1 1 0 0 1 1-1zm13 8H4v8a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-8z'/%3E%3C/svg%3E");
                mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M7 2a1 1 0 0 1 1 1v1h8V3a1 1 0 1 1 2 0v1h1a3 3 0 0 1 3 3v11a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3h1V3a1 1 0 0 1 1-1zm13 8H4v8a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-8z'/%3E%3C/svg%3E");
            }
            [data-testid="stSidebar"] .st-key-nav_dashboard button::before {
                -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M12 12a5 5 0 1 0-5-5 5 5 0 0 0 5 5zm-8 9a8 8 0 0 1 16 0z'/%3E%3C/svg%3E");
                mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M12 12a5 5 0 1 0-5-5 5 5 0 0 0 5 5zm-8 9a8 8 0 0 1 16 0z'/%3E%3C/svg%3E");
            }
            [data-testid="stSidebar"] .st-key-nav_equipe button::before {
                -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M8 11a4 4 0 1 0-4-4 4 4 0 0 0 4 4zm8 0a4 4 0 1 0-4-4 4 4 0 0 0 4 4zM1 21a7 7 0 0 1 14 0zm9 0a7 7 0 0 1 13 0z'/%3E%3C/svg%3E");
                mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M8 11a4 4 0 1 0-4-4 4 4 0 0 0 4 4zm8 0a4 4 0 1 0-4-4 4 4 0 0 0 4 4zM1 21a7 7 0 0 1 14 0zm9 0a7 7 0 0 1 13 0z'/%3E%3C/svg%3E");
            }
            [data-testid="stSidebar"] .st-key-nav_sobre button::before {
                -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 15h-2v-6h2zm0-8h-2V7h2z'/%3E%3C/svg%3E");
                mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 15h-2v-6h2zm0-8h-2V7h2z'/%3E%3C/svg%3E");
            }
            [data-testid="stSidebar"] .stButton > button:hover {
                background: #d7e8f4;
                color: #07253f !important;
                border-color: #5f8fab;
            }
            [data-testid="stSidebar"] .stButton > button:hover * {
                color: #07253f !important;
            }
            [data-testid="stSidebar"] .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 5px 12px rgba(6, 39, 63, 0.2);
                transition: all 0.15s ease-out;
            }
            [data-testid="stSidebar"] .stButton > button[kind="primary"] {
                background: #0d5e86 !important;
                border-color: #0d5e86 !important;
                color: #ffffff !important;
                box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.12);
            }
            [data-testid="stSidebar"] .stButton > button[kind="primary"] * {
                color: #ffffff !important;
            }
            [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
                background: #0a4f72 !important;
                border-color: #0a4f72 !important;
            }
            h1, h2, h3 {
                color: #08304a;
            }
            .stButton > button[kind="primary"] {
                border-radius: 10px;
                border: 1px solid #0d5e86;
                background: #0d5e86;
                color: #ffffff;
                font-weight: 600;
            }
            .stButton > button[kind="primary"]:hover {
                background: #0a4f72;
                color: #ffffff;
                border-color: #0a4f72;
            }
            .stButton > button[kind="secondary"] {
                border-radius: 10px;
                border: 1px solid #9ab6ca;
                background: #ffffff;
                color: #0b3a56;
                font-weight: 600;
            }
            .stButton > button[kind="secondary"]:hover {
                border-color: #7ea6c2;
                background: #eef5fb;
                color: #072f47;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def set_page(page_key: str) -> None:
    """Atualiza rota atual no estado da sessão."""
    st.session_state["page"] = page_key


def init_session_state() -> None:
    """Garante estado inicial de navegação."""
    if "page" not in st.session_state:
        st.session_state["page"] = "home"


def sidebar_navigation() -> None:
    """Menu lateral da aplicação."""
    logo_candidates = [
        Path("logos/logo_i3_aps_institucional_mark_v3.svg"),
        Path("logos/logo_i3_aps_institucional_mark_v2.svg"),
    ]
    sidebar_logo = next((path for path in logo_candidates if path.exists()), None)
    if sidebar_logo:
        try:
            svg_content = sidebar_logo.read_text(encoding="utf-8")
            st.sidebar.markdown(
                f'<div class="sidebar-brand-logo">{svg_content}</div>',
                unsafe_allow_html=True,
            )
        except OSError:
            pass

    st.sidebar.markdown(
        '<div class="sidebar-brand-title">I³ APS</div>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        '<div class="sidebar-brand-subtitle"><strong>Ambiente multiusuário</strong></div>',
        unsafe_allow_html=True,
    )

    nav_items = [
        ("home", "Início"),
        ("catalogo", "Infraestrutura"),
        ("servicos", "Serviços"),
        ("agendamento", "Agendar Uso"),
        ("dashboard", "Área do Usuário"),
        ("equipe", "Equipe"),
        ("sobre", "Sobre"),
    ]

    current_page = st.session_state.get("page", "home")
    for key, label in nav_items:
        button_type = "primary" if current_page == key else "secondary"
        if st.sidebar.button(
            label,
            key=f"nav_{key}",
            use_container_width=True,
            type=button_type,
        ):
            set_page(key)
            st.rerun()


def route_page() -> None:
    """Roteador simples de páginas."""
    page_key = st.session_state.get("page", "home")

    routes = {
        "home": lambda: home.render(set_page),
        "catalogo": lambda: catalogo.render(set_page),
        "servicos": servicos.render,
        "equipe": equipe.render,
        "agendamento": agendamento.render,
        "dashboard": lambda: dashboard.render(set_page),
        "admin": admin.render,
        "sobre": sobre.render,
    }

    render = routes.get(page_key, lambda: home.render(set_page))
    render()


# Bootstrap da aplicação.
init_db()
init_session_state()
apply_custom_style()
sidebar_navigation()
route_page()
