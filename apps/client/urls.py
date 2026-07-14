from django.urls import path
from . import views

app_name = "client"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("overview/", views.overview, name="overview"),
    path("information/", views.information, name="information"),
    path("contract/", views.contract, name="contract"),
    path("guard/", views.guard, name="guard"),
    path("billing/", views.billing, name="billing"),
    path("report/", views.report, name="report"),
    path("setting/", views.setting, name="setting"),
]
