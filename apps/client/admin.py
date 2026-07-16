from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "contact_person",
        "phone",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "organization",
        "contact_person",
        "email",
        "phone",
    )

    ordering = ("-created_at",)