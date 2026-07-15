from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from apps.accounts.decorators import roles_required
from apps.accounts.models import User

from apps.contract.models import Contract
from apps.agency.forms import ContractForm


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def show_contracts(request):
    search = request.GET.get("search")
    status = request.GET.get("status")

    contracts = Contract.objects.all()

    if status:
        contracts = contracts.filter(status=status)

    if search:
        contracts = contracts.filter(
            Q(contract_number__icontains=search)
            | Q(title__icontains=search)
            | Q(client__name__icontains=search)
            | Q(client__organization__icontains=search)
        )

    context = {"contracts": contracts, "search": search, "status": status}

    return render(request, "contract/contract_page.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def contract_profile(request, id):
    contract = get_object_or_404(Contract, id=id)
    
    return render(
        request, "contract/contract_profile.html",
        {
            "contract": contract
        }
    )
    

@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def contract_create(request):
    if request.method == "POST":
        form = ContractForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Client created sucessfully.")
            return redirect("agency:show_contracts")
        
    else:
        form = ContractForm()
        
    return render(request, "contract/contract_create.html", {"form": form})


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def contract_update(request,id):
    contract = get_object_or_404(Contract, id=id)
    
    if request.method == "POST":
        form = ContractForm(request.POST, instance=contract)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Contract updated successfully.")
            return redirect(
                "agency:contract_profile",
                id=contract.id,
            )
            
    else:
        form = ContractForm(instance=contract)
        
    return render(request, "contract/contract_update.html", {"form": form, "contract": contract})