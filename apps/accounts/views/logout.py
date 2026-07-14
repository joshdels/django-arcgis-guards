from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


class ClientLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:client_login")


class GuardLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:guard_login")


class StaffLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:staff_login")
