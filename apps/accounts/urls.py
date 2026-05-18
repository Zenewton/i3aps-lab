from django.urls import path

from .views import AccountLoginView, AccountLogoutView, register


app_name = "accounts"

urlpatterns = [
    path("entrar/", AccountLoginView.as_view(), name="login"),
    path("sair/", AccountLogoutView.as_view(), name="logout"),
    path("cadastro/", register, name="register"),
]
