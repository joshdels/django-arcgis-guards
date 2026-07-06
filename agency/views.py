from django.shortcuts import render, get_object_or_404
from .models import Client, Guard


def show_agency(request):
    return render(request, "agency_page.html")


def show_clients(request):
    clients = Client.objects.all()

    context = {"clients": clients}

    return render(request, "client_page.html", context)


def show_guards(request):
    guards = Guard.objects.all()

    context = {
        "guards": guards,
    }

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
