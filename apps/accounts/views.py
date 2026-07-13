from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .models import User


class BaseRoleLoginView(LoginView):
    """
    Base login view that only allows a specific role to log in.
    """

    required_role = None

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.user.role != self.required_role:
            logout(self.request)
            form.add_error(None, "You are not authorized to access this portal.")
            return self.form_invalid(form)

        return response


class GuardLoginView(BaseRoleLoginView):
    template_name = "guard_login.html"
    required_role = User.ROLE_GUARD
    redirect_authenticated_user = True
    next_page = reverse_lazy("guard:dashboard")


class StaffLoginView(BaseRoleLoginView):
    template_name = "staff_login.html"
    required_role = User.ROLE_STAFF
    redirect_authenticated_user = True
    next_page = reverse_lazy("staff:dashboard")


class ClientLoginView(BaseRoleLoginView):
    template_name = "client_login.html"
    required_role = User.ROLE_CLIENT
    redirect_authenticated_user = True
    next_page = reverse_lazy("client:dashboard")


class AdminLoginView(BaseRoleLoginView):
    template_name = "admin_login.html"
    required_role = User.ROLE_ADMIN
    redirect_authenticated_user = True
    next_page = reverse_lazy("dashboard:index")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")
