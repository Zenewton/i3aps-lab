from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AccessRequestForm, AccessRequestStatusForm
from .models import AccessRequest


def create_request(request):
    initial = {}
    if request.user.is_authenticated:
        profile = getattr(request.user, "profile", None)
        initial.update(
            {
                "responsavel_nome": request.user.get_full_name() or request.user.username,
                "responsavel_email": request.user.email,
                "instituicao_nome": getattr(profile, "institution", ""),
            }
        )

    form = AccessRequestForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        access_request = form.save(commit=False)
        if request.user.is_authenticated:
            access_request.user = request.user
        access_request.save()
        messages.success(
            request,
            f"Solicitação recebida. Protocolo #{access_request.pk}. A equipe do I³ APS fará a triagem.",
        )
        return redirect("dashboards:user_dashboard" if request.user.is_authenticated else "public_site:home")

    return render(request, "access_requests/request_form.html", {"form": form})


@login_required
@user_passes_test(lambda user: user.is_staff)
def admin_panel(request):
    status = request.GET.get("status") or ""
    requests_qs = AccessRequest.objects.select_related("user")
    if status:
        requests_qs = requests_qs.filter(status=status)

    metrics = {
        "total": AccessRequest.objects.count(),
        "by_status": list(AccessRequest.objects.values("status").annotate(total=Count("id")).order_by("status")),
    }
    return render(
        request,
        "admin_panel/access_requests.html",
        {
            "requests": requests_qs[:200],
            "metrics": metrics,
            "status_choices": AccessRequest.STATUS_CHOICES,
            "selected_status": status,
        },
    )


@login_required
@user_passes_test(lambda user: user.is_staff)
def update_status(request, pk):
    access_request = get_object_or_404(AccessRequest, pk=pk)
    form = AccessRequestStatusForm(request.POST or None, instance=access_request)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Solicitação #{access_request.pk} atualizada com sucesso.")
        return redirect("access_requests:admin_panel")

    return render(
        request,
        "admin_panel/update_request.html",
        {"form": form, "access_request": access_request},
    )
