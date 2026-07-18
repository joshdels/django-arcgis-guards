from django.contrib import admin

from .models import Deployment


@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "contract",
        "location",
        "required_guards",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "location",
        "contract__title",
        "contract__client__name",
    )

    list_filter = (
        "created_at",
        "contract",
    )

    ordering = ("name",)

    list_select_related = (
        "contract",
        "contract__client",
    )
