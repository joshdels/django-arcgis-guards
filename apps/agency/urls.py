from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_agency, name="home"),

    path("client-page/", views.show_clients, name="clients"),
    path("guard-page/", views.show_guards, name="guards"),

    path("client-profile/<int:id>/", views.client_profile, name="client-profile"),

    path("client-profile/<int:id>/dashboard/", views.client_dashboard, name="client_dashboard"),
    path("client-profile/<int:id>/information/", views.client_information, name="client_information"),
    path("client-profile/<int:id>/guard/", views.client_guard, name="client_guard"),
    path("client-profile/<int:id>/billing/", views.client_billing, name="client_billing"),
    path("client-profile/<int:id>/report/", views.client_report, name="client_report"),

    path("guard-profile/<int:id>/", views.guard_profile, name="guard-profile"),
]