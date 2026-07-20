from django.urls import path
from . import views

app_name = "finances"

urlpatterns = [
  path("", views.show_finances, name="show_finances"),
  path("overview/", views.finances_overview, name="finances_overview")
]