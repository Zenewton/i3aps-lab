"""Página institucional da equipe do I³ APS."""

from __future__ import annotations

import base64
import html
from pathlib import Path

import streamlit as st

TEAM_BLOCKS = [
    {
        "titulo": "Saúde Coletiva e APS",
        "membros": [
            {
                "nome": "Zenewton André da Silva Gama",
                "afiliacao": "UFRN – Saúde Coletiva | QualiSaúde | PPGSC",
                "area": "Saúde coletiva, qualidade do cuidado e segurança do paciente",
                "lattes": "http://lattes.cnpq.br/8885774273217562",
                "orcid": "https://orcid.org/0000-0003-0818-9680",
            },
            {
                "nome": "Tatyana Maria S. S. Rosendo",
                "afiliacao": "UFRN – Saúde Coletiva | PPGSF",
                "area": "Epidemiologia e saúde materno-infantil",
                "lattes": "http://lattes.cnpq.br/4946747115155324",
                "orcid": "https://orcid.org/0000-0003-0233-3119",
            },
            {
                "nome": "Angelo Roncalli",
                "afiliacao": "UFRN – Saúde Coletiva",
                "area": "Epidemiologia e avaliação em saúde",
                "lattes": "http://lattes.cnpq.br/0023445563721084",
                "orcid": "https://orcid.org/0000-0001-5311-697X",
            },
        ],
    },
    {
        "titulo": "Inteligência Artificial e Engenharia",
        "membros": [
            {
                "nome": "Itamir de Morais Barroca Filho",
                "afiliacao": "IMD/UFRN – Engenharia de Software",
                "area": "Sistemas distribuídos e infraestrutura digital",
                "lattes": "http://lattes.cnpq.br/1093675040121205",
                "orcid": "https://orcid.org/0000-0003-1694-8237",
            },
            {
                "nome": "Marcelo Augusto Costa Fernandes",
                "afiliacao": "UFRN – Engenharia da Computação",
                "area": "Inteligência artificial e sistemas complexos",
                "lattes": "http://lattes.cnpq.br/3475337353676349",
                "orcid": "https://orcid.org/0000-0001-7536-2506",
            },
            {
                "nome": "César Rennó Costa",
                "afiliacao": "IMD/UFRN – Bioinformática",
                "area": "Integração de dados e IA em saúde",
                "lattes": "http://lattes.cnpq.br/9222565820639401",
                "orcid": "https://orcid.org/0000-0003-0417-8108",
            },
        ],
    },
    {
        "titulo": "Linhas de cuidado (materno-infantil, oncologia, crônicas)",
        "membros": [
            {
                "nome": "Dyego Leandro Bezerra de Souza",
                "afiliacao": "UFRN – Saúde Coletiva",
                "area": "Epidemiologia e oncologia",
                "lattes": "http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4702617H2",
                "orcid": "https://orcid.org/0000-0001-8426-3120",
            },
            {
                "nome": "Viviane Souza do Amaral",
                "afiliacao": "UFRN – Saúde da Mulher",
                "area": "Saúde materna e cuidado clínico",
                "lattes": "http://lattes.cnpq.br/4440806451383783",
                "orcid": "https://orcid.org/0000-0002-9326-9054",
            },
            {
                "nome": "Ana Katherine Oliveira",
                "afiliacao": "UFRN – Saúde da Mulher",
                "area": "Ginecologia e obstetrícia",
                "lattes": "http://lattes.cnpq.br/3436756337251449",
                "orcid": "https://orcid.org/0000-0002-8351-5119",
            },
            {
                "nome": "Karla Morganna P. P. Mendonça",
                "afiliacao": "UFRN – Fisioterapia",
                "area": "Doenças respiratórias e inovação clínica",
                "lattes": "http://lattes.cnpq.br/1736384836028397",
                "orcid": "https://orcid.org/0000-0001-5734-3707",
            },
        ],
    },
]


def _resolve_lattes_logo_path() -> Path | None:
    """Resolve logo do Currículo Lattes para uso nos links dos cards."""
    candidates = [
        Path("logos/lattes-logo.jpg"),
        Path("logos/lattes-logo.png"),
        Path("logos/lattes-logo.svg"),
        Path("logo/lattes-logo.jpg"),
        Path("logo/lattes-logo.png"),
        Path("logo/lattes-logo.svg"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def _resolve_orcid_logo_path() -> Path | None:
    """Resolve ícone do ORCID para uso nos links dos cards."""
    candidates = [
        Path("logos/orcid-icone.png"),
        Path("logos/orcid-icone.jpg"),
        Path("logos/orcid-icone.svg"),
        Path("logo/orcid-icone.png"),
        Path("logo/orcid-icone.jpg"),
        Path("logo/orcid-icone.svg"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def _to_data_uri(path: Path | None) -> str | None:
    """Converte imagem local em data URI para renderização inline no HTML."""
    if path is None or not path.exists():
        return None

    mime_by_suffix = {
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }
    mime = mime_by_suffix.get(path.suffix.lower())
    if mime is None:
        return None

    try:
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    except OSError:
        return None

    return f"data:{mime};base64,{encoded}"


def _render_member_cards(
    members: list[dict[str, str]],
    lattes_logo_uri: str | None,
    orcid_logo_uri: str | None,
) -> None:
    cards_html: list[str] = []
    for member in members:
        nome = html.escape(member["nome"])
        afiliacao = html.escape(member["afiliacao"])
        area = html.escape(member["area"])
        lattes = html.escape(member["lattes"])
        orcid = html.escape(member["orcid"])
        if lattes_logo_uri:
            lattes_icon = f'<img src="{lattes_logo_uri}" alt="" class="lattes-logo" />'
        else:
            lattes_icon = '<span class="lattes-dot">L</span>'
        if orcid_logo_uri:
            orcid_icon = f'<img src="{orcid_logo_uri}" alt="" class="orcid-logo" />'
        else:
            orcid_icon = '<span class="orcid-dot">iD</span>'

        cards_html.append(
            f'<article class="team-card">'
            f'<h4 class="team-name">{nome}</h4>'
            f'<p class="team-affiliation">{afiliacao}</p>'
            f'<p class="team-area">{area}</p>'
            f'<div class="team-footer">'
            f'<div class="team-links">'
            f'<a href="{lattes}" target="_blank" rel="noopener noreferrer" aria-label="Currículo Lattes de {nome}">'
            f"{lattes_icon}<span>Lattes</span></a>"
            f'<a href="{orcid}" target="_blank" rel="noopener noreferrer" aria-label="Perfil ORCID de {nome}">'
            f"{orcid_icon}<span>ORCID</span></a>"
            "</div></div></article>"
        )

    st.markdown(
        (
            "<div class='team-grid'>"
            f"{''.join(cards_html)}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def render() -> None:
    """Renderiza página da equipe com agrupamento temático."""
    st.title("Equipe do I³ APS")
    st.write(
        "A equipe do I³-APS reúne pesquisadores líderes nas áreas de saúde coletiva, "
        "engenharia de software, inteligência artificial e epidemiologia, refletindo a "
        "natureza interdisciplinar necessária para a construção de uma infraestrutura "
        "nacional de dados clínicos interoperáveis voltada ao cuidado longitudinal no SUS."
    )
    lattes_logo_uri = _to_data_uri(_resolve_lattes_logo_path())
    orcid_logo_uri = _to_data_uri(_resolve_orcid_logo_path())

    st.markdown(
        """
        <style>
          .team-block-title {
            margin: 1rem 0 0.6rem 0;
            font: 700 1.15rem "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
            color: #12354f;
          }
          .team-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 16px;
            margin-bottom: 14px;
          }
          .team-card {
            background: #ffffff;
            border: 1px solid #d8e3ec;
            border-radius: 16px;
            padding: 18px;
            box-shadow: 0 6px 16px rgba(19, 56, 84, 0.08);
            display: flex;
            flex-direction: column;
            min-height: 210px;
            transition: transform .18s ease, box-shadow .18s ease;
          }
          .team-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(19, 56, 84, 0.14);
          }
          .team-name {
            margin: 0 0 6px 0;
            font: 600 18px "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
            color: #132f47;
            line-height: 1.3;
          }
          .team-affiliation {
            margin: 0 0 10px 0;
            font-size: 13px;
            color: #5f7385;
            line-height: 1.35;
          }
          .team-area {
            margin: 0;
            font-size: 14px;
            color: #27445d;
            line-height: 1.45;
          }
          .team-footer {
            margin-top: auto;
            padding-top: 12px;
            border-top: 1px solid #e2ebf2;
          }
          .team-links {
            display: flex;
            align-items: center;
            gap: 10px;
          }
          .team-links a {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: #1f3b53;
            text-decoration: none;
            font-size: 12px;
            font-weight: 600;
            padding: 4px 8px;
            border-radius: 8px;
          }
          .team-links a:hover {
            background: #eef5fb;
          }
          .lattes-dot {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 16px;
            height: 16px;
            border-radius: 999px;
            background: #1f5fa8;
            color: #ffd447;
            font-size: 9px;
            font-weight: 800;
            line-height: 1;
          }
          .lattes-logo {
            width: 16px;
            height: 16px;
            border-radius: 4px;
            object-fit: cover;
            display: inline-block;
          }
          .orcid-dot {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 16px;
            height: 16px;
            border-radius: 999px;
            background: #a6ce39;
            color: #fff;
            font-size: 9px;
            font-weight: 700;
            line-height: 1;
          }
          .orcid-logo {
            width: 16px;
            height: 16px;
            border-radius: 4px;
            object-fit: cover;
            display: inline-block;
          }
          @media (max-width: 1024px) {
            .team-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          }
          @media (max-width: 680px) {
            .team-grid { grid-template-columns: 1fr; }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    for block in TEAM_BLOCKS:
        st.markdown(
            f'<div class="team-block-title">{html.escape(block["titulo"])}</div>',
            unsafe_allow_html=True,
        )
        _render_member_cards(block["membros"], lattes_logo_uri, orcid_logo_uri)
