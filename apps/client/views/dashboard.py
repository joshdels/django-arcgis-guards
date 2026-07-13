from django.shortcuts import render


def dashboard(request):
    return render(request, "_client_dashboard.html")
