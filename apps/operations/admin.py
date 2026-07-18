from django.contrib import admin

from .models import Deployment, Assignment


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


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "guard",
        "deployment",
        "contract",
        "start_date",
        "end_date",
        "is_active",
        "created_at",
    )

    search_fields = (
        "guard__first_name",
        "guard__last_name",
        "guard__badge_number",
        "deployment__name",
        "deployment__location",
        "deployment__contract__contract_number",
        "deployment__contract__title",
    )

    list_filter = (
        "is_active",
        "created_at",
        "start_date",
        "deployment",
    )

    ordering = ("-start_date",)

    list_select_related = (
        "guard",
        "deployment",
        "deployment__contract",
    )

    @admin.display(description="Contract", ordering="deployment__contract")
    def contract(self, obj):
        return obj.deployment.contract.contract_number
