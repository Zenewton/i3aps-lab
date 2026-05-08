"""Compatibilidade legada: catálogo foi incorporado à página de serviços."""

from __future__ import annotations

import streamlit as st

from pages.servicos import INFRASTRUCTURE_RESOURCES, render as render_servicos

# Alias legado para compatibilidade com integrações antigas.
RESOURCES = INFRASTRUCTURE_RESOURCES


def render(set_page) -> None:
    """Mantém rota antiga apontando para a experiência unificada de serviços."""
    st.info("O catálogo de infraestrutura foi incorporado à página de Serviços.")
    render_servicos(set_page)
