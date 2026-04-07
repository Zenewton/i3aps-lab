"""Página inicial institucional do Laboratório Multiusuário I³ APS."""

from __future__ import annotations
import base64
import html
from pathlib import Path

import streamlit as st

def _go_to(set_page, page_key: str) -> None:
    """Navegação reutilizável para botões de ação."""
    set_page(page_key)
    st.rerun()


def _resolve_logo_path(*patterns: str) -> Path | None:
    """Busca logo em logo/ e logos/ com nomes alternativos."""
    folders = [Path("logo"), Path("logos")]
    allowed_suffixes = {".svg", ".png", ".jpg", ".jpeg", ".webp"}
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


def _render_home_flow_animation(animate_once: bool) -> None:
    """Renderiza diagrama com entrada única e microanimações contínuas sutis."""
    _ = animate_once
    mode = "static in-view"
    html = f"""
    <div class="i3-flow-shell">
      <div id="i3-flow" class="i3-flow {mode}">
      <div class="flow-grid">
        <div class="flow-card flow-left seq1">
          <div class="flow-card-content pulse-1">
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
            <div class="flow-line">APS e rede de atenção à saúde</div>
          </div>
        </div>

        <div class="flow-arrow seq2" aria-hidden="true">
          <span class="arrow-stream"></span>
          <span class="arrow-node node-start"></span>
          <span class="arrow-node node-end"></span>
        </div>

        <div class="flow-card flow-center seq3">
          <div class="flow-card-content pulse-2">
            <div class="center-live">
              <div class="flow-title-center">I<span class="sup">3</span> APS</div>
            </div>
            <div class="flow-line-center">Dados clínicos interoperáveis para coordenação do cuidado</div>
          </div>
        </div>

        <div class="flow-arrow seq4" aria-hidden="true">
          <span class="arrow-stream"></span>
          <span class="arrow-node node-start"></span>
          <span class="arrow-node node-end"></span>
        </div>

        <div class="flow-card flow-right seq5">
          <div class="flow-card-content pulse-3">
            <div class="icon-wrap">
              <svg viewBox="0 0 64 64" aria-hidden="true">
                <circle cx="32" cy="32" r="24" class="icon-stroke"></circle>
                <path d="M18 35 H25 L31 24 L37 40 L42 32 H47" class="icon-stroke"></path>
              </svg>
            </div>
            <div class="flow-title">Cuidado longitudinal</div>
            <div class="flow-line">Cuidado contínuo ao longo do tempo</div>
          </div>
        </div>
      </div>
      </div>
    </div>

    <style>
      .i3-flow-shell {{
        max-width: 1360px;
        margin: 0 auto;
      }}
      .i3-flow {{
        background: linear-gradient(180deg, #f8fbff 0%, #f2f6fa 100%);
        border: 1px solid #d7e5ef;
        border-radius: 12px;
        padding: 11px 14px;
        opacity: 0;
        transform: translateY(6px);
        transition: opacity .4s ease-out, transform .4s ease-out;
      }}
      .i3-flow.in-view {{
        opacity: 1;
        transform: translateY(0);
      }}
      .flow-grid {{
        display: grid;
        grid-template-columns: 1fr 56px 1.25fr 56px 1fr;
        align-items: center;
        gap: 14px;
        animation: gridDrift 8.8s ease-in-out infinite;
      }}
      .flow-card {{
        border: 1px solid #d2e2ec;
        border-radius: 12px;
        background: #ffffff;
        box-shadow: 0 10px 20px rgba(20, 58, 87, 0.10);
        min-height: 0;
        padding: 8px 11px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
      }}
      .flow-card-content {{
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        gap: 3px;
        border-radius: 10px;
        animation: cardPulse 5.6s ease-in-out infinite;
        will-change: filter, box-shadow;
      }}
      .flow-card-content.pulse-2 {{
        animation-delay: 1s;
      }}
      .flow-card-content.pulse-3 {{
        animation-delay: 2s;
      }}
      .flow-center {{
        min-height: 0;
        padding: 10px 13px;
        background: linear-gradient(90deg, #0b69be 0%, #128dd7 100%);
        border-color: #0e73c9;
        box-shadow: 0 10px 24px rgba(10, 94, 156, 0.22), 0 0 0 1px rgba(209, 235, 255, 0.24) inset;
        position: relative;
      }}
      .center-live {{
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 0;
        margin-bottom: 2px;
        transform-origin: center;
        will-change: transform;
        animation: centerPulse 3.8s ease-in-out 1.35s infinite;
      }}
      .icon-wrap {{
        width: 72px;
        height: 72px;
        margin-bottom: 4px;
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
      .flow-title {{
        font: 700 28px "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
        color: #173e59;
        margin-bottom: 2px;
      }}
      .flow-title-center {{
        font: 700 46px "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
        color: #ffffff;
        margin: 0 0 4px 0;
      }}
      .flow-title-center .sup {{
        font-size: 62%;
        vertical-align: super;
      }}
      .flow-line {{
        font: 520 19px "SF Pro Text", "Inter", "Segoe UI", Arial, sans-serif;
        color: #3a5a72;
        line-height: 1.35;
        margin: 0;
      }}
      .flow-line-center {{
        font: 520 19px "SF Pro Text", "Inter", "Segoe UI", Arial, sans-serif;
        color: #eaf6ff;
        line-height: 1.35;
        margin: 0;
      }}
      .flow-arrow {{
        position: relative;
        height: 20px;
      }}
      .flow-arrow::before {{
        content: "";
        position: absolute;
        left: 0;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        border-top: 3px solid #8fb6d2;
      }}
      .flow-arrow::after {{
        content: "";
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        right: -1px;
        border-top: 7px solid transparent;
        border-bottom: 7px solid transparent;
        border-left: 11px solid #8fb6d2;
      }}
      .arrow-stream {{
        position: absolute;
        top: 50%;
        left: 0;
        width: 30px;
        height: 3px;
        border-radius: 999px;
        transform: translate(-8px, -50%);
        background: linear-gradient(90deg, rgba(143, 182, 210, 0), rgba(217, 233, 245, 0.88), rgba(143, 182, 210, 0));
        animation: flowTravel 4.8s ease-in-out infinite;
        will-change: transform, opacity;
      }}
      .seq4 .arrow-stream {{
        animation-delay: 1.2s;
      }}
      .arrow-node {{
        position: absolute;
        top: 50%;
        width: 6px;
        height: 6px;
        margin-top: -3px;
        border-radius: 999px;
        background: #c6dceb;
        opacity: 0.5;
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
      @keyframes cardPulse {{
        0%,
        11%,
        100% {{
          filter: brightness(1);
          box-shadow: 0 0 0 rgba(15, 58, 88, 0);
        }}
        4% {{
          filter: brightness(1.08);
          box-shadow: 0 10px 24px rgba(15, 58, 88, 0.18);
        }}
        8% {{
          filter: brightness(1.05);
          box-shadow: 0 8px 20px rgba(15, 58, 88, 0.14);
        }}
      }}
      @keyframes gridDrift {{
        0%, 100% {{ transform: translateX(0); }}
        50% {{ transform: translateX(4px); }}
      }}

      @media (max-width: 620px) {{
        .i3-flow {{
          padding: 10px 10px;
        }}
        .flow-grid {{
          grid-template-columns: 1fr;
          gap: 8px;
          animation-name: gridDriftMobile;
          animation-duration: 9.5s;
        }}
        .flow-card {{
          min-height: 0;
          padding: 7px 9px;
        }}
        .flow-center {{
          min-height: 0;
          padding: 8px 10px;
        }}
        .icon-wrap {{
          width: 50px;
          height: 50px;
          margin-bottom: 6px;
        }}
        .flow-title {{
          font-size: 21px;
          margin-bottom: 2px;
        }}
        .flow-title-center {{
          font-size: 34px;
          margin-bottom: 3px;
        }}
        .flow-line,
        .flow-line-center {{
          font-size: 15px;
          line-height: 1.28;
        }}
        .flow-arrow {{
          width: 0;
          height: 24px;
          margin: 0 auto;
        }}
        .flow-arrow::before {{
          left: 50%;
          right: auto;
          width: 0;
          height: 100%;
          transform: translateX(-50%);
          border-top: 0;
          border-left: 3px solid #8fb6d2;
        }}
        .flow-arrow::after {{
          top: auto;
          right: -6px;
          bottom: -1px;
          transform: none;
          border-left: 7px solid transparent;
          border-right: 7px solid transparent;
          border-top: 11px solid #8fb6d2;
          border-bottom: 0;
        }}
        .arrow-stream {{
          width: 3px;
          height: 24px;
          left: 50%;
          top: 0;
          transform: translateX(-50%);
          background: linear-gradient(180deg, rgba(143, 182, 210, 0), rgba(217, 233, 245, 0.84), rgba(143, 182, 210, 0));
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
        @keyframes gridDriftMobile {{
          0%, 100% {{ transform: translateX(0); }}
          50% {{ transform: translateX(2px); }}
        }}
      }}

      @media (max-width: 520px) {{
        .i3-flow {{
          padding: 8px;
        }}
        .flow-card {{
          padding: 7px 8px;
        }}
        .flow-center {{
          padding: 8px 8px;
        }}
        .icon-wrap {{
          width: 46px;
          height: 46px;
          margin-bottom: 5px;
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
        .flow-arrow {{ height: 20px; }}
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
        .flow-card-content,
        .flow-grid,
        .center-live,
        .arrow-stream,
        .arrow-node {{
          animation: none !important;
          transition: none !important;
        }}
        .arrow-stream {{
          display: none !important;
        }}
      }}
    </style>

    """
    st.markdown(html, unsafe_allow_html=True)


def _to_data_uri(path: Path | None) -> str | None:
    """Converte arquivo de imagem local para data URI."""
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


def _resolve_logo_candidates() -> list[tuple[str, Path | None]]:
    """Resolve logos institucionais de parceiros, priorizando arquivos de maior qualidade."""
    ufrn_logo = None
    qualisaude_logo = None
    imd_logo = None
    sus_logo = None
    finep_logo = None

    ufrn_candidates = [
        Path("logos/ufrn-alta.png"),
        Path("logo/ufrn-alta.png"),
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
        Path("logos/imd-inovai.svg"),
        Path("logo/imd-inovai.svg"),
    ]
    sus_candidates = [
        Path("logos/logo-sus.svg"),
        Path("logo/logo-sus.svg"),
        Path("logos/sus-logo.svg"),
        Path("logo/sus-logo.svg"),
        Path("logos/sus-logo.png"),
        Path("logo/sus-logo.png"),
    ]
    finep_candidates = [
        Path("logos/finep-logo.svg"),
        Path("logo/finep-logo.svg"),
        Path("logos/finep-logo.png"),
        Path("logo/finep-logo.png"),
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
    for candidate in sus_candidates:
        if candidate.exists():
            sus_logo = candidate
            break
    for candidate in finep_candidates:
        if candidate.exists():
            finep_logo = candidate
            break

    # Fallback final por nome parcial.
    if ufrn_logo is None:
        ufrn_logo = _resolve_logo_path("ufrn-alta")
    if qualisaude_logo is None:
        qualisaude_logo = _resolve_logo_path("qualis", "quali")
    if imd_logo is None:
        imd_logo = _resolve_logo_path("imd-inovai", "inovai")
    if sus_logo is None:
        sus_logo = _resolve_logo_path("sus-logo", "logo-sus", "sus")
    if finep_logo is None:
        finep_logo = _resolve_logo_path("finep-logo", "finep")

    return [
        ("UFRN", ufrn_logo),
        ("Qualisaúde", qualisaude_logo),
        ("IMD-InovAI", imd_logo),
        ("SUS", sus_logo),
        ("FINEP", finep_logo),
    ]


def render_ui_refinements_style() -> None:
    """Aplica refinamentos visuais globais da homepage."""
    st.markdown(
        """
        <style>
          :root {
            --ui-blue-700: #0d5e86;
            --ui-blue-600: #1a76b1;
            --ui-text-900: #1f2a37;
            --ui-text-700: #41576b;
            --ui-border: #d8e4ee;
            --ui-surface: #ffffff;
            --ui-surface-soft: #f8fbfe;
            --ui-radius: 14px;
            --ui-shadow: 0 8px 18px rgba(10, 47, 79, 0.08);
          }

          .hero-brand-text,
          .hero-main,
          .hero-subtitle {
            max-width: 800px !important;
          }
          .hero-name {
            color: #0b3350 !important;
          }
          .hero-main {
            color: var(--ui-text-900) !important;
          }
          .hero-subtitle {
            color: var(--ui-text-700) !important;
          }

          .i3-flow,
          .flow-card,
          .infra-card,
          .problem-panel,
          .sus-impact-item,
          .i3-concept-card,
          .inst-block,
          .inst-logo-card,
          .partner-logo-card {
            border-radius: var(--ui-radius) !important;
            border-color: var(--ui-border) !important;
          }

          .flow-card,
          .infra-card,
          .problem-panel,
          .sus-impact-item,
          .i3-concept-card,
          .inst-block,
          .partner-logo-card {
            box-shadow: var(--ui-shadow) !important;
          }

          .flow-center {
            background: linear-gradient(90deg, var(--ui-blue-700) 0%, var(--ui-blue-600) 100%) !important;
            box-shadow: var(--ui-shadow), inset 0 0 0 1px rgba(215, 233, 245, 0.28) !important;
          }

          .flow-arrow::before {
            border-top-color: #9db7cb !important;
          }
          .flow-arrow::after {
            border-left-color: #9db7cb !important;
          }
          .arrow-node {
            background: #c4d8e6 !important;
          }

          .infra-grid,
          .sus-impact,
          .i3-concept-grid,
          .inst-partnerships {
            gap: 16px !important;
          }

          .infra-title,
          .problem-title,
          .sus-impact-title,
          .i3-concept-title,
          .inst-title {
            color: #1e3850 !important;
          }
          .infra-text,
          .problem-desc,
          .sus-impact-desc,
          .i3-concept-text,
          .inst-footer-text {
            color: var(--ui-text-700) !important;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """Renderiza topo enxuto com label, título e linha dos 3 Is."""
    hero_logo_candidates = [
        Path("logos/logo_i3_aps_institucional_mark_v3.svg"),
        Path("logos/logo_i3_aps_institucional_mark_v2.svg"),
    ]
    hero_logo_path = next((path for path in hero_logo_candidates if path.exists()), None)
    if hero_logo_path is None:
        hero_logo_path = _resolve_logo_path(
            "i3_aps_institucional_mark_v3",
            "i3_aps_institucional_mark_v2",
            "institucional_mark",
        )
    hero_logo_uri = _to_data_uri(hero_logo_path)

    st.markdown(
        """
        <style>
          .hero-shell {
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding: 8px 0 2px 0;
            margin-bottom: 2px;
          }
          .hero-brand {
            display: flex;
            align-items: center;
            gap: 24px;
            margin-bottom: 0;
          }
          .hero-logo-wrap {
            width: 136px;
            height: 136px;
            flex: 0 0 136px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: -4px;
          }
          .hero-logo {
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
          }
          .hero-brand-text {
            display: flex;
            flex-direction: column;
            gap: 0;
            padding-top: 0;
            max-width: 920px;
          }
          .hero-main {
            font: 680 clamp(2.05rem, 2.7vw, 2.9rem) "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
            color: #0b2f49;
            line-height: 1.14;
            letter-spacing: -0.3px;
            margin: 0;
            max-width: 920px;
            text-wrap: balance;
          }
          .hero-subtitle {
            margin: 8px 0 0 0;
            font: 520 17px "SF Pro Text", "Inter", "Segoe UI", Arial, sans-serif;
            color: #4f6375;
            line-height: 1.35;
            letter-spacing: 0.1px;
            max-width: 800px;
          }
          .hero-subtitle .sup {
            font-size: 68%;
            vertical-align: super;
          }
          @media (max-width: 860px) {
            .hero-shell {
              gap: 6px;
              padding: 8px 0 2px 0;
            }
            .hero-brand {
              gap: 16px;
            }
            .hero-logo-wrap {
              width: 112px;
              height: 112px;
              flex-basis: 112px;
            }
            .hero-main {
              font-size: 30px;
              line-height: 1.15;
              max-width: 100%;
            }
            .hero-subtitle {
              font-size: 15px;
              margin-top: 8px;
              max-width: 100%;
            }
          }
          @media (max-width: 620px) {
            .hero-brand {
              align-items: center;
              gap: 12px;
            }
            .hero-logo-wrap {
              width: 92px;
              height: 92px;
              flex-basis: 92px;
            }
            .hero-brand-text {
              gap: 0;
            }
            .hero-main {
              font-size: 22px;
              line-height: 1.16;
            }
            .hero-subtitle {
              font-size: 14px;
              margin-top: 8px;
            }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if hero_logo_uri:
        hero_logo_html = (
            '<div class="hero-logo-wrap">'
            f'<img class="hero-logo" src="{hero_logo_uri}" alt="I3 APS" />'
            "</div>"
        )
    else:
        hero_logo_html = ""

    st.markdown(
        f"""
        <div class="hero-shell">
          <div class="hero-brand">
            {hero_logo_html}
            <div class="hero-brand-text">
              <h1 class="hero-main">Infraestrutura nacional de dados clínicos interoperáveis para o cuidado na Atenção Primária à&nbsp;Saúde</h1>
              <p class="hero-subtitle">I<span class="sup">3</span>-APS: plataforma nacional para integração segura de dados clínicos, inteligência artificial e telemedicina, voltada ao cuidado longitudinal de condições crônicas na APS.</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_main_diagram() -> None:
    """Renderiza diagrama principal da home."""
    _render_home_flow_animation(animate_once=True)


def render_infrastructure_overview_section() -> None:
    """Renderiza bloco visual sobre a infraestrutura em grid 2x2."""
    st.markdown("### Sobre a infraestrutura")
    st.markdown(
        """
        <style>
          .infra-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 16px;
            margin-top: 10px;
          }
          .infra-card {
            border: 1px solid #d7e5ef;
            border-radius: 16px;
            background: #ffffff;
            box-shadow: 0 8px 18px rgba(10, 47, 79, 0.06);
            padding: 16px;
            min-height: 132px;
          }
          .infra-icon {
            width: 24px;
            height: 24px;
            margin-bottom: 8px;
            display: block;
          }
          .infra-title {
            margin: 0 0 6px 0;
            font: 700 19px "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
            color: #21384d;
          }
          .infra-text {
            margin: 0;
            font: 510 15px "SF Pro Text", "Inter", "Segoe UI", Arial, sans-serif;
            color: #43596e;
            line-height: 1.35;
          }
          @media (max-width: 760px) {
            .infra-grid { grid-template-columns: 1fr; }
          }
        </style>
        <div class="infra-grid">
          <article class="infra-card">
            <svg class="infra-icon" viewBox="0 0 24 24" fill="none" stroke="#0b6aa7" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <rect x="4" y="4" width="16" height="16" rx="3"></rect>
              <path d="M8 12h8M12 8v8"></path>
            </svg>
            <h4 class="infra-title">Integração nacional</h4>
            <p class="infra-text">Ambiente para uso compartilhado e integração de dados clínicos.</p>
          </article>

          <article class="infra-card">
            <svg class="infra-icon" viewBox="0 0 24 24" fill="none" stroke="#0c7f66" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M7 12a3 3 0 0 1 3-3h1"></path>
              <path d="M13 9h1a3 3 0 1 1 0 6h-1"></path>
              <path d="M10 12h4"></path>
            </svg>
            <h4 class="infra-title">Interoperabilidade</h4>
            <p class="infra-text">Padrões RNDS/FHIR para continuidade do cuidado em rede.</p>
          </article>

          <article class="infra-card">
            <svg class="infra-icon" viewBox="0 0 24 24" fill="none" stroke="#a11d62" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M9 7.5C7 7.5 5.5 9 5.5 11c0 1.2.6 2.2 1.5 2.8-.4 1.5.3 3 1.8 3.6"></path>
              <path d="M15 7.5c2 0 3.5 1.5 3.5 3.5 0 1.2-.6 2.2-1.5 2.8.4 1.5-.3 3-1.8 3.6"></path>
              <path d="M12 10v7M9.2 13h5.6"></path>
            </svg>
            <h4 class="infra-title">IA aplicada</h4>
            <p class="infra-text">Inteligência artificial para apoiar decisão clínica e gestão.</p>
          </article>

          <article class="infra-card">
            <svg class="infra-icon" viewBox="0 0 24 24" fill="none" stroke="#45556b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M12 3l7 4v5c0 4.2-2.7 7.8-7 9-4.3-1.2-7-4.8-7-9V7l7-4z"></path>
              <path d="M9.2 12l1.8 1.8 3.8-3.8"></path>
            </svg>
            <h4 class="infra-title">Governança de dados</h4>
            <p class="infra-text">Segurança, qualidade e uso responsável da informação em saúde.</p>
          </article>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_problem_section() -> None:
    """Renderiza problemas centrais com destaque visual e ícones."""
    st.markdown("### Problema")
    st.markdown(
        """
        <style>
          .problem-panel {
            background: #f7fafc;
            border: 1px solid #dbe7f1;
            border-radius: 16px;
            padding: 12px 14px;
          }
          .problem-row {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 10px 4px;
          }
          .problem-row + .problem-row {
            border-top: 1px solid #e5edf4;
          }
          .problem-ic {
            width: 18px;
            height: 18px;
            flex: 0 0 auto;
            margin-top: 2px;
          }
          .problem-title {
            margin: 0;
            font: 650 16px "SF Pro Text", "Inter", "Segoe UI", Arial, sans-serif;
            color: #283b4d;
          }
          .problem-desc {
            margin: 2px 0 0 0;
            font: 500 14px "SF Pro Text", "Inter", "Segoe UI", Arial, sans-serif;
            color: #526579;
            line-height: 1.35;
          }
        </style>
        <div class="problem-panel">
          <div class="problem-row">
            <svg class="problem-ic" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M12 9v4"></path><circle cx="12" cy="16.5" r="0.7"></circle>
              <path d="M10.3 4.6 2.9 17.4A2 2 0 0 0 4.6 20h14.8a2 2 0 0 0 1.7-2.6L13.7 4.6a2 2 0 0 0-3.4 0z"></path>
            </svg>
            <div>
              <p class="problem-title">Dados clínicos fragmentados no SUS</p>
              <p class="problem-desc">Informações dispersas entre serviços e níveis de atenção.</p>
            </div>
          </div>
          <div class="problem-row">
            <svg class="problem-ic" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M12 9v4"></path><circle cx="12" cy="16.5" r="0.7"></circle>
              <path d="M10.3 4.6 2.9 17.4A2 2 0 0 0 4.6 20h14.8a2 2 0 0 0 1.7-2.6L13.7 4.6a2 2 0 0 0-3.4 0z"></path>
            </svg>
            <div>
              <p class="problem-title">Sistemas não interoperáveis</p>
              <p class="problem-desc">A integração limitada compromete a continuidade do cuidado.</p>
            </div>
          </div>
          <div class="problem-row">
            <svg class="problem-ic" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M12 9v4"></path><circle cx="12" cy="16.5" r="0.7"></circle>
              <path d="M10.3 4.6 2.9 17.4A2 2 0 0 0 4.6 20h14.8a2 2 0 0 0 1.7-2.6L13.7 4.6a2 2 0 0 0-3.4 0z"></path>
            </svg>
            <div>
              <p class="problem-title">Decisão clínica sem visão longitudinal</p>
              <p class="problem-desc">Profissionais atuam sem acesso ao histórico completo do paciente.</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sus_importance_section(
    start_idx: int = 0,
    max_items: int | None = None,
    heading: str | None = "### Por que isso importa para o SUS?",
) -> None:
    """Renderiza impacto estratégico para o SUS com possibilidade de fatiamento."""
    cards = [
        (
            "Coordenação do cuidado longitudinal",
            "Melhora acompanhamento de condições crônicas ao longo da rede.",
        ),
        (
            "Gestão e vigilância com oportunidade",
            "Qualifica regulação, monitoramento e resposta com dados atualizados.",
        ),
        (
            "Mais segurança, eficiência e equidade",
            "Fortalece qualidade do cuidado com base em dados integrados.",
        ),
    ]

    end_idx = None if max_items is None else start_idx + max_items
    selected_cards = cards[start_idx:end_idx]
    if not selected_cards:
        return

    if heading:
        st.markdown(heading)

    card_items_html = []
    for title, desc in selected_cards:
        card_items_html.append(
            "<div class=\"sus-impact-item\">"
            "<svg class=\"sus-check\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#15803d\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\">"
            "<circle cx=\"12\" cy=\"12\" r=\"9\"></circle><path d=\"m8.5 12 2.4 2.4L15.8 9.6\"></path>"
            "</svg>"
            "<div>"
            f"<p class=\"sus-impact-title\">{html.escape(title)}</p>"
            f"<p class=\"sus-impact-desc\">{html.escape(desc)}</p>"
            "</div>"
            "</div>"
        )

    section_html = (
        """
        <style>
          .sus-impact {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin-top: 8px;
          }
          .sus-impact-item {
            display: flex;
            align-items: flex-start;
            gap: 9px;
            border: 1px solid #d9e7dc;
            border-radius: 14px;
            padding: 10px 12px;
            background: #ffffff;
            box-shadow: 0 6px 16px rgba(19, 56, 84, 0.05);
          }
          .sus-check {
            width: 18px;
            height: 18px;
            flex: 0 0 auto;
            margin-top: 1px;
          }
          .sus-impact-title {
            margin: 0;
            font: 650 16px "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
            color: #1f3a2a;
            line-height: 1.25;
          }
          .sus-impact-desc {
            margin: 2px 0 0 0;
            font: 500 13px "SF Pro Text", "Inter", "Segoe UI", Arial, sans-serif;
            color: #4e6a58;
            line-height: 1.3;
          }
          @media (max-width: 1120px) {
            .sus-impact {
              grid-template-columns: repeat(2, minmax(0, 1fr));
            }
          }
          @media (max-width: 760px) {
            .sus-impact {
              grid-template-columns: 1fr;
            }
          }
        </style>
        """
        + f'<div class="sus-impact">{"".join(card_items_html)}</div>'
    )
    st.markdown(section_html, unsafe_allow_html=True)


def render_concept_i3_section() -> None:
    """Renderiza conceito I3 com ícones coloridos e cards institucionais."""
    st.markdown("### Conceito I³")
    st.markdown(
        "O I³-APS é estruturado a partir de três pilares integrados:"
    )
    st.markdown(
        """
        <style>
          .i3-concept-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 16px;
          }
          .i3-concept-card {
            border: 1px solid #d7e5ef;
            border-radius: 16px;
            background: #ffffff;
            padding: 18px 18px 16px 18px;
            min-height: 210px;
            box-shadow: 0 8px 18px rgba(10, 47, 79, 0.06);
          }
          .i3-concept-head {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
          }
          .i3-concept-icon {
            width: 28px;
            height: 28px;
            flex: 0 0 auto;
          }
          .i3-concept-title {
            margin: 0;
            font: 700 23px "SF Pro Display", "Inter", "Segoe UI", Arial, sans-serif;
            color: #2f3342;
            line-height: 1.2;
          }
          .i3-concept-text {
            margin: 0;
            font: 510 18px "SF Pro Text", "Inter", "Segoe UI", Arial, sans-serif;
            color: #353a49;
            line-height: 1.45;
          }
          @media (max-width: 980px) {
            .i3-concept-grid {
              grid-template-columns: repeat(2, minmax(0, 1fr));
            }
          }
          @media (max-width: 680px) {
            .i3-concept-grid {
              grid-template-columns: 1fr;
            }
            .i3-concept-title {
              font-size: 21px;
            }
            .i3-concept-text {
              font-size: 17px;
            }
          }
        </style>
        <div class="i3-concept-grid">
          <div class="i3-concept-card">
            <div class="i3-concept-head">
              <svg class="i3-concept-icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#1f6fb5" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10.5 13.5l3-3"></path>
                <path d="M7.8 16.2a3 3 0 0 1 0-4.2l2-2a3 3 0 0 1 4.2 4.2l-.7.7"></path>
                <path d="M16.2 7.8a3 3 0 0 1 0 4.2l-2 2a3 3 0 1 1-4.2-4.2l.7-.7"></path>
              </svg>
              <h4 class="i3-concept-title">Interoperabilidade</h4>
            </div>
            <p class="i3-concept-text">Integração de sistemas e dados para continuidade do cuidado.</p>
          </div>

          <div class="i3-concept-card">
            <div class="i3-concept-head">
              <svg class="i3-concept-icon" viewBox="0 0 24 24" aria-hidden="true">
                <rect x="3" y="12" width="4" height="9" fill="#22c55e"></rect>
                <rect x="10" y="8" width="4" height="13" fill="#0ea5e9"></rect>
                <rect x="17" y="5" width="4" height="16" fill="#64748b"></rect>
              </svg>
              <h4 class="i3-concept-title">Informação</h4>
            </div>
            <p class="i3-concept-text">Dados qualificados para vigilância, gestão e pesquisa aplicada.</p>
          </div>

          <div class="i3-concept-card">
            <div class="i3-concept-head">
              <svg class="i3-concept-icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#e26aa3" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M8 6c-2 0-3.5 1.7-3.5 3.7 0 1.4.7 2.6 1.8 3.2-.6 2 .4 4.1 2.5 4.8"></path>
                <path d="M16 6c2 0 3.5 1.7 3.5 3.7 0 1.4-.7 2.6-1.8 3.2.6 2-.4 4.1-2.5 4.8"></path>
                <path d="M9 8.8c1 .6 2 .9 3 .9s2-.3 3-.9"></path>
                <path d="M12 9.7v8.1"></path>
                <path d="M9 13h6"></path>
              </svg>
              <h4 class="i3-concept-title">Inteligência</h4>
            </div>
            <p class="i3-concept-text">Modelos analíticos e IA para apoiar decisões em tempo oportuno.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
    st.markdown("### Botões de ação")
    st.markdown(
        """
        <style>
          .st-key-acesso_solicitar button,
          .st-key-acesso_casos button,
          .st-key-acesso_area button {
            min-height: 48px;
            border-radius: 10px;
            font-weight: 620;
          }
          .st-key-acesso_solicitar button[kind="primary"] {
            background: #0d5e86;
            border-color: #0d5e86;
            box-shadow: 0 8px 16px rgba(13, 94, 134, 0.20);
          }
          .st-key-acesso_solicitar button[kind="primary"]:hover {
            background: #0a4f72;
            border-color: #0a4f72;
          }
          .st-key-acesso_casos button[kind="secondary"] {
            background: #ffffff;
            border: 1px solid #8faeca;
            color: #164666;
          }
          .st-key-acesso_casos button[kind="secondary"]:hover {
            background: #eef5fb;
            border-color: #7ea6c2;
            color: #123e5a;
          }
          .st-key-acesso_area button[kind="secondary"] {
            background: #f6f9fc;
            border: 1px solid #d6e1eb;
            color: #5a6f82;
            box-shadow: none;
          }
          .st-key-acesso_area button[kind="secondary"]:hover {
            background: #eff4f8;
            border-color: #c6d3df;
            color: #4f6477;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )
    b1, b2, b3 = st.columns(3, gap="medium")

    if b1.button(
        "Solicitar acesso institucional",
        use_container_width=True,
        key="acesso_solicitar",
        type="primary",
    ):
        _go_to(set_page, "agendamento")
    if b2.button(
        "Ver infraestrutura",
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
    partner_logos = _resolve_logo_candidates()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Instituições que constroem esta infraestrutura")

    card_items: list[str] = []
    missing: list[str] = []
    for name, logo_path in partner_logos:
        logo_uri = _to_data_uri(logo_path)
        if logo_uri:
            card_items.append(
                f'<div class="partner-logo-card" title="{html.escape(name)}">'
                f'<img src="{logo_uri}" alt="{html.escape(name)}" />'
                "</div>"
            )
        else:
            missing.append(name)

    if card_items:
        logos_html = "".join(card_items)
        grid_html = (
            "<style>"
            ".partner-logo-grid{display:grid;grid-template-columns:repeat(5,minmax(140px,1fr));gap:14px;margin-top:10px;}"
            ".partner-logo-card{background:#ffffff;border:1px solid #d7e8f4;border-radius:14px;height:128px;display:flex;"
            "align-items:center;justify-content:center;padding:14px;}"
            ".partner-logo-card img{max-width:100%;max-height:80px;width:auto;height:auto;object-fit:contain;display:block;}"
            "@media (max-width:1120px){.partner-logo-grid{grid-template-columns:repeat(3,minmax(140px,1fr));}}"
            "@media (max-width:760px){.partner-logo-grid{grid-template-columns:repeat(2,minmax(130px,1fr));}}"
            "</style>"
            f'<div class="partner-logo-grid">{logos_html}</div>'
        )
        st.markdown(
            grid_html,
            unsafe_allow_html=True,
        )

    if missing:
        st.warning(f"Logo(s) não encontrada(s): {', '.join(missing)}")


def render_partnerships_section() -> None:
    """Renderiza seção final de parcerias e articulação institucional."""
    logo_map = {
        "SUS": _resolve_logo_path("logo-sus", "sus-logo", "sus"),
        "Ministério da Saúde": _resolve_logo_path("ms-logo", "ministerio", "saude"),
        "SESAP": _resolve_logo_path("sesap-logo", "sesap"),
        "ANVISA": _resolve_logo_path("anvisa-logo", "anvisa"),
        "FINEP": _resolve_logo_path("finep-logo", "finep"),
        "CNPq": _resolve_logo_path("cnpq-logo", "cnpq"),
        "CAPES": _resolve_logo_path("capes-logo", "logo-capes", "capes"),
        "UFRN": _resolve_logo_path("ufrn-alta", "ufrn"),
        "IMD-InovAI": _resolve_logo_path("imd-inovai", "inovai", "imd"),
        "Qualisaúde": _resolve_logo_path("qualisaude_horizontal", "qualisaude", "quali"),
    }

    blocks = [
        (
            "Governança do SUS",
            ["SUS", "Ministério da Saúde", "SESAP", "ANVISA"],
        ),
        (
            "Ciência e tecnologia",
            ["UFRN", "FINEP", "CNPq", "CAPES"],
        ),
        (
            "Cooperação e inovação",
            ["IMD-InovAI", "Qualisaúde"],
        ),
    ]

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown("### Parcerias e articulação institucional")

    section_html = [
        "<style>",
        ".inst-partnerships{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:10px;}",
        ".inst-block{background:#ffffff;border:1px solid #d8e4ee;border-radius:16px;padding:14px 14px 12px;box-shadow:0 8px 16px rgba(12,45,72,.05);}",
        ".inst-title{margin:0 0 10px 0;font:700 18px \"SF Pro Display\",\"Inter\",\"Segoe UI\",Arial,sans-serif;color:#1f3a4f;}",
        ".inst-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;}",
        ".inst-logo-card{height:84px;background:#f8fbfd;border:1px solid #dee8f0;border-radius:12px;display:flex;align-items:center;justify-content:center;padding:10px;}",
        ".inst-logo-card img{max-width:100%;max-height:46px;object-fit:contain;display:block;filter:grayscale(1) saturate(.45) contrast(.98);opacity:.92;}",
        ".inst-footer{margin-top:14px;padding-top:10px;border-top:1px solid #dfe8f0;display:flex;align-items:center;justify-content:center;gap:10px;}",
        ".inst-footer-text{margin:0;font:530 14px \"SF Pro Text\",\"Inter\",\"Segoe UI\",Arial,sans-serif;color:#445b6f;text-align:center;line-height:1.35;}",
        ".inst-footer-text .inst-footer-line{display:block;}",
        ".inst-footer img{height:26px;width:auto;object-fit:contain;display:block;filter:grayscale(.7) saturate(.6);opacity:.9;}",
        "@media (max-width:980px){.inst-partnerships{grid-template-columns:1fr;}.inst-grid{grid-template-columns:repeat(3,minmax(0,1fr));}}",
        "@media (max-width:640px){.inst-grid{grid-template-columns:repeat(2,minmax(0,1fr));}.inst-logo-card{height:78px;}}",
        "</style>",
        '<section class="inst-partnerships">',
    ]

    missing: list[str] = []

    for title, items in blocks:
        section_html.append('<article class="inst-block">')
        section_html.append(f'<h4 class="inst-title">{html.escape(title)}</h4>')
        section_html.append('<div class="inst-grid">')
        for name in items:
            logo_uri = _to_data_uri(logo_map.get(name))
            if logo_uri:
                section_html.append(
                    f'<div class="inst-logo-card" title="{html.escape(name)}">'
                    f'<img src="{logo_uri}" alt="{html.escape(name)}" />'
                    "</div>"
                )
            else:
                missing.append(name)
        section_html.append("</div>")
        section_html.append("</article>")

    section_html.append("</section>")

    footer_text_html = (
        '<p class="inst-footer-text">'
        '<span class="inst-footer-line">Projeto coordenado pelo Centro de Ciências da Saúde (CCS)</span>'
        '<span class="inst-footer-line">Universidade Federal do Rio Grande do Norte (UFRN)</span>'
        "</p>"
    )

    ufrn_uri = _to_data_uri(logo_map.get("UFRN"))
    if ufrn_uri:
        section_html.append(
            '<div class="inst-footer">'
            f"{footer_text_html}"
            f'<img src="{ufrn_uri}" alt="Universidade Federal do Rio Grande do Norte" />'
            "</div>"
        )
    else:
        section_html.append(
            '<div class="inst-footer">'
            f"{footer_text_html}"
            "</div>"
        )
        missing.append("UFRN")

    st.markdown("".join(section_html), unsafe_allow_html=True)

    if missing:
        uniq_missing = ", ".join(sorted(set(missing)))
        st.caption(f"Alguns arquivos de logo não foram encontrados: {uniq_missing}.")


def render_homepage(set_page) -> None:
    """Renderiza homepage com foco em comunicação visual e leitura rápida."""
    render_ui_refinements_style()
    render_hero()

    render_main_diagram()

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    render_sus_importance_section()

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    render_concept_i3_section()

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    render_infrastructure_overview_section()

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    render_problem_section()

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    render_access_section(set_page)

    render_partnerships_section()


def render(set_page) -> None:
    """Compatibilidade com o roteador atual do app."""
    render_homepage(set_page)
