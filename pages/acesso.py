"""Página institucional para regras e fluxo de acesso à infraestrutura I³ APS."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

NORMS_PDF_PATH = Path("assets/docs/normas_acesso_uso_governanca_i3_aps.pdf")
DOCS_DIR = Path("assets/docs")


def _go_to(set_page, page_key: str) -> None:
    """Navegação reutilizável para botões de ação."""
    set_page(page_key)
    st.rerun()


def _load_norms_pdf() -> bytes | None:
    """Carrega PDF de normas para download."""
    if not NORMS_PDF_PATH.exists():
        return None
    try:
        return NORMS_PDF_PATH.read_bytes()
    except OSError:
        return None


def _resolve_document_path(*tokens: str) -> Path | None:
    if not DOCS_DIR.exists():
        return None

    for path in sorted(DOCS_DIR.glob("*.pdf")):
        name = path.name.lower()
        if all(token.lower() in name for token in tokens):
            return path
    return None


def _load_pdf(path: Path | None) -> bytes | None:
    if path is None or not path.exists():
        return None
    try:
        return path.read_bytes()
    except OSError:
        return None


def _render_institutional_documents(set_page) -> None:
    """Mostra referência resumida aos documentos formais de governança."""
    st.markdown("### Normas, governança e documentos institucionais")
    st.write(
        "O uso da infraestrutura do I³ APS segue normas institucionais, regimento próprio "
        "e instâncias formais de governança, incluindo coordenação, comitê gestor e comitê "
        "de usuários."
    )

    regimento_path = _resolve_document_path("regimento")
    criacao_path = _resolve_document_path("portaria 1", "cria")
    regimento_pdf = _load_pdf(regimento_path)
    criacao_pdf = _load_pdf(criacao_path)

    col_regimento, col_criacao, col_sobre = st.columns(3, gap="medium")
    with col_regimento:
        if regimento_pdf:
            st.download_button(
                "Ver regimento",
                data=regimento_pdf,
                file_name="regimento_i3_aps.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="acesso_download_regimento",
            )
        else:
            st.info("Regimento não localizado.")
    with col_criacao:
        if criacao_pdf:
            st.download_button(
                "Ver criação do I³ APS",
                data=criacao_pdf,
                file_name="portaria_criacao_i3_aps.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="acesso_download_criacao",
            )
        else:
            st.info("Portaria de criação não localizada.")
    with col_sobre:
        if st.button("Conhecer governança", use_container_width=True):
            _go_to(set_page, "sobre")


def render(set_page) -> None:
    """Renderiza conteúdo de acesso com linguagem simples e download das normas."""
    st.title("Acesso à Infraestrutura I³ APS")
    st.write(
        "O I³ APS é uma infraestrutura nacional e multiusuária. O acesso é aberto a instituições "
        "do SUS, pesquisadores, gestores e empresas, com critérios de segurança, ética e governança."
    )

    st.markdown("### Como funciona o acesso")
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        with st.container(border=True):
            st.markdown("**1. Defina seu objetivo**")
            st.write("Informe qual problema, serviço ou projeto será desenvolvido com a infraestrutura.")
    with c2:
        with st.container(border=True):
            st.markdown("**2. Envie a solicitação**")
            st.write("Preencha o formulário com dados institucionais, escopo técnico e período de uso.")
    with c3:
        with st.container(border=True):
            st.markdown("**3. Passe pela análise**")
            st.write("A equipe avalia aderência técnica, LGPD, governança e disponibilidade operacional.")

    st.markdown("### Regras completas de acesso e uso")
    st.write(
        "As normas detalham elegibilidade, responsabilidades, critérios de priorização, segurança da "
        "informação e governança de uso da infraestrutura."
    )

    pdf_data = _load_norms_pdf()
    if pdf_data:
        st.download_button(
            "Ver regras completas (PDF)",
            data=pdf_data,
            file_name="normas_acesso_uso_governanca_i3_aps.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="download_normas_acesso",
        )
        st.caption(f"Arquivo: {NORMS_PDF_PATH}")
    else:
        st.warning(
            "Arquivo de normas não encontrado em "
            f"`{NORMS_PDF_PATH}`. Adicione o PDF para habilitar o download."
        )

    _render_institutional_documents(set_page)

    st.markdown("### Próximo passo")
    col_primary, col_secondary = st.columns([2, 1], gap="medium")
    with col_primary:
        if st.button("Solicitar acesso institucional", type="primary", use_container_width=True):
            _go_to(set_page, "agendamento")
    with col_secondary:
        if st.button("Ver serviços disponíveis", use_container_width=True):
            _go_to(set_page, "servicos")
