from django.http import FileResponse, Http404
from django.shortcuts import render

from .content import (
    ACCESS_MODALITIES,
    CONCRETE_EXAMPLES,
    GOVERNANCE_DOCUMENTS,
    GOVERNANCE_ITEMS,
    INFRASTRUCTURE_RESOURCES,
    PARTNER_LABS,
    SERVICE_OFFERINGS,
    TEAM_BLOCKS,
    USER_PROFILES,
)
from .services import resolve_document_path


def home(request):
    resources = []
    for resource in INFRASTRUCTURE_RESOURCES:
        item = dict(resource)
        if item["title"] == "Telemonitoramento e Cuidado Remoto":
            item.update(
                {
                    "title": "Telessaúde e coordenação digital do cuidado",
                    "description": (
                        "Apoio à organização de serviços digitais integrados à APS, incluindo "
                        "acompanhamento remoto, comunicação digital, suporte assistencial e "
                        "integração entre equipes e pontos da rede."
                    ),
                    "use_cases": (
                        "Condições crônicas, pós-alta, APS-especializada e continuidade do cuidado."
                    ),
                }
            )
        resources.append(item)

    return render(
        request,
        "public_site/home.html",
        {
            "resources": resources,
            "examples": CONCRETE_EXAMPLES[:4],
        },
    )


def services(request):
    return render(
        request,
        "public_site/services.html",
        {
            "profiles": USER_PROFILES,
            "services": SERVICE_OFFERINGS,
            "resources": INFRASTRUCTURE_RESOURCES,
            "governance_items": GOVERNANCE_ITEMS,
            "modalities": ACCESS_MODALITIES,
            "examples": CONCRETE_EXAMPLES,
        },
    )


def access(request):
    return render(request, "public_site/access.html", {"documents": GOVERNANCE_DOCUMENTS})


def about(request):
    return render(
        request,
        "public_site/about.html",
        {
            "documents": GOVERNANCE_DOCUMENTS,
            "partner_labs": PARTNER_LABS,
        },
    )


def team(request):
    return render(request, "public_site/team.html", {"team_blocks": TEAM_BLOCKS})


def download_document(request, slug):
    path = resolve_document_path(slug)
    if path is None or not path.exists():
        raise Http404("Documento não localizado.")
    return FileResponse(path.open("rb"), as_attachment=True, filename=path.name, content_type="application/pdf")
