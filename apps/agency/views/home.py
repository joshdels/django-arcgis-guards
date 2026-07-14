from django.shortcuts import render

from apps.accounts.decorators import roles_required
from apps.accounts.models import User


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def show_agency(request):
    return render(request, "_agency_page.html")
