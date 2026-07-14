from django.urls import path
from . import views

app_name = "agency"

urlpatterns = [
    path("", views.show_agency, name="home"),

    path("client-page/", views.show_clients, name="clients"),
    path("guard-page/", views.show_guards, name="guards"),

    path("client-profile/<int:id>/", views.client_profile, name="client_profile"),
    path("client-profile/<int:id>/overview/", views.client_overview, name="client_overview"),
    path("client-profile/<int:id>/information/", views.client_information, name="client_information"),
    path("client-profile/<int:id>/contract/", views.client_contract, name="client_contract"),
    path("client-profile/<int:id>/guard/", views.client_guard, name="client_guard"),
    path("client-profile/<int:id>/billing/", views.client_billing, name="client_billing"),
    path("client-profile/<int:id>/report/", views.client_report, name="client_report"),

    path("guard-profile/<int:id>/", views.guard_profile, name="guard_profile"),
]