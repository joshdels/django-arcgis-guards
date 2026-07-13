from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from apps.guard.models import Guard


def guard_profile(request, id):
    guard = get_object_or_404(Guard, id=id)
    context = {"guard": guard}

    return render(request, "guard_profile.html", context)


def show_guards(request):
    search = request.GET.get("search")

    guards = Guard.objects.all()

    if search:
        guards = guards.filter(
            Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(user__username__icontains=search)
            | Q(user__email__icontains=search)
        )

    context = {"guards": guards, "search": search}

    return render(
        request,
        "guard_page.html",
        context,
    )
