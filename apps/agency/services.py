from django.contrib.auth import get_user_model
from django.db import transaction

from apps.client.models import Client

User = get_user_model()


@transaction.atomic
def create_client(data):
    """When staff/admin adds a new client it auto creates a user auth for the client to user later"""
    contact_person = data["contact_person"].strip()
    email = data["email"].strip().lower()

    username = ".".join(contact_person.lower().split())

    original = username
    counter = 1

    while User.objects.filter(username=username).exists():
        username = f"{original}{counter}"
        counter += 1

    user = User.objects.create_user(
        username=username,
        email=email,
        password="123",
        role=User.ROLE_CLIENT,
    )

    client = Client.objects.create(
        user=user,
        name=data["name"],
        organization=data["organization"],
        location=data["location"],
        contact_person=contact_person,
        email=email,
        phone=data["phone"],
    )

    return client
