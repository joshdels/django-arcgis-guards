from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q

from apps.accounts.decorators import roles_required
from apps.accounts.models import User

from apps.agency.forms import GuardForm

from apps.guard.models import Guard


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def guard_profile(request, id):
    guard = get_object_or_404(Guard, id=id)
    context = {"guard": guard}

    return render(request, "guard_profile.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def show_guards(request):
    search = request.GET.get("search")
    status = request.GET.get("status")

    guards = Guard.objects.all()

    if status == "active":
        guards = guards.filter(is_active=True)

    elif status == "inactive":
        guards = guards.filter(is_active=False)

    if search:
        guards = guards.filter(
            Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(user__username__icontains=search)
            | Q(user__email__icontains=search)
        )

    context = {"guards": guards, "search": search, "is_active": status}

    return render(
        request,
        "guard_page.html",
        context,
    )


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def guard_create(request):
    if request.method == "POST":
        form = GuardForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Form created sucessfully")
            return redirect("agency:show_guards")

    else:
        form = GuardForm()

    return render(request, "guard_create.html", {"form": form})


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def guard_update(request, id):
    guard = get_object_or_404(Guard, id=id)

    if request.method == "POST":
        form = GuardForm(request.POST, instance=guard)

        if form.is_valid():
            form.save()
            messages.success(request, "Guard updated successfully.")
            return redirect("agency:guard_profile", id=guard.id)

    else:
        form = GuardForm(instance=guard)

    return render(
        request,
        "guard_update.html",
        {
            "form": form,
            "guard": guard,
        },
    )


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def guard_toggle_status(request, id):
    guard = get_object_or_404(Guard, id=id)

    guard.is_active = not guard.is_active
    guard.save()

    if guard.is_active:
        messages.success(request, "Guard activated successfully.")
    else:
        messages.success(request, "Guard deactivated successfully.")

    return redirect("agency:guard_profile", id=guard.id)
