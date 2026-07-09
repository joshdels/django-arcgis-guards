from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from apps.client.models import Client
from apps.guard.models import Guard


def show_agency(request):
    return render(request, "_agency_page.html")


def show_clients(request):
    status = request.GET.get("status")
    search = request.GET.get("search")

    clients = Client.objects.all()

    if status:
        clients = clients.filter(invoices__status=status)

    if search:
        clients = clients.filter(
            Q(name__icontains=search)
            | Q(organization__icontains=search)
            | Q(email__icontains=search)
        )

    context = {
        "clients": clients,
        "current_status": status,
        "search": search,
    }

    return render(request, "client_page.html", context)


def show_guards(request):
    status = request.GET.get("status")
    search = request.GET.get("search")

    guards = Guard.objects.all()

    if status == "active":
        guards = guards.filter(is_active=True)
    elif status == "inactive":
        guards = guards.filter(is_active=False)

    if search:
        guards = guards.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search) 
        )

    context = {"guards": guards, "current_status": status, "search": search}

    return render(
        request,
        "guard_page.html",
        context,
    )


def client_profile(request, id):
    client = get_object_or_404(Client, id=id)
    context = {"client": client}

    return render(request, "client_profile.html", context)


def guard_profile(request, id):
    guard = get_object_or_404(Guard, id=id)
    context = {"guard": guard}

    return render(request, "guard_profile.html", context)
