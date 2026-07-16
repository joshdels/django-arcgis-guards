# Operations
#     Overview        -> quick look
#     Deployments     -> Manage where guards are needed.
#      • Create deployment
#      • Required guards
#      • Location/Post
#     Assignments     -> Decide which guard goes to which deployment.
#      • Assign guards
#      • Replace guards
#      • Transfer guards


from django.shortcuts import render

from apps.accounts.decorators import roles_required
from apps.accounts.models import User


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def show_operations(request):
    return render(request, "operation/operation_page.html")
