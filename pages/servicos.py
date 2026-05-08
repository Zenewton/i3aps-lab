"""Página de serviços do Laboratório Multiusuário I³ APS."""

from __future__ import annotations

import streamlit as st

INFRASTRUCTURE_RESOURCES = [
    {
        "title": "Integração de Dados Clínicos do SUS",
        "description": (
            "Apoio técnico para conectar sistemas da APS, atenção especializada e rede hospitalar "
            "com padrões interoperáveis e implantação progressiva."
        ),
        "use_cases": "PEC, prontuários hospitalares, RNDS, linhas de cuidado e painéis assistenciais.",
        "services": [
            "Apoio técnico em interoperabilidade e implementação",
            "Sandbox para testes e validação",
        ],
    },
    {
        "title": "Ambiente Seguro para Dados Clínicos e Pesquisa",
        "description": (
            "Espaço controlado para organização, tratamento e análise de dados sensíveis, com "
            "rastreabilidade, governança e atenção à LGPD."
        ),
        "use_cases": "Estudos multicêntricos, avaliação de desfechos e análise de linhas de cuidado.",
        "services": [
            "Ambiente seguro para dados clínicos e pesquisa",
            "Inteligência analítica para apoio ao cuidado",
        ],
    },
    {
        "title": "Monitoramento e Gestão do Cuidado",
        "description": (
            "Dashboards, indicadores e rotinas analíticas para apoiar equipes e gestores no "
            "acompanhamento longitudinal da população."
        ),
        "use_cases": "Hipertensão, diabetes, pós-alta, perda de seguimento e condições crônicas.",
        "services": [
            "Monitoramento e gestão do cuidado",
            "Inteligência analítica para apoio ao cuidado",
        ],
    },
    {
        "title": "Telemonitoramento e Cuidado Remoto",
        "description": (
            "Apoio à estruturação de fluxos de acompanhamento remoto, comunicação e priorização "
            "de pacientes para continuidade do cuidado."
        ),
        "use_cases": "Condições crônicas, acompanhamento domiciliar e continuidade após internação.",
        "services": [
            "Telemonitoramento e cuidado remoto",
            "Monitoramento e gestão do cuidado",
        ],
    },
    {
        "title": "Sandbox para Testes e Validação",
        "description": (
            "Ambiente simulado e controlado para testar integrações, fluxos de dados e aderência "
            "a padrões antes de uso em operação real."
        ),
        "use_cases": "Validação FHIR, integração com RNDS, MVPs e provas técnicas de interoperabilidade.",
        "services": [
            "Sandbox para testes e validação",
            "Apoio técnico em interoperabilidade e implementação",
        ],
    },
]

USER_PROFILES = [
    {
        "title": "Secretarias Municipais e Estaduais",
        "description": (
            "Apoio para transformar dados já existentes em informação útil para gestão, regulação "
            "e coordenação do cuidado."
        ),
        "examples": [
            "Integração progressiva de sistemas da rede.",
            "Dashboards assistenciais para linhas de cuidado.",
            "Monitoramento de condições crônicas na APS.",
            "Apoio à interoperabilidade APS-hospital.",
        ],
        "cta": "Solicitar uso da infraestrutura",
    },
    {
        "title": "Serviços de Saúde",
        "description": (
            "Suporte para acompanhar pacientes ao longo do tempo e reduzir perda de seguimento "
            "em fluxos assistenciais prioritários."
        ),
        "examples": [
            "Monitoramento longitudinal de usuários.",
            "Indicadores assistenciais para equipes.",
            "Apoio ao acompanhamento pós-alta.",
            "Continuidade do cuidado entre pontos da rede.",
        ],
        "cta": "Agendar reunião",
    },
    {
        "title": "Pesquisadores e Pós-graduação",
        "description": (
            "Ambiente multiusuário para pesquisa aplicada, análise de dados e avaliação de "
            "análises aplicadas em problemas reais do SUS."
        ),
        "examples": [
            "Ambiente seguro para análise de dados clínicos.",
            "Estudos multicêntricos e avaliação de desfechos.",
            "Avaliação de linhas de cuidado.",
            "Validação aplicada de indicadores e análises.",
        ],
        "cta": "Solicitar uso da infraestrutura",
    },
    {
        "title": "Empresas e Startups",
        "description": (
            "Espaço de validação técnica para soluções de saúde digital, sem confundir o laboratório "
            "com canal comercial ou implantação automática no SUS."
        ),
        "examples": [
            "Testes de interoperabilidade com padrões FHIR.",
            "Validação técnica em ambiente simulado.",
            "Ensaios de integração com fluxos RNDS.",
            "Ajustes antes de pilotos institucionais.",
        ],
        "cta": "Solicitar validação técnica",
    },
]

SERVICE_OFFERINGS = [
    {
        "title": "Integração de Dados Clínicos do SUS",
        "summary": (
            "Apoio para conectar sistemas e organizar fluxos de dados clínicos de forma gradual, "
            "com prioridade para problemas assistenciais concretos."
        ),
        "problem": "Dados fragmentados entre APS, serviços especializados e hospitais.",
        "examples": [
            "Integrar PEC e prontuário hospitalar.",
            "Apoiar validação de fluxos com RNDS.",
            "Mapear dados necessários para uma linha de cuidado.",
        ],
        "users": "Secretarias, serviços de saúde, ICTs e equipes de tecnologia.",
        "infra": "Integração de Dados Clínicos do SUS; Sandbox para Testes e Validação.",
        "cta": "Solicitar validação técnica",
    },
    {
        "title": "Ambiente Seguro para Dados Clínicos e Pesquisa",
        "summary": (
            "Ambiente governado para análise de dados sensíveis, com regras de acesso, registro de "
            "uso e escopo definido por projeto."
        ),
        "problem": "Necessidade de pesquisar e avaliar dados clínicos sem ampliar riscos de privacidade.",
        "examples": [
            "Analisar desfechos em condições crônicas.",
            "Avaliar linhas de cuidado em múltiplos municípios.",
            "Organizar bases para pesquisa aplicada na APS.",
        ],
        "users": "Pesquisadores, programas de pós-graduação, gestores e instituições parceiras.",
        "infra": "Ambiente Seguro para Dados Clínicos e Pesquisa.",
        "cta": "Solicitar uso da infraestrutura",
    },
    {
        "title": "Inteligência Analítica para Apoio ao Cuidado",
        "summary": (
            "Construção e validação progressiva de indicadores, painéis e análises aplicadas "
            "para apoiar decisões de gestão e cuidado."
        ),
        "problem": "Equipes precisam priorizar usuários e identificar riscos com base em dados confiáveis.",
        "examples": [
            "Identificar usuários com perda de seguimento.",
            "Priorizar acompanhamento de hipertensos sem consulta recente.",
            "Avaliar padrões de encaminhamento e retorno.",
        ],
        "users": "Gestores, equipes assistenciais, pesquisadores e programas de avaliação.",
        "infra": "Monitoramento e Gestão do Cuidado; Ambiente Seguro para Dados Clínicos e Pesquisa.",
        "cta": "Agendar reunião",
    },
    {
        "title": "Monitoramento e Gestão do Cuidado",
        "summary": (
            "Apoio à construção de painéis e rotinas de acompanhamento para condições e linhas de "
            "cuidado prioritárias."
        ),
        "problem": "Dificuldade de acompanhar longitudinalmente usuários em redes assistenciais complexas.",
        "examples": [
            "Monitorar hipertensos e diabéticos sem acompanhamento recente.",
            "Acompanhar pacientes pós-alta.",
            "Construir dashboards assistenciais para equipes e gestão.",
        ],
        "users": "Secretarias, serviços de saúde, equipes da APS e coordenações de linha de cuidado.",
        "infra": "Monitoramento e Gestão do Cuidado.",
        "cta": "Agendar reunião",
    },
    {
        "title": "Telemonitoramento e Cuidado Remoto",
        "summary": (
            "Ambiente para apoiar o desenho, teste e validação de fluxos de acompanhamento "
            "remoto integrados ao cuidado presencial."
        ),
        "problem": "Pacientes acompanhados fora da unidade podem perder vínculo e continuidade do cuidado.",
        "examples": [
            "Acompanhar pacientes com condição crônica estável.",
            "Registrar contatos e alertas de acompanhamento.",
            "Apoiar continuidade após alta hospitalar.",
        ],
        "users": "Serviços de saúde, equipes da APS, gestores e projetos de pesquisa aplicada.",
        "infra": "Telemonitoramento e Cuidado Remoto; Monitoramento e Gestão do Cuidado.",
        "cta": "Solicitar uso da infraestrutura",
    },
    {
        "title": "Sandbox para Testes e Validação",
        "summary": (
            "Ambiente controlado para testar integrações e soluções antes de uso em cenários reais, "
            "com dados simulados ou bases autorizadas."
        ),
        "problem": "Integrações em saúde precisam ser testadas antes de entrar na rotina assistencial.",
        "examples": [
            "Validar troca de dados por FHIR.",
            "Testar integração com padrões RNDS.",
            "Avaliar MVPs de saúde digital com segurança técnica.",
        ],
        "users": "Empresas, startups, ICTs, equipes públicas de tecnologia e projetos cooperativos.",
        "infra": "Sandbox para Testes e Validação.",
        "cta": "Solicitar validação técnica",
    },
    {
        "title": "Apoio Técnico em Interoperabilidade e Implementação",
        "summary": (
            "Orientação aplicada para diagnóstico, desenho de fluxos, definição de padrões e plano "
            "progressivo de implantação."
        ),
        "problem": "Instituições sabem o problema assistencial, mas precisam estruturar o caminho técnico.",
        "examples": [
            "Definir dados mínimos para uma linha de cuidado.",
            "Planejar integração APS-hospital.",
            "Apoiar equipes na leitura de padrões e requisitos.",
        ],
        "users": "Secretarias, serviços de saúde, pesquisadores, equipes técnicas e parceiros institucionais.",
        "infra": "Integração de Dados Clínicos do SUS; Sandbox para Testes e Validação.",
        "cta": "Solicitar apoio técnico",
    },
]

CONCRETE_EXAMPLES = [
    "Integrar PEC e prontuário hospitalar para apoiar continuidade do cuidado.",
    "Monitorar hipertensos sem consulta recente ou sem registro de acompanhamento.",
    "Identificar perda de seguimento em linhas de cuidado prioritárias.",
    "Acompanhar pacientes pós-alta com dados mínimos e alertas assistenciais.",
    "Validar integração com padrões FHIR/RNDS em ambiente controlado.",
    "Construir dashboards assistenciais para gestão e equipes da APS.",
]

GOVERNANCE_ITEMS = [
    "Escopo definido por projeto",
    "Autorização institucional",
    "Controle de acesso",
    "Rastreabilidade",
    "Conformidade com LGPD",
    "Uso progressivo da infraestrutura",
]

ACCESS_MODALITIES = [
    {
        "title": "Cooperação científica",
        "description": "Uso da infraestrutura em projetos de pesquisa aplicada e formação avançada.",
    },
    {
        "title": "Projetos institucionais com o SUS",
        "description": "Apoio a demandas pactuadas com secretarias, serviços e redes assistenciais.",
    },
    {
        "title": "Validação técnica de soluções digitais",
        "description": "Testes controlados de interoperabilidade, fluxos de dados e aderência a padrões.",
    },
    {
        "title": "Serviços especializados mediante avaliação de viabilidade",
        "description": "Atendimento de demandas específicas conforme escopo, capacidade operacional e governança.",
    },
]

REQUEST_TYPE_BY_CTA = {
    "Solicitar uso da infraestrutura": "Uso da infraestrutura multiusuária",
    "Solicitar apoio técnico": "Apoio técnico em interoperabilidade ou governança de dados",
    "Solicitar validação técnica": "Validação técnica de solução digital",
    "Agendar reunião": "Reunião inicial",
}


def _go_to(set_page, page_key: str = "agendamento") -> None:
    """Navegação reutilizável para ações de CTA."""
    if set_page is None:
        return
    set_page(page_key)
    st.rerun()


def _schedule_button(label: str, key: str, set_page, *, primary: bool = False) -> None:
    if st.button(
        label,
        key=key,
        type="primary" if primary else "secondary",
        use_container_width=True,
    ):
        request_type = REQUEST_TYPE_BY_CTA.get(label)
        if request_type:
            st.session_state["tipo_solicitacao_preselecionado"] = request_type
        _go_to(set_page)


def _render_bullets(items: list[str]) -> None:
    for item in items:
        st.markdown(f"- {item}")


def _render_profile_card(profile: dict[str, object], idx: int, set_page) -> None:
    with st.container(border=True):
        st.markdown(f"#### {profile['title']}")
        st.write(str(profile["description"]))
        _render_bullets(profile["examples"])  # type: ignore[arg-type]
        _schedule_button(str(profile["cta"]), f"profile_cta_{idx}", set_page)


def _render_service_card(service: dict[str, object], idx: int, set_page) -> None:
    with st.container(border=True):
        st.markdown(f"#### {service['title']}")
        st.write(str(service["summary"]))
        st.markdown(f"**Problema que resolve:** {service['problem']}")
        st.markdown("**Exemplos concretos:**")
        _render_bullets(service["examples"])  # type: ignore[arg-type]
        st.caption(f"Quem pode usar: {service['users']}")
        st.caption(f"Infraestrutura associada: {service['infra']}")
        _schedule_button(str(service["cta"]), f"service_cta_{idx}", set_page)


def _render_resource_summary(resource: dict[str, object], idx: int, set_page) -> None:
    with st.container(border=True):
        st.markdown(f"#### {resource['title']}")
        st.write(str(resource["description"]))
        st.caption(f"Usos típicos: {resource['use_cases']}")
        if st.button(
            "Solicitar uso da infraestrutura",
            key=f"resource_cta_{idx}",
            use_container_width=True,
        ):
            st.session_state["infra_preselecionada"] = resource["title"]
            st.session_state["tipo_solicitacao_preselecionado"] = (
                "Uso da infraestrutura multiusuária"
            )
            _go_to(set_page)


def _render_institutional_capacity(set_page) -> None:
    """Renderiza chamada discreta ao ecossistema institucional agregado."""
    st.markdown("### Capacidade institucional ampliada")
    with st.container(border=True):
        st.write(
            "O I³ APS opera de forma articulada com laboratórios e infraestruturas "
            "complementares da UFRN em bioinformática, inteligência artificial, processamento "
            "de alto desempenho e pesquisa aplicada em saúde digital."
        )
        if st.button(
            "Conhecer ecossistema institucional",
            key="servicos_ecossistema_institucional",
            use_container_width=True,
        ):
            _go_to(set_page, "sobre")


def _render_governance_section() -> None:
    st.markdown("### Governança e uso responsável dos dados")
    st.write(
        "O uso da infraestrutura do I³ APS será realizado com escopo definido por projeto, "
        "autorização institucional, controle de acesso, rastreabilidade das operações e "
        "conformidade com a LGPD. A integração e análise de dados ocorrerão de forma progressiva, "
        "conforme a maturidade dos sistemas, a disponibilidade operacional e os acordos "
        "estabelecidos com cada instituição parceira."
    )

    cols = st.columns(3, gap="medium")
    for idx, item in enumerate(GOVERNANCE_ITEMS):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"**{item}**")


def _render_access_modalities() -> None:
    st.markdown("### Modalidades de acesso")
    cols = st.columns(2, gap="large")
    for idx, modality in enumerate(ACCESS_MODALITIES):
        with cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"#### {modality['title']}")
                st.write(modality["description"])


def render(set_page=None) -> None:
    """Renderiza serviços com foco em utilidade prática, viabilidade e uso multiusuário."""
    st.title("Infraestrutura para integrar dados clínicos e apoiar o cuidado longitudinal no SUS")
    st.write(
        "O I³ APS apoia secretarias de saúde, serviços assistenciais, pesquisadores, programas de "
        "pós-graduação, empresas e startups na integração e no uso responsável de dados clínicos "
        "interoperáveis. O foco é resolver problemas reais do SUS com implantação progressiva, "
        "governança e uso compartilhado da infraestrutura."
    )
    st.info(
        "Infraestrutura em implantação progressiva no âmbito do projeto FINEP, com priorização "
        "de demandas alinhadas ao SUS, à pesquisa aplicada e à validação tecnológica."
    )

    hero_cta_1, hero_cta_2, _ = st.columns([1, 1, 2], gap="medium")
    with hero_cta_1:
        _schedule_button("Solicitar uso da infraestrutura", "hero_uso_infra", set_page, primary=True)
    with hero_cta_2:
        _schedule_button("Solicitar apoio técnico", "hero_apoio_tecnico", set_page)

    st.markdown("### Como o I³ APS pode ajudar você?")
    st.write(
        "A infraestrutura é multiusuária: diferentes perfis podem utilizar o laboratório para "
        "cooperação institucional, pesquisa aplicada, validação técnica e organização de dados para "
        "cuidado longitudinal."
    )
    profile_cols = st.columns(2, gap="large")
    for idx, profile in enumerate(USER_PROFILES):
        with profile_cols[idx % 2]:
            _render_profile_card(profile, idx, set_page)

    st.markdown("### Serviços prioritários")
    st.write(
        "Os serviços abaixo foram organizados por problema de uso, e não apenas pela tecnologia. "
        "Cada frente pode começar por escopos menores, com validação técnica e ampliação gradual."
    )
    for idx, service in enumerate(SERVICE_OFFERINGS):
        _render_service_card(service, idx, set_page)

    _render_governance_section()

    st.markdown("### Exemplos concretos de uso")
    example_cols = st.columns(2, gap="large")
    for idx, example in enumerate(CONCRETE_EXAMPLES):
        with example_cols[idx % 2]:
            with st.container(border=True):
                st.write(example)

    st.markdown("### Infraestrutura compartilhada")
    st.write(
        "A base operacional combina ambientes de integração, análise, monitoramento, cuidado remoto "
        "e validação. O uso da infraestrutura é definido conforme disponibilidade operacional, "
        "escopo do projeto, maturidade do fluxo de dados e critérios de governança do laboratório."
    )
    for idx, resource in enumerate(INFRASTRUCTURE_RESOURCES):
        _render_resource_summary(resource, idx, set_page)

    _render_institutional_capacity(set_page)

    _render_access_modalities()

    st.markdown("### Como utilizar o laboratório multiusuário")
    use_col_1, use_col_2 = st.columns(2, gap="large")
    with use_col_1:
        with st.container(border=True):
            st.markdown("#### Formas de uso")
            _render_bullets(
                [
                    "Projetos de pesquisa e pós-graduação.",
                    "Cooperação institucional com secretarias e serviços de saúde.",
                    "Validação técnica de integrações e soluções digitais.",
                    "Integração progressiva de sistemas e dados clínicos.",
                ]
            )
    with use_col_2:
        with st.container(border=True):
            st.markdown("#### O que o laboratório oferece")
            _render_bullets(
                [
                    "Uso compartilhado de infraestrutura especializada.",
                    "Apoio técnico em interoperabilidade e governança de dados.",
                    "Ambientes controlados para análise, testes e validação.",
                    "Acompanhamento por equipe interdisciplinar.",
                ]
            )

    final_cta_1, final_cta_2, final_cta_3 = st.columns(3, gap="medium")
    with final_cta_1:
        _schedule_button("Agendar reunião", "final_agendar_reuniao", set_page, primary=True)
    with final_cta_2:
        _schedule_button("Solicitar apoio técnico", "final_apoio_tecnico", set_page)
    with final_cta_3:
        _schedule_button("Solicitar validação técnica", "final_validacao_tecnica", set_page)
