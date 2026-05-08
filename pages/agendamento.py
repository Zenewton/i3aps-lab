"""Página de agendamento e solicitação de uso de infraestrutura."""

from __future__ import annotations

from datetime import date

import streamlit as st

from database import create_request
from pages.servicos import INFRASTRUCTURE_RESOURCES

TIPO_SOLICITACAO_OPTIONS = [
    "Reunião inicial",
    "Uso da infraestrutura multiusuária",
    "Apoio técnico em interoperabilidade ou governança de dados",
    "Validação técnica de solução digital",
    "Cooperação científica ou projeto de pesquisa",
    "Projeto institucional com secretaria ou serviço de saúde",
    "Outro",
]

PERFIL_INSTITUICAO_OPTIONS = [
    "Secretaria estadual de saúde",
    "Secretaria municipal de saúde",
    "Serviço de saúde público",
    "Serviço de saúde privado ou filantrópico",
    "Programa de pós-graduação / grupo de pesquisa",
    "Empresa / startup / healthtech",
    "Organização do terceiro setor",
    "Outro",
]

OBJETIVO_SOLICITACAO_OPTIONS = [
    "Integrar dados clínicos",
    "Avaliar linha de cuidado",
    "Construir ou validar painel/indicador",
    "Testar interoperabilidade",
    "Validar solução digital",
    "Apoiar telemonitoramento ou cuidado remoto",
    "Realizar pesquisa aplicada",
    "Discutir parceria institucional",
    "Outro",
]

DADOS_SISTEMAS_OPTIONS = [
    "Sim, já existem dados/sistemas identificados",
    "Sim, mas ainda precisamos mapear",
    "Não, é uma demanda inicial de orientação",
    "Não sei informar",
]

PRAZO_URGENCIA_OPTIONS = [
    "Apenas conversa inicial",
    "Próximos 30 dias",
    "1 a 3 meses",
    "3 a 6 meses",
    "Sem prazo definido",
]


def _resource_titles() -> list[str]:
    return [r["title"] for r in INFRASTRUCTURE_RESOURCES]


def _default_option_index(options: list[str], value: str | None) -> int:
    return options.index(value) if value in options else 0


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
    st.title("Solicitar uso ou apoio do I³ APS")
    st.write(
        "Use este formulário para solicitar uso da infraestrutura, apoio técnico, reunião inicial, "
        "demonstração ou validação técnica. A equipe do I³ APS fará uma triagem da demanda "
        "conforme escopo, viabilidade, disponibilidade operacional e critérios de governança."
    )

    infra_titles = _resource_titles()
    preselected = st.session_state.get("infra_preselecionada")
    default_idx = infra_titles.index(preselected) if preselected in infra_titles else 0
    tipo_preselecionado = st.session_state.get("tipo_solicitacao_preselecionado")
    tipo_default_idx = _default_option_index(TIPO_SOLICITACAO_OPTIONS, tipo_preselecionado)
    auth_user = st.session_state.get("auth_user")

    default_responsavel_nome = auth_user["name"] if auth_user else ""
    default_responsavel_email = auth_user["email"] if auth_user else ""
    default_instituicao_nome = auth_user["institution"] if auth_user else ""

    with st.form("form_agendamento", clear_on_submit=False):
        _render_icon_heading("Dados da Solicitação", "solicitacao")
        tipo_solicitacao = st.selectbox(
            "Tipo de solicitação",
            TIPO_SOLICITACAO_OPTIONS,
            index=tipo_default_idx,
        )
        project_name = st.text_input(
            "Nome do projeto ou iniciativa",
            placeholder="Ex.: Monitoramento longitudinal de condições crônicas na APS",
        )

        infraestrutura = st.selectbox("Infraestrutura desejada", infra_titles, index=default_idx)

        _render_icon_heading("Instituição", "instituicao")
        col_i1, col_i2 = st.columns(2)
        instituicao_nome = col_i1.text_input(
            "Nome da instituição",
            value=default_instituicao_nome,
        )
        perfil_instituicao = col_i2.selectbox(
            "Perfil da instituição solicitante",
            PERFIL_INSTITUICAO_OPTIONS,
        )

        objetivos_solicitacao = st.multiselect(
            "Objetivo da solicitação",
            OBJETIVO_SOLICITACAO_OPTIONS,
        )
        demanda_descricao = st.text_area(
            "Descreva brevemente sua demanda",
            help=(
                "Informe o problema que deseja resolver, os sistemas envolvidos, o público-alvo, "
                "o território ou serviço de saúde, e o estágio atual da iniciativa."
            ),
            placeholder=(
                "Ex.: Secretaria municipal deseja avaliar perda de seguimento de hipertensos "
                "usando dados do PEC e registros locais da rede."
            ),
        )
        finalidade = demanda_descricao

        _render_icon_heading("Escopo técnico", "escopo")
        dados_sistemas_envolvidos = st.selectbox(
            "Existem dados clínicos ou sistemas envolvidos?",
            DADOS_SISTEMAS_OPTIONS,
        )
        detalhes_tecnicos = st.text_area(
            "Detalhes técnicos adicionais (opcional)",
            help=(
                "Caso deseje, informe sistemas envolvidos, padrões utilizados, requisitos técnicos "
                "ou outras informações relevantes."
            ),
            placeholder="Ex.: PEC, e-SUS APS, prontuário hospitalar, FHIR, RNDS, painel existente...",
            height=90,
        )

        _render_icon_heading("Período", "periodo")
        prazo_urgencia = st.selectbox("Prazo ou urgência", PRAZO_URGENCIA_OPTIONS)
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
        st.info(
            "O envio deste formulário não implica aprovação automática do uso da infraestrutura. "
            "As solicitações serão avaliadas quanto ao alinhamento com a missão do I³ APS, "
            "disponibilidade operacional, governança dos dados, viabilidade técnica e "
            "conformidade ética e legal."
        )
        concorda_lgpd = st.checkbox("Concordo com LGPD")
        concorda_etica = st.checkbox("Concordo com uso ético")

        submitted = st.form_submit_button("Enviar solicitação", use_container_width=True)

    if submitted:
        if not all([project_name, instituicao_nome, demanda_descricao, responsavel_nome, responsavel_email]):
            st.error("Preencha todos os campos textuais obrigatórios.")
            return
        if not objetivos_solicitacao:
            st.error("Selecione pelo menos um objetivo da solicitação.")
            return
        if data_fim < data_inicio:
            st.error("A data fim não pode ser anterior à data início.")
            return
        if not concorda_lgpd or not concorda_etica:
            st.error("É necessário concordar com LGPD e uso ético para enviar.")
            return

        payload = {
            "project_name": project_name,
            "tipo_solicitacao": tipo_solicitacao,
            "tipo_uso": tipo_solicitacao,
            "infraestrutura": infraestrutura,
            "instituicao_nome": instituicao_nome,
            "perfil_instituicao": perfil_instituicao,
            "instituicao_tipo": perfil_instituicao,
            "objetivos_solicitacao": "; ".join(objetivos_solicitacao),
            "demanda_descricao": demanda_descricao,
            "dados_sistemas_envolvidos": (
                f"{dados_sistemas_envolvidos}"
                + (f" | Detalhes: {detalhes_tecnicos.strip()}" if detalhes_tecnicos.strip() else "")
            ),
            "prazo_urgencia": prazo_urgencia,
            "finalidade": finalidade,
            "escopo_dados": "A mapear na triagem",
            "uso_ia": "A avaliar na triagem",
            "data_inicio": data_inicio.isoformat(),
            "data_fim": data_fim.isoformat(),
            "responsavel_nome": responsavel_nome,
            "responsavel_email": responsavel_email,
            "concorda_lgpd": concorda_lgpd,
            "concorda_etica": concorda_etica,
        }

        request_id = create_request(payload)
        st.success(
            "Solicitação recebida. A equipe do I³ APS fará a triagem e entrará em contato "
            f"para os próximos passos. Protocolo #{request_id}."
        )
        st.session_state.pop("infra_preselecionada", None)
        st.session_state.pop("tipo_solicitacao_preselecionado", None)
