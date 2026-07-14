from django.shortcuts import render

from apps.accounts.decorators import roles_required
from apps.accounts.models import User


@roles_required("accounts:guard_login", User.ROLE_GUARD)
def home(request):
    guard = request.user.guard_profile

    context = {"guard": guard}

    return render(request, "_guard.html", context)
