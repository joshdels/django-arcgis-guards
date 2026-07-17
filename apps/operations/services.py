from django.db.models import Prefetch

from .models import Deployment

from apps.contract.models import Contract

def create_deployment(**data):
    return Deployment.objects.create(**data)


def update_deployment(deployment, **data):
    for field, value in data.items():
        setattr(deployment, field, value)

    deployment.save()
    return deployment


def delete_deployment(deployment):
    deployment.delete()


def activate_deployment(deployment):
    deployment.is_active = True
    deployment.save(update_fields=["is_active"])


def deactivate_deployment(deployment):
    deployment.is_active = False
    deployment.save(update_fields=["is_active"])


