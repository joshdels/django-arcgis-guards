from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.accounts.urls")),
    path("agency/", include('apps.agency.urls')),
    path("client-dashboard/", include('apps.client.urls')),
    path("guard-dashboard/", include('apps.guard.urls')),
]
