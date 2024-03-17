from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="index"),
    path("keyfile/", views.download_key_file, name="keyfile"),
    path("vm/", views.VM, name="vm"),
]