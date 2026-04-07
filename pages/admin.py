"""Painel administrativo para gestão de solicitações do laboratório."""

import streamlit as st

from database import get_request_by_id, list_requests, update_request_status


STATUS_OPTIONS = ["Em análise", "Aprovado", "Em execução", "Finalizado", "Rejeitado"]


def _render_update_heading() -> None:
    st.markdown(
        """
        <style>
          .admin-update-head {
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 8px 0 6px 0;
          }
          .admin-update-head svg {
            width: 18px;
            height: 18px;
            flex: 0 0 auto;
          }
          .admin-update-head h3 {
            margin: 0;
            font: 680 1.05rem "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
            color: #1f3650;
          }
        </style>
        <div class="admin-update-head">
          <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#0d5e86" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20h9"></path><path d="m16.5 3.5 4 4L8 20H4v-4L16.5 3.5z"></path>
          </svg>
          <h3>Atualizar solicitação</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    """Renderiza painel admin com visualização geral e atualização de status."""
    st.title("Painel Administrativo")
    st.write("Visualize solicitações do laboratório, atualize status e registre observações internas.")

    rows = list_requests()
    if not rows:
        st.info("Ainda não há solicitações cadastradas.")
        return

    table_data = [
        {
            "ID": row["id"],
            "Infraestrutura": row["infraestrutura"],
            "Instituição": row["instituicao_nome"],
            "Tipo de uso": row["tipo_uso"],
            "Status": row["status"],
            "Data": row["created_at"],
            "Notas": row["notas_admin"] or "",
        }
        for row in rows
    ]
    st.dataframe(table_data, use_container_width=True, hide_index=True)

    _render_update_heading()
    ids = [row["id"] for row in rows]
    selected_id = st.selectbox("Selecione o ID", ids)
    selected_row = get_request_by_id(selected_id)

    if selected_row is None:
        st.error("Solicitação não encontrada.")
        return

    with st.form("admin_update_form"):
        status = st.selectbox(
            "Novo status",
            STATUS_OPTIONS,
            index=STATUS_OPTIONS.index(selected_row["status"])
            if selected_row["status"] in STATUS_OPTIONS
            else 0,
        )
        notes = st.text_area(
            "Notas administrativas",
            value=selected_row["notas_admin"] or "",
            placeholder="Ex.: pendência documental, janela aprovada, contato realizado...",
        )
        submitted = st.form_submit_button("Salvar atualização", use_container_width=True)

    if submitted:
        update_request_status(selected_id, status, notes)
        st.success(f"Solicitação #{selected_id} atualizada com sucesso.")
        st.rerun()
