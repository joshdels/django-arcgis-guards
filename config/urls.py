from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('apps.agency.urls')),
    path("client/", include('apps.client.urls')),
    path("guard/", include('apps.guard.urls')),
]
