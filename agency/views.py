from django.shortcuts import render

# Create your views here.
# 1 for the agency  ( clients list, and guards list )
# 1 for clients (guards name, )
# 1 for guards (total time, jobs history)
  # time in/out

def show_agency(request):
    return render(request, "agency_page.html")