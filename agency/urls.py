from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_agency, name="home"),
    path("client-page/", views.show_clients, name="clients"),
    path("guard-page/", views.show_guards, name="guards"),
    path("client-profile/<int:id>/", views.client_profile, name="client-profile"),
    path("guard-profile/<int:id>/", views.guard_profile, name="guard-profile"),
]
