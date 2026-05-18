from django.urls import path

from . import views


app_name = "access_requests"

urlpatterns = [
    path("nova/", views.create_request, name="create"),
    path("admin/", views.admin_panel, name="admin_panel"),
    path("admin/<int:pk>/status/", views.update_status, name="update_status"),
]
