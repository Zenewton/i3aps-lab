"""Catálogo de infraestrutura do Laboratório Multiusuário I³ APS."""

import streamlit as st

RESOURCES = [
    {
        "title": "Ambiente Seguro de Dados Clínicos",
        "description": "Espaço protegido para tratamento e análise de dados sensíveis em conformidade com LGPD.",
        "use_cases": "Vigilância em saúde, estudos epidemiológicos, avaliação de desfechos.",
    },
    {
        "title": "Plataforma de Interoperabilidade (FHIR/API)",
        "description": "Serviços de integração padronizada para troca de dados clínicos entre sistemas.",
        "use_cases": "Integração PEC e prontuários, troca entre APS e atenção especializada.",
    },
    {
        "title": "Ambiente de Inteligência Artificial",
        "description": "Infraestrutura para experimentação, treinamento e validação de modelos de IA em saúde.",
        "use_cases": "Estratificação de risco, previsão de demanda, apoio à decisão clínica.",
    },
    {
        "title": "Sandbox de Saúde Digital",
        "description": "Ambiente de testes para soluções digitais com dados simulados e APIs controladas.",
        "use_cases": "Validação de MVPs, testes de conformidade, provas de conceito.",
    },
    {
        "title": "Plataforma de Monitoramento do Cuidado",
        "description": "Dashboards e indicadores para acompanhamento longitudinal do cuidado na APS.",
        "use_cases": "Gestão de linhas de cuidado, monitoramento de indicadores assistenciais.",
    },
    {
        "title": "Plataforma de Telemonitoramento",
        "description": "Suporte a acompanhamento remoto e comunicação estruturada entre equipes e usuários.",
        "use_cases": "Condições crônicas, monitoramento domiciliar, continuidade do cuidado.",
    },
]


def render(set_page) -> None:
    """Renderiza catálogo com cards de recursos."""
    st.title("Catálogo do Laboratório Multiusuário")
    st.write(
        "Explore os recursos disponíveis no laboratório e solicite uso conforme "
        "sua necessidade institucional."
    )

    for resource in RESOURCES:
        with st.container(border=True):
            st.markdown(f"### 🧩 {resource['title']}")
            st.write(resource["description"])
            st.markdown(f"**Casos de uso:** {resource['use_cases']}")
            if st.button(f"Solicitar acesso: {resource['title']}", key=f"request_{resource['title']}"):
                st.session_state["infra_preselecionada"] = resource["title"]
                set_page("agendamento")
                st.rerun()
