from django.urls import path
from . import views

app_name = "agency"

urlpatterns = [
    path("", views.show_agency, name="home"),

    path("client-page/", views.show_clients, name="show_clients"),
    path("guard-page/", views.show_guards, name="show_guards"),
    path("contract-page/", views.show_contracts, name="show_contracts"),

    path("client-profile/<int:id>/", views.client_profile, name="client_profile"),
    path("client-profile/<int:id>/overview/", views.client_overview, name="client_overview"),
    path("client-profile/<int:id>/information/", views.client_information, name="client_information"),
    path("client-profile/<int:id>/contract/", views.client_contract, name="client_contract"),
    path("client-profile/<int:id>/guard/", views.client_guard, name="client_guard"),
    path("client-profile/<int:id>/billing/", views.client_billing, name="client_billing"),
    path("client-profile/<int:id>/report/", views.client_report, name="client_report"),
    path("client-profile/create/", views.client_create, name="client_create"),
    path("client-profile/<int:id>/update/", views.client_update, name="client_update"),
    path("client-profile/<int:id>/toggle-status/", views.client_toggle_status, name="client_toggle_status"),

    path("guard-profile/<int:id>/", views.guard_profile, name="guard_profile"),
    path("guard-profile/create/", views.guard_create, name="guard_create"),  
    path("guard-profile/<int:id>/update/", views.guard_update, name="guard_update"), 
    path("guard-profile/<int:id>/toggle-status/", views.guard_toggle_status, name="guard_toggle_status"),
]