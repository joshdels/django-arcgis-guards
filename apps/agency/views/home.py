from django.shortcuts import render

def show_agency(request):
    return render(request, "_agency_page.html")