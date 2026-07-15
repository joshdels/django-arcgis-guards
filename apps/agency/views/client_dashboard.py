from apps.agency.helpers import render_client_tab

from apps.accounts.decorators import roles_required
from apps.accounts.models import User


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_overview(request, id):
    return render_client_tab(request, id, "partials/content_client/overview.html")


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_information(request, id):
    return render_client_tab(request, id, "partials/content_client/information.html")


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_contract(request, id):
    return render_client_tab(request, id, "partials/content_client/contract.html")


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_guard(request, id):
    return render_client_tab(request, id, "partials/content_client/guard.html")


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_billing(request, id):
    return render_client_tab(request, id, "partials/content_client/billing.html")


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_report(request, id):
    return render_client_tab(request, id, "partials/content_client/report.html")
