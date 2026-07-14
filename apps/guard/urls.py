from django.urls import path
from . import views

app_name = "guard"

urlpatterns = [path("", views.home, name="home")]
