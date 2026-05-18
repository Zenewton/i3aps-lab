def navigation(request):
    """Shared navigation items used by public and authenticated templates."""
    return {
        "main_navigation": [
            {"route": "public_site:home", "label": "Início", "icon": "home"},
            {"route": "public_site:services", "label": "Serviços", "icon": "services"},
            {"route": "public_site:access", "label": "Acesso", "icon": "shield"},
            {"route": "access_requests:create", "label": "Agendar Uso", "icon": "calendar"},
            {"route": "dashboards:user_dashboard", "label": "Área do Usuário", "icon": "user"},
            {"route": "public_site:team", "label": "Equipe", "icon": "team"},
            {"route": "public_site:about", "label": "Sobre", "icon": "info"},
        ]
    }
