from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from .forms import RegistrationForm


class AccountLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class AccountLogoutView(LogoutView):
    pass


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboards:user_dashboard")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Cadastro realizado com sucesso.")
        return redirect("dashboards:user_dashboard")

    return render(request, "accounts/register.html", {"form": form})
