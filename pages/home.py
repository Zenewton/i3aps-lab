"""Página inicial institucional do Laboratório Multiusuário I³ APS."""

from __future__ import annotations
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

def _go_to(set_page, page_key: str) -> None:
    """Navegação reutilizável para botões de ação."""
    set_page(page_key)
    st.rerun()


def _resolve_logo_path(*patterns: str) -> Path | None:
    """Busca logo em logo/ e logos/ com nomes alternativos."""
    folders = [Path("logo"), Path("logos")]
    allowed_suffixes = {".png", ".jpg", ".jpeg", ".webp"}
    for folder in folders:
        if not folder.exists():
            continue
        files = list(folder.iterdir())
        lowered = {
            f.name.lower(): f
            for f in files
            if f.is_file() and f.suffix.lower() in allowed_suffixes
        }
        for pattern in patterns:
            for name, file_path in lowered.items():
                if pattern in name:
                    return file_path
    return None


def _resolve_i3_brand_mark_path() -> Path | None:
    """Resolve marca I³ APS para destaque no hero."""
    candidates = [
        Path("logos/logo_i3_aps_institucional_mark_v3.svg"),
        Path("logos/logo_i3_aps_institucional_mark_v2.svg"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _load_svg(path: Path | None) -> str | None:
    """Carrega conteúdo SVG para renderização inline."""
    if path is None or path.suffix.lower() != ".svg":
        return None
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def _render_home_flow_animation(animate_once: bool) -> None:
    """Renderiza diagrama com entrada única e microanimações contínuas sutis."""
    mode = "first-run" if animate_once else "static"
    html = f"""
    <div id="i3-flow" class="i3-flow {mode}">
      <div class="flow-grid">
        <div class="flow-card flow-left seq1">
          <div class="icon-wrap">
            <svg viewBox="0 0 64 64" aria-hidden="true">
              <circle cx="32" cy="32" r="24" class="icon-stroke"></circle>
              <circle cx="24" cy="27" r="3.5" class="icon-stroke"></circle>
              <circle cx="40" cy="27" r="3.5" class="icon-stroke"></circle>
              <circle cx="32" cy="38" r="3.5" class="icon-stroke"></circle>
              <path d="M26 30 L30 35 M38 30 L34 35 M27 27 L37 27" class="icon-stroke"></path>
            </svg>
          </div>
          <div class="flow-title">Rede do SUS</div>
          <div class="flow-line">APS, atenção especializada, urgência e vigilância</div>
        </div>

        <div class="flow-arrow seq2" aria-hidden="true">
          <span class="arrow-stream"></span>
          <span class="arrow-node node-start"></span>
          <span class="arrow-node node-end"></span>
        </div>

        <div class="flow-card flow-center seq3">
          <div class="center-live">
            <div class="icon-wrap center-node-wrap">
              <svg viewBox="0 0 64 64" aria-hidden="true">
                <circle cx="32" cy="32" r="25" class="icon-stroke-center-soft"></circle>
                <circle cx="32" cy="32" r="20" class="icon-stroke-center"></circle>
                <ellipse cx="32" cy="25" rx="10" ry="3.5" class="icon-stroke-center"></ellipse>
                <path d="M22 25 V32 C22 34 27 36 32 36 C37 36 42 34 42 32 V25" class="icon-stroke-center"></path>
                <path d="M22 32 V39 C22 41 27 43 32 43 C37 43 42 41 42 39 V32" class="icon-stroke-center"></path>
              </svg>
            </div>
            <div class="flow-title-center">I<span class="sup">3</span> APS</div>
          </div>
          <div class="flow-line-center">Plataforma nacional de dados clínicos interoperáveis</div>
          <div class="flow-line-center">Repositório seguro • Integração RNDS/FHIR • Serviços de IA • Governança de dados</div>
        </div>

        <div class="flow-arrow seq4" aria-hidden="true">
          <span class="arrow-stream"></span>
          <span class="arrow-node node-start"></span>
          <span class="arrow-node node-end"></span>
        </div>

        <div class="flow-card flow-right seq5">
          <div class="icon-wrap">
            <svg viewBox="0 0 64 64" aria-hidden="true">
              <circle cx="32" cy="32" r="24" class="icon-stroke"></circle>
              <path d="M18 35 H25 L31 24 L37 40 L42 32 H47" class="icon-stroke"></path>
            </svg>
          </div>
          <div class="flow-title">Cuidado longitudinal</div>
          <div class="flow-line">Decisão clínica, telemedicina e IA</div>
        </div>
      </div>
    </div>

    <style>
      .i3-flow {{
        background: linear-gradient(180deg, #f8fbff 0%, #f2f6fa 100%);
        border: 1px solid #d7e5ef;
        border-radius: 12px;
        padding: 18px;
      }}
      .flow-grid {{
        display: grid;
        grid-template-columns: 1fr 56px 1.25fr 56px 1fr;
        align-items: center;
        gap: 12px;
      }}
      .flow-card {{
        border: 1px solid #d2e2ec;
        border-radius: 12px;
        background: #ffffff;
        box-shadow: 0 10px 20px rgba(20, 58, 87, 0.10);
        min-height: 230px;
        padding: 18px 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        text-align: center;
      }}
      .flow-center {{
        min-height: 280px;
        padding: 24px 20px;
        background: linear-gradient(90deg, #0e73c9 0%, #1493da 100%);
        border-color: #0e73c9;
        position: relative;
      }}
      .center-live {{
        transform-origin: center;
        will-change: transform;
        animation: centerPulse 3.8s ease-in-out 1.35s infinite;
      }}
      .icon-wrap {{
        width: 72px;
        height: 72px;
        margin-bottom: 10px;
      }}
      .center-node-wrap {{
        position: relative;
      }}
      .center-node-wrap::after {{
        content: "";
        position: absolute;
        inset: -5px;
        border-radius: 999px;
        border: 1px solid rgba(223, 242, 255, 0.36);
        animation: ringSweep 9.5s ease-in-out infinite;
      }}
      .icon-wrap svg {{
        width: 100%;
        height: 100%;
      }}
      .icon-stroke {{
        stroke: #2c6d99;
        stroke-width: 2.8;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
      }}
      .icon-stroke-center {{
        stroke: #dff2ff;
        stroke-width: 2.8;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
      }}
      .icon-stroke-center-soft {{
        stroke: rgba(223, 242, 255, 0.52);
        stroke-width: 1.6;
        fill: none;
      }}
      .flow-title {{
        font: 700 25px "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
        color: #173e59;
        margin-bottom: 8px;
      }}
      .flow-title-center {{
        font: 700 41px "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
        color: #ffffff;
        margin-bottom: 8px;
      }}
      .flow-title-center .sup {{
        font-size: 62%;
        vertical-align: super;
      }}
      .flow-line {{
        font: 500 18px "SF Pro Text", "Inter", "Segoe UI", Arial, sans-serif;
        color: #3a5a72;
        line-height: 1.35;
      }}
      .flow-line-center {{
        font: 500 18px "SF Pro Text", "Inter", "Segoe UI", Arial, sans-serif;
        color: #eaf6ff;
        line-height: 1.35;
      }}
      .flow-arrow {{
        position: relative;
        height: 24px;
      }}
      .flow-arrow::before {{
        content: "";
        position: absolute;
        left: 0;
        right: 12px;
        top: 50%;
        transform: translateY(-50%);
        border-top: 5px solid #1186d4;
      }}
      .flow-arrow::after {{
        content: "";
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        right: -1px;
        border-top: 9px solid transparent;
        border-bottom: 9px solid transparent;
        border-left: 14px solid #1186d4;
      }}
      .arrow-stream {{
        position: absolute;
        top: 50%;
        left: 0;
        width: 42px;
        height: 5px;
        border-radius: 999px;
        transform: translate(-8px, -50%);
        background: linear-gradient(90deg, rgba(17, 134, 212, 0), rgba(208, 238, 255, 0.90), rgba(17, 134, 212, 0));
        animation: flowTravel 4.8s ease-in-out infinite;
        will-change: transform, opacity;
      }}
      .seq4 .arrow-stream {{
        animation-delay: 1.2s;
      }}
      .arrow-node {{
        position: absolute;
        top: 50%;
        width: 9px;
        height: 9px;
        margin-top: -4.5px;
        border-radius: 999px;
        background: #a6dbfb;
        opacity: 0.55;
        animation: nodeBreathe 4.2s ease-in-out infinite;
      }}
      .node-start {{
        left: -2px;
      }}
      .node-end {{
        right: 11px;
        animation-delay: 1.35s;
      }}

      .seq1, .seq2, .seq3, .seq4, .seq5 {{
        opacity: 0;
      }}
      .i3-flow.static .seq1,
      .i3-flow.static .seq2,
      .i3-flow.static .seq3,
      .i3-flow.static .seq4,
      .i3-flow.static .seq5 {{
        opacity: 1;
        transform: none;
      }}
      .i3-flow.first-run .seq1 {{ transform: translateX(-16px); }}
      .i3-flow.first-run .seq2 {{ transform: scaleX(0.85); transform-origin: left; }}
      .i3-flow.first-run .seq3 {{ transform: scale(0.96); }}
      .i3-flow.first-run .seq4 {{ transform: scaleX(0.85); transform-origin: left; }}
      .i3-flow.first-run .seq5 {{ transform: translateX(16px); }}

      .i3-flow.first-run.in-view .seq1 {{ animation: inLeft .34s ease-out forwards; animation-delay: 0s; }}
      .i3-flow.first-run.in-view .seq2 {{ animation: inArrow .15s ease-out forwards; animation-delay: .34s; }}
      .i3-flow.first-run.in-view .seq3 {{ animation: inCenter .35s ease-out forwards; animation-delay: .50s; }}
      .i3-flow.first-run.in-view .seq4 {{ animation: inArrow .15s ease-out forwards; animation-delay: .88s; }}
      .i3-flow.first-run.in-view .seq5 {{ animation: inRight .34s ease-out forwards; animation-delay: 1.04s; }}

      @keyframes inLeft {{
        from {{ opacity: 0; transform: translateX(-16px); }}
        to {{ opacity: 1; transform: translateX(0); }}
      }}
      @keyframes inArrow {{
        from {{ opacity: 0; transform: scaleX(0.85); }}
        to {{ opacity: 1; transform: scaleX(1); }}
      }}
      @keyframes inCenter {{
        from {{ opacity: 0; transform: scale(0.96); }}
        to {{ opacity: 1; transform: scale(1); }}
      }}
      @keyframes inRight {{
        from {{ opacity: 0; transform: translateX(16px); }}
        to {{ opacity: 1; transform: translateX(0); }}
      }}
      @keyframes centerPulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.02); }}
      }}
      @keyframes flowTravel {{
        0% {{ opacity: 0; transform: translate(-8px, -50%); }}
        20% {{ opacity: 0.32; }}
        65% {{ opacity: 0.52; }}
        100% {{ opacity: 0; transform: translate(calc(100% - 50px), -50%); }}
      }}
      @keyframes nodeBreathe {{
        0%, 100% {{
          opacity: 0.42;
          box-shadow: 0 0 0 0 rgba(175, 223, 251, 0);
        }}
        50% {{
          opacity: 0.88;
          box-shadow: 0 0 0 4px rgba(175, 223, 251, 0.2);
        }}
      }}
      @keyframes ringSweep {{
        0%, 100% {{
          opacity: 0.28;
          transform: rotate(0deg) scale(1);
        }}
        50% {{
          opacity: 0.52;
          transform: rotate(3deg) scale(1.015);
        }}
      }}

      @media (max-width: 860px) {{
        .i3-flow {{
          padding: 14px;
        }}
        .flow-grid {{
          grid-template-columns: 1fr;
          gap: 8px;
        }}
        .flow-card {{
          min-height: 0;
          padding: 14px 12px;
        }}
        .flow-center {{
          min-height: 0;
          padding: 16px 14px;
        }}
        .icon-wrap {{
          width: 58px;
          height: 58px;
          margin-bottom: 8px;
        }}
        .flow-title {{
          font-size: 21px;
          margin-bottom: 6px;
        }}
        .flow-title-center {{
          font-size: 34px;
          margin-bottom: 6px;
        }}
        .flow-line,
        .flow-line-center {{
          font-size: 15px;
          line-height: 1.28;
        }}
        .flow-arrow {{
          width: 0;
          height: 30px;
          margin: 0 auto;
        }}
        .flow-arrow::before {{
          left: 50%;
          right: auto;
          width: 0;
          height: 100%;
          transform: translateX(-50%);
          border-top: 0;
          border-left: 5px solid #1186d4;
        }}
        .flow-arrow::after {{
          top: auto;
          right: -6px;
          bottom: -1px;
          transform: none;
          border-left: 9px solid transparent;
          border-right: 9px solid transparent;
          border-top: 14px solid #1186d4;
          border-bottom: 0;
        }}
        .arrow-stream {{
          width: 5px;
          height: 34px;
          left: 50%;
          top: 0;
          transform: translateX(-50%);
          background: linear-gradient(180deg, rgba(17, 134, 212, 0), rgba(208, 238, 255, 0.88), rgba(17, 134, 212, 0));
          animation: flowTravelMobile 5.2s ease-in-out infinite;
        }}
        .arrow-node {{
          left: 50%;
          margin-left: -4.5px;
        }}
        .node-start {{
          top: -1px;
        }}
        .node-end {{
          top: auto;
          bottom: -1px;
          right: auto;
          animation-delay: 1.1s;
        }}
        .center-live {{
          animation-name: centerPulseMobile;
          animation-duration: 4.8s;
        }}
        .i3-flow.first-run .seq1,
        .i3-flow.first-run .seq5 {{
          transform: translateY(14px);
        }}
        @keyframes inLeft {{
          from {{ opacity: 0; transform: translateY(14px); }}
          to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes inRight {{
          from {{ opacity: 0; transform: translateY(14px); }}
          to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes centerPulseMobile {{
          0%, 100% {{ transform: scale(1); }}
          50% {{ transform: scale(1.012); }}
        }}
        @keyframes flowTravelMobile {{
          0% {{ opacity: 0; transform: translate(-50%, -6px); }}
          20% {{ opacity: 0.3; }}
          65% {{ opacity: 0.48; }}
          100% {{ opacity: 0; transform: translate(-50%, calc(100% - 26px)); }}
        }}
      }}

      @media (max-width: 520px) {{
        .i3-flow {{
          padding: 12px;
        }}
        .flow-card {{
          padding: 12px 10px;
        }}
        .flow-center {{
          padding: 14px 10px;
        }}
        .icon-wrap {{
          width: 52px;
          height: 52px;
          margin-bottom: 7px;
        }}
        .flow-title {{
          font-size: 19px;
        }}
        .flow-title-center {{
          font-size: 30px;
        }}
        .flow-line,
        .flow-line-center {{
          font-size: 14px;
          line-height: 1.26;
        }}
        .flow-arrow {{
          height: 24px;
        }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        .seq1, .seq2, .seq3, .seq4, .seq5 {{
          opacity: 1 !important;
          transform: none !important;
        }}
        .i3-flow.first-run.in-view .seq1,
        .i3-flow.first-run.in-view .seq2,
        .i3-flow.first-run.in-view .seq3,
        .i3-flow.first-run.in-view .seq4,
        .i3-flow.first-run.in-view .seq5,
        .center-live,
        .arrow-stream,
        .arrow-node,
        .center-node-wrap::after {{
          animation: none !important;
          transition: none !important;
        }}
        .arrow-stream {{
          display: none !important;
        }}
      }}
    </style>

    <script>
      (function() {{
        const root = document.getElementById("i3-flow");
        if (!root) {{
          return;
        }}

        const prefersReduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        if (prefersReduced) {{
          root.classList.add("static", "in-view");
          return;
        }}

        if (root.classList.contains("static")) {{
          if (root) root.classList.add("in-view");
          return;
        }}

        const reveal = () => root.classList.add("in-view");
        if ("IntersectionObserver" in window) {{
          const io = new IntersectionObserver((entries) => {{
            entries.forEach((entry) => {{
              if (entry.isIntersecting) {{
                reveal();
                io.disconnect();
              }}
            }});
          }}, {{ threshold: 0.35 }});
          io.observe(root);
        }} else {{
          setTimeout(reveal, 40);
        }}
      }})();
    </script>
    """
    components.html(html, height=620, scrolling=False)


def _resolve_logo_candidates() -> tuple[Path | None, Path | None, Path | None]:
    """Resolve logos institucionais principais (somente formatos de imagem)."""
    ufrn_logo = None
    qualisaude_logo = None
    imd_logo = None

    ufrn_candidates = [
        Path("logo/UFRN.png"),
        Path("logos/UFRN.png"),
        Path("logo/ufrn.png"),
        Path("logos/ufrn.png"),
    ]
    qualisaude_candidates = [
        Path("logo/logo_qualisaude_horizontal.png"),
        Path("logos/logo_qualisaude_horizontal.png"),
        Path("logo/logo_qualisaude.png"),
        Path("logos/logo_qualisaude.png"),
        Path("logo/logo horizontal qualisaude.jpg"),
        Path("logo/logo horizontal Qualisaude.jpg"),
        Path("logos/logo horizontal qualisaude.jpg"),
        Path("logos/logo horizontal Qualisaúde.jpg"),
        Path("logos/logo horizontal Qualisaúde.jpg"),
    ]
    imd_candidates = [
        Path("logo/logo_imd.png"),
        Path("logos/logo_imd.png"),
        Path("logo/imd.png"),
        Path("logos/imd.png"),
    ]

    for candidate in ufrn_candidates:
        if candidate.exists():
            ufrn_logo = candidate
            break
    for candidate in qualisaude_candidates:
        if candidate.exists():
            qualisaude_logo = candidate
            break
    for candidate in imd_candidates:
        if candidate.exists():
            imd_logo = candidate
            break

    # Fallback final por nome parcial.
    if ufrn_logo is None:
        ufrn_logo = _resolve_logo_path("ufrn")
    if qualisaude_logo is None:
        qualisaude_logo = _resolve_logo_path("qualis", "quali")
    if imd_logo is None:
        imd_logo = _resolve_logo_path("imd")

    return ufrn_logo, qualisaude_logo, imd_logo


def render_hero(set_page) -> None:
    """Renderiza hero principal com diagrama animado em largura total."""
    mark_path = _resolve_i3_brand_mark_path()
    mark_svg = _load_svg(mark_path)

    st.markdown(
        """
        <style>
          .hero-brand {
            display: flex;
            align-items: center;
            gap: 28px;
            margin-bottom: 16px;
          }
          .hero-logo-wrap {
            width: clamp(180px, 24vw, 240px);
            flex: 0 0 auto;
          }
          .hero-logo-wrap svg {
            width: 100%;
            height: auto;
            display: block;
          }
          .hero-brand-text {
            display: flex;
            flex-direction: column;
            gap: 8px;
          }
          .hero-name {
            font: 820 34px "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
            color: #0b2f49;
            line-height: 1;
            letter-spacing: 0.2px;
            text-transform: uppercase;
          }
          .hero-name .sup {
            font-size: 48%;
            vertical-align: super;
          }
          .hero-main .sup {
            font-size: 62%;
            vertical-align: super;
          }
          .hero-main {
            font: 650 42px "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
            color: #0b2f49;
            line-height: 1.1;
            letter-spacing: -0.3px;
            margin: 0;
          }
          .hero-subtitle {
            font: 600 26px "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
            color: #214862;
            margin: 16px 0 8px 0;
            line-height: 1.2;
          }
          @media (max-width: 860px) {
            .hero-brand {
              flex-direction: column;
              align-items: flex-start;
              gap: 10px;
            }
            .hero-logo-wrap {
              width: min(56vw, 210px);
            }
            .hero-name {
              font-size: 28px;
            }
            .hero-main {
              font-size: 31px;
            }
            .hero-subtitle {
              font-size: 20px;
            }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if mark_svg:
        st.markdown(
            f"""
            <div class="hero-brand">
              <div class="hero-logo-wrap">{mark_svg}</div>
              <div class="hero-brand-text">
                <div class="hero-name">I<span class="sup">3</span> APS</div>
                <h1 class="hero-main">Interoperabilidade, Informação e Inteligência na Atenção Primária à Saúde</h1>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="hero-name">I<span class="sup">3</span> APS</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-main">Interoperabilidade, Informação e Inteligência na Atenção Primária à Saúde</h1>', unsafe_allow_html=True)

    st.markdown(
        '<div class="hero-subtitle">Infraestrutura nacional de dados clínicos para coordenação do cuidado longitudinal de condições crônicas na APS</div>',
        unsafe_allow_html=True,
    )
    st.write(
        "Plataforma multiusuário para desenvolvimento, validação e operação de "
        "soluções digitais, telemedicina e inteligência artificial em ambiente real de atenção à saúde"
    )
    b1, b2 = st.columns(2)
    if b1.button("Explorar Infraestrutura", use_container_width=True, key="hero_explorar"):
        _go_to(set_page, "catalogo")
    if b2.button("Agendar Uso", use_container_width=True, key="hero_agendar"):
        _go_to(set_page, "agendamento")

    animate_once = not st.session_state.get("home_flow_animation_seen", False)
    _render_home_flow_animation(animate_once=animate_once)
    if animate_once:
        st.session_state["home_flow_animation_seen"] = True


def render_impact_section() -> None:
    """Renderiza seção de impacto no SUS."""
    st.markdown("### Impacto no SUS")
    cards = [
        (
            "Coordenação do cuidado na APS",
            "Integra informações entre níveis de atenção para continuidade do cuidado.",
        ),
        (
            "Redução de perdas de seguimento",
            "Permite monitoramento contínuo de pacientes crônicos.",
        ),
        (
            "Uso de dados em tempo real",
            "Disponibiliza informações clínicas atualizadas para tomada de decisão.",
        ),
        (
            "Apoio à decisão clínica",
            "Oferece suporte analítico baseado em dados interoperáveis.",
        ),
    ]

    row1_col1, row1_col2 = st.columns(2, gap="large")
    row2_col1, row2_col2 = st.columns(2, gap="large")
    rows = [row1_col1, row1_col2, row2_col1, row2_col2]

    for col, (label, description) in zip(rows, cards):
        with col:
            with st.container(border=True):
                st.markdown(f"#### {label}")
                st.write(description)


def render_capacity_section() -> None:
    """Renderiza seção de capacidade estratégica da infraestrutura."""
    st.markdown("### Capacidade da infraestrutura")
    items = [
        "Integra dados clínicos de múltiplos sistemas",
        "Opera em diferentes pontos da rede do SUS",
        "Garante segurança e escalabilidade",
        "Suporta uso multiusuário em ambiente real",
    ]

    col1, col2 = st.columns(2, gap="large")
    col3, col4 = st.columns(2, gap="large")
    cols = [col1, col2, col3, col4]

    for col, item in zip(cols, items):
        with col:
            with st.container(border=True):
                st.markdown(f"#### {item}")


def render_about_section() -> None:
    """Renderiza seção institucional 'Sobre o Laboratório'."""
    st.markdown("### Sobre o Laboratório")
    with st.container(border=True):
        st.markdown("**Problema:** Fragmentação de dados no SUS")
        st.markdown("**Solução:** Infraestrutura interoperável")
        st.markdown("**Função:** Apoiar cuidado longitudinal na APS")


def render_offerings() -> None:
    """Renderiza seção de serviços da infraestrutura."""
    st.markdown("### Serviços da infraestrutura")
    services = [
        "Integração de dados clínicos interoperáveis",
        "Telemedicina integrada",
        "Inteligência para decisão clínica",
        "Ambiente multiusuário para validação",
    ]

    col1, col2 = st.columns(2, gap="large")
    col3, col4 = st.columns(2, gap="large")
    cols = [col1, col2, col3, col4]

    for col, service in zip(cols, services):
        with col:
            with st.container(border=True):
                st.markdown(f"#### {service}")


def render_access_section(set_page) -> None:
    """Renderiza atalhos de acesso com destaque visual."""
    st.markdown("### Como utilizar a infraestrutura")
    b1, b2, b3 = st.columns(3, gap="large")

    if b1.button(
        "Solicitar acesso institucional",
        use_container_width=True,
        key="acesso_solicitar",
        type="primary",
    ):
        _go_to(set_page, "agendamento")
    if b2.button(
        "Conhecer casos de uso",
        use_container_width=True,
        key="acesso_casos",
        type="secondary",
    ):
        _go_to(set_page, "catalogo")
    if b3.button(
        "Área do usuário",
        use_container_width=True,
        key="acesso_area",
        type="secondary",
    ):
        _go_to(set_page, "dashboard")


def render_partner_logos() -> None:
    """Renderiza logos institucionais no rodapé da homepage."""
    ufrn_logo, qualisaude_logo, imd_logo = _resolve_logo_candidates()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Instituições que constroem esta infraestrutura")

    # Três colunas para exibir logos horizontalmente e com tamanho consistente.
    col1, col2, col3 = st.columns(3)

    with col1:
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            if ufrn_logo:
                st.image(str(ufrn_logo), width=120)
            else:
                st.warning("Imagem não encontrada")

    with col2:
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            if qualisaude_logo:
                # Usa versão horizontal preferencialmente.
                try:
                    with Image.open(qualisaude_logo) as img:
                        img_to_show = img.copy()
                        if img_to_show.height > img_to_show.width:
                            img_to_show = img_to_show.rotate(90, expand=True)
                    st.image(img_to_show, width=220)
                except Exception:
                    st.image(str(qualisaude_logo), width=220)
            else:
                st.warning("Imagem não encontrada")

    with col3:
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            if imd_logo:
                st.image(str(imd_logo), width=120)
            else:
                st.warning("Imagem não encontrada")


def render_homepage(set_page) -> None:
    """Renderiza a homepage completa com hierarquia institucional."""
    render_hero(set_page)

    st.markdown("<br><br>", unsafe_allow_html=True)
    render_impact_section()

    st.markdown("<br><br>", unsafe_allow_html=True)
    render_about_section()

    st.markdown("<br><br>", unsafe_allow_html=True)
    render_capacity_section()

    st.markdown("<br><br>", unsafe_allow_html=True)
    render_offerings()

    st.markdown("<br><br>", unsafe_allow_html=True)
    render_access_section(set_page)

    st.markdown("<br><br>", unsafe_allow_html=True)
    render_partner_logos()


def render(set_page) -> None:
    """Compatibilidade com o roteador atual do app."""
    render_homepage(set_page)
