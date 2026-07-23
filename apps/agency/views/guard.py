from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q, Exists, OuterRef, Prefetch

from apps.accounts.decorators import roles_required
from apps.agency.forms import GuardForm

from apps.accounts.models import User
from apps.guard.models import Guard, GuardStatus
from apps.operations.models import AssignmentStatus, Assignment


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def guard_profile(request, id):
    # chaining, i might chunk it down
    guard = get_object_or_404(
        Guard.objects.annotate(
            on_duty=Exists(
                Assignment.objects.filter(
                    guard=OuterRef("pk"),
                    status=AssignmentStatus.ACTIVE,
                )
            )
        ).prefetch_related(
            Prefetch(
                "assignments",
                queryset=Assignment.objects.select_related(
                    "deployment",
                    "deployment__contract",
                ).order_by("-created_at"),
            )
        ),
        id=id,
    )

    context = {"guard": guard}

    return render(request, "guard/guard_profile.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def show_guards(request):
    search = request.GET.get("search")
    status = request.GET.get("status")

    guards = Guard.objects.annotate(
        on_duty=Exists(
            Assignment.objects.filter(
                guard=OuterRef("pk"),
                status=AssignmentStatus.ACTIVE,
            )
        )
    )

    if status == "available":
        guards = guards.filter(status=GuardStatus.AVAILABLE).exclude(
            assignments__status=AssignmentStatus.ACTIVE
        )

    elif status == "on_duty":
        guards = guards.filter(assignments__status=AssignmentStatus.ACTIVE).distinct()

    elif status == "leave":
        guards = guards.filter(status=GuardStatus.LEAVE)

    elif status == "suspended":
        guards = guards.filter(status=GuardStatus.SUSPENDED)

    if search:
        guards = guards.filter(
            Q(badge_number__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        )

    context = {"guards": guards, "search": search, "status": status}

    return render(
        request,
        "guard/guard_page.html",
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

    return render(request, "guard/guard_create.html", {"form": form})


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
        "guard/guard_update.html",
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
