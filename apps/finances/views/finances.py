from django.shortcuts import render

from apps.accounts.decorators import roles_required
from apps.accounts.models import User

from apps.finances.helpers import render_finances_tab


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def show_finances(request):
    


    return render(request, "_finances_page.html")



