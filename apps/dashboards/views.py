from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from apps.access_requests.models import AccessRequest


@login_required
def user_dashboard(request):
    selected_status = request.GET.get("status") or ""
    requests_qs = AccessRequest.objects.visible_to(request.user)
    if selected_status:
        requests_qs = requests_qs.filter(status=selected_status)

    metrics = {
        "total": AccessRequest.objects.visible_to(request.user).count(),
        "by_status": list(
            AccessRequest.objects.visible_to(request.user)
            .values("status")
            .annotate(total=Count("id"))
            .order_by("status")
        ),
    }
    return render(
        request,
        "dashboards/user_dashboard.html",
        {
            "requests": requests_qs[:100],
            "metrics": metrics,
            "status_choices": AccessRequest.STATUS_CHOICES,
            "selected_status": selected_status,
        },
    )
