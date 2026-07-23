from django.db.models import Q

from apps.client.models import Client


def get_clients(search=None, status=None):
    clients = Client.objects.all()

    if search:
        clients = clients.filter(
            Q(name__icontains=search)
            | Q(organization__icontains=search)
            | Q(client_id__icontains=search)
        )

    if status == "active":
        clients = clients.filter(is_active=True)
    elif status == "inactive":
        clients = clients.filter(is_active=False)

    return clients
