from django.urls import path
from . import views

app_name = "client_portal"

urlpatterns = [
    path("overview/", views.overview, name="overview"),
    path("information/", views.information, name="information"),
    path("contract/", views.contract, name="contract"),
    path("guard/", views.guard, name="guard"),
    path("finances/", views.finances, name="finances"),
    path("report/", views.report, name="report"),
    path("setting/", views.setting, name="setting"),
]
