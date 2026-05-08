"""Página institucional sobre o Laboratório Multiusuário I³ APS."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

DOCS_DIR = Path("assets/docs")

GOVERNANCE_DOCUMENTS = [
    {
        "title": "Criação do I³ APS",
        "description": "Portaria que institui formalmente o Laboratório Multiusuário I³ APS.",
        "tokens": ("portaria 1", "cria"),
        "file_name": "portaria_criacao_i3_aps.pdf",
    },
    {
        "title": "Regimento interno",
        "description": "Documento que define finalidade, estrutura, funcionamento e regras institucionais.",
        "tokens": ("regimento",),
        "file_name": "regimento_i3_aps.pdf",
    },
    {
        "title": "Coordenação",
        "description": "Portaria de designação da coordenação do laboratório.",
        "tokens": ("portaria 2", "coorden"),
        "file_name": "portaria_coordenacao_i3_aps.pdf",
    },
    {
        "title": "Comitê Gestor",
        "description": "Portaria que institui a instância de gestão e acompanhamento institucional.",
        "tokens": ("portaria 3", "gestor"),
        "file_name": "portaria_comite_gestor_i3_aps.pdf",
    },
    {
        "title": "Comitê de Usuários",
        "description": "Portaria que institui a representação de usuários da infraestrutura multiusuária.",
        "tokens": ("portaria 4", "usua"),
        "file_name": "portaria_comite_usuarios_i3_aps.pdf",
    },
]

PARTNER_LABS = [
    {
        "name": "Centro Multiusuário de Bioinformática - BIOME",
        "description": (
            "Apoio à bioinformática, análise de dados biológicos e integração com pesquisa "
            "translacional em saúde."
        ),
        "capabilities": [
            "Bioinformática aplicada",
            "Análise de dados biológicos",
            "Pesquisa translacional",
        ],
        "url": "https://bioinfo.imd.ufrn.br/site/pt",
    },
    {
        "name": "Laboratório de Inovação em Inteligência Artificial - InovaAI Lab",
        "description": (
            "Infraestrutura e desenvolvimento aplicado em inteligência artificial, aprendizado "
            "de máquina e modelos analíticos."
        ),
        "capabilities": [
            "Inteligência artificial aplicada",
            "Modelos analíticos",
            "Validação tecnológica",
        ],
        "url": "https://inovailab.imd.ufrn.br",
    },
    {
        "name": "Núcleo de Processamento de Alto Desempenho - NPAD",
        "description": (
            "Infraestrutura computacional de alto desempenho para processamento escalável, "
            "análise intensiva de dados e suporte analítico."
        ),
        "capabilities": [
            "Computação de alto desempenho",
            "Processamento escalável",
            "Infraestrutura analítica",
        ],
        "url": "https://npad.ufrn.br/npad/bemvindo",
    },
    {
        "name": (
            "Laboratório Multiusuário de Interoperabilidade, Informação e Inteligência na "
            "Atenção Primária à Saúde - I³ APS"
        ),
        "description": (
            "Integração de dados clínicos interoperáveis, monitoramento longitudinal e apoio "
            "analítico aplicado ao SUS."
        ),
        "capabilities": [
            "Interoperabilidade clínica",
            "Dados longitudinais",
            "Monitoramento assistencial",
            "Saúde digital aplicada",
        ],
        "url": "https://www.i3aps.ccs.ufrn.br",
    },
    {
        "name": "Laboratório de Avaliação e Intervenção Respiratória - LAIRE",
        "description": (
            "Pesquisa aplicada e validação clínica em doenças respiratórias e cuidado longitudinal."
        ),
        "capabilities": [
            "Validação clínica",
            "Doenças respiratórias",
            "Pesquisa aplicada em cuidado longitudinal",
        ],
        "url": "http://laire.ufrn.br/",
    },
]


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


def _resolve_document_path(tokens: tuple[str, ...]) -> Path | None:
    """Localiza documento institucional por partes do nome do arquivo."""
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


def _render_governance_documents() -> None:
    """Renderiza documentos formais de criação e governança institucional."""
    st.markdown("### Governança institucional")
    st.write(
        "O I³ APS conta com atos formais de criação, regimento próprio e instâncias de "
        "governança que apoiam o uso multiusuário, a transparência institucional e a "
        "priorização responsável da infraestrutura."
    )

    cols = st.columns(2, gap="large")
    for idx, document in enumerate(GOVERNANCE_DOCUMENTS):
        path = _resolve_document_path(document["tokens"])
        pdf_data = _load_pdf(path)
        with cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"#### {document['title']}")
                st.write(document["description"])
                if pdf_data:
                    st.download_button(
                        "Ver documento (PDF)",
                        data=pdf_data,
                        file_name=document["file_name"],
                        mime="application/pdf",
                        use_container_width=True,
                        key=f"sobre_governance_doc_{idx}",
                    )
                    st.caption(f"Arquivo: {path.name}")
                else:
                    st.info("Documento ainda não localizado em `assets/docs`.")


def _render_partner_labs() -> None:
    """Renderiza laboratórios parceiros como ecossistema agregado."""
    st.markdown("### Laboratórios parceiros e infraestrutura agregada")
    st.write(
        "O I³ APS atua de forma articulada com laboratórios e infraestruturas parceiras da UFRN, "
        "compondo uma base agregada de capacidades em bioinformática, inteligência artificial, "
        "processamento de alto desempenho, interoperabilidade e avaliação em saúde."
    )

    st.markdown(
        """
        <style>
          .partner-lab-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
            margin-top: 8px;
          }
          .partner-lab-card {
            border: 1px solid #d8e3ec;
            border-radius: 12px;
            background: #ffffff;
            box-shadow: 0 6px 16px rgba(19, 56, 84, 0.07);
            padding: 16px;
            display: flex;
            flex-direction: column;
            min-height: 245px;
          }
          .partner-lab-name {
            margin: 0 0 8px 0;
            font: 700 18px "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
            color: #12354f;
            line-height: 1.28;
          }
          .partner-lab-description {
            margin: 0 0 10px 0;
            font: 510 14px "SF Pro Text", "Inter", "Segoe UI", Arial, sans-serif;
            color: #38556c;
            line-height: 1.45;
          }
          .partner-lab-capabilities {
            margin: 0 0 14px 0;
            padding-left: 18px;
            color: #4f6678;
            font-size: 13px;
            line-height: 1.42;
          }
          .partner-lab-capabilities li + li {
            margin-top: 4px;
          }
          .partner-lab-link {
            margin-top: auto;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            min-height: 40px;
            border: 1px solid #9ab6ca;
            border-radius: 10px;
            color: #0b3a56;
            background: #f8fbfd;
            font-weight: 650;
            text-decoration: none;
          }
          .partner-lab-link:hover {
            background: #eef5fb;
            border-color: #7ea6c2;
          }
          .partner-lab-note {
            margin: 10px 0 0 0;
            color: #50697d;
            font-size: 0.94rem;
          }
          @media (max-width: 860px) {
            .partner-lab-grid {
              grid-template-columns: 1fr;
            }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    cards_html: list[str] = []
    for lab in PARTNER_LABS:
        capabilities = "".join(
            f"<li>{capability}</li>" for capability in lab["capabilities"]
        )
        cards_html.append(
            '<article class="partner-lab-card">'
            f'<h4 class="partner-lab-name">{lab["name"]}</h4>'
            f'<p class="partner-lab-description">{lab["description"]}</p>'
            f'<ul class="partner-lab-capabilities">{capabilities}</ul>'
            f'<a class="partner-lab-link" href="{lab["url"]}" target="_blank" rel="noopener noreferrer">'
            "Acessar infraestrutura</a>"
            "</article>"
        )

    st.markdown(
        f'<div class="partner-lab-grid">{"".join(cards_html)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="partner-lab-note">As capacidades do I³ APS são ampliadas por articulação '
        "com infraestruturas complementares da UFRN, fortalecendo interoperabilidade, análise "
        "de dados, inteligência analítica e pesquisa aplicada no SUS.</p>",
        unsafe_allow_html=True,
    )


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

    _render_governance_documents()

    _render_partner_labs()

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
