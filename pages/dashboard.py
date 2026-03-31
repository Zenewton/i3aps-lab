"""Dashboard multiusuário com autenticação e gestão de solicitações."""

from __future__ import annotations

import streamlit as st

from database import authenticate_user, create_user, list_requests


STATUS_OPTIONS = ["Todos", "Em análise", "Aprovado", "Em execução", "Finalizado", "Rejeitado"]
USER_TYPES = ["Gestor SUS", "Pesquisador", "Empresa", "Outro"]
COMMON_PERSONAL_DOMAINS = {
    "gmail.com",
    "hotmail.com",
    "outlook.com",
    "yahoo.com",
    "icloud.com",
}


def _is_personal_domain(email: str) -> bool:
    """Indica se o domínio do email é tipicamente pessoal."""
    try:
        domain = email.strip().lower().split("@", maxsplit=1)[1]
    except IndexError:
        return True
    return domain in COMMON_PERSONAL_DOMAINS


def _set_authenticated_user(row) -> None:
    """Persistência de sessão do usuário autenticado."""
    st.session_state["auth_user"] = {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "institution": row["institution"],
        "user_type": row["user_type"],
    }


def _render_authentication_panel() -> None:
    """Exibe login e cadastro para acesso ao dashboard."""
    st.write(
        "Faça login para acompanhar solicitações com rastreabilidade e governança "
        "de acesso alinhadas à LGPD."
    )
    login_tab, register_tab = st.tabs(["Entrar", "Cadastrar"])

    with login_tab:
        with st.form("form_login_dashboard", clear_on_submit=False):
            email = st.text_input("Email", placeholder="seu.email@instituicao.gov.br")
            password = st.text_input("Senha", type="password")
            login_submitted = st.form_submit_button("Entrar", use_container_width=True)

        if login_submitted:
            if not email or not password:
                st.error("Informe email e senha para continuar.")
            else:
                row = authenticate_user(email, password)
                if not row:
                    st.error("Credenciais inválidas.")
                else:
                    _set_authenticated_user(row)
                    st.success("Autenticação concluída.")
                    st.rerun()

    with register_tab:
        with st.form("form_register_dashboard", clear_on_submit=False):
            name = st.text_input("Nome")
            email = st.text_input("Email institucional", placeholder="seu.email@instituicao.gov.br")
            institution = st.text_input("Instituição")
            user_type = st.selectbox("Tipo de usuário", USER_TYPES)
            password = st.text_input("Senha", type="password")
            confirm_password = st.text_input("Confirmar senha", type="password")
            register_submitted = st.form_submit_button("Criar conta", use_container_width=True)

        if register_submitted:
            if not all([name, email, institution, password, confirm_password]):
                st.error("Preencha todos os campos.")
                return
            if "@" not in email:
                st.error("Informe um email válido.")
                return
            if len(password) < 8:
                st.error("A senha deve ter pelo menos 8 caracteres.")
                return
            if password != confirm_password:
                st.error("As senhas não coincidem.")
                return
            if _is_personal_domain(email):
                st.info("Prefira email institucional para governança de acesso.")

            created, message = create_user(
                name=name,
                email=email,
                institution=institution,
                user_type=user_type,
                password=password,
            )
            if not created:
                st.error(message)
                return

            row = authenticate_user(email, password)
            if row:
                _set_authenticated_user(row)
            st.success("Cadastro realizado com sucesso.")
            st.rerun()


def _render_user_header(user: dict[str, str]) -> None:
    """Exibe cabeçalho contextual do usuário logado."""
    with st.container(border=True):
        info_col, action_col = st.columns([5, 1])
        with info_col:
            st.markdown(f"**{user['name']}**")
            st.caption(f"{user['institution']} • {user['email']}")
        with action_col:
            if st.button("Sair", use_container_width=True, key="logout_dashboard"):
                st.session_state.pop("auth_user", None)
                st.success("Sessão encerrada.")
                st.rerun()


def render(set_page) -> None:
    """Renderiza dashboard institucional multiusuário."""
    st.title("Minhas solicitações de uso da infraestrutura")
    user = st.session_state.get("auth_user")

    if not user:
        _render_authentication_panel()
        return

    _render_user_header(user)

    action_col, _ = st.columns([1, 3])
    with action_col:
        if st.button("+ Nova solicitação de uso", type="primary", use_container_width=True):
            set_page("agendamento")
            st.rerun()

    selected_status = st.selectbox("Filtrar por status", STATUS_OPTIONS)
    rows = list_requests(status=selected_status, user_email=user["email"])

    if not rows:
        st.info("Você ainda não possui solicitações. Clique em 'Nova solicitação' para começar.")
        return

    table_data = [
        {
            "Projeto": row["project_name"] or row["infraestrutura"],
            "Instituição": row["instituicao_nome"],
            "Status": row["status"],
            "Data de envio": row["created_at"],
        }
        for row in rows
    ]
    st.dataframe(table_data, use_container_width=True, hide_index=True)
