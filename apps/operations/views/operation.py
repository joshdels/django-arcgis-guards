#     Assignments     -> Decide which guard goes to which deployment.
#      • Assign guards
#      • Replace guards
#      • Transfer guards


from django.shortcuts import render

from apps.accounts.decorators import roles_required
from apps.accounts.models import User

from apps.operations.helpers import render_operation_tab


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def show_operations(request):
    return render(request, "_operation_page.html")


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def operation_overview(request):
    return render_operation_tab(request, "_partials/overview/_overview.html")
