from django.shortcuts import render

from apps.accounts.decorators import roles_required
from apps.accounts.models import User

from apps.operations.helpers import render_operation_tab
from apps.operations.services import get_operations_overview


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def operation_overview(request):
    context = get_operations_overview()

    return render_operation_tab(request, "overview-operation/_overview.html", context)
