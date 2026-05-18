from django.urls import path

from . import views


app_name = "public_site"

urlpatterns = [
    path("", views.home, name="home"),
    path("servicos/", views.services, name="services"),
    path("acesso/", views.access, name="access"),
    path("sobre/", views.about, name="about"),
    path("equipe/", views.team, name="team"),
    path("documentos/<slug:slug>/", views.download_document, name="download_document"),
]
