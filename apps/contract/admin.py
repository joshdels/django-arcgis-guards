from django.contrib import admin

from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "contract_number",
        "client",
        "title",
        "status",
        "number_of_guards",
        "start_date",
        "end_date",
        "location",
        "created_at",
    )

    list_display_links = (
        "contract_number",
        "title",
    )

    list_filter = (
        "status",
        "start_date",
        "end_date",
        "created_at",
    )

    search_fields = (
        "contract_number",
        "title",
        "client__name",
        "location",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "contract_number",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("client",)

    date_hierarchy = "created_at"

    list_per_page = 25

    fieldsets = (
        (
            "Contract Information",
            {
                "fields": (
                    "contract_number",
                    "client",
                    "status",
                )
            },
        ),
        (
            "Details",
            {
                "fields": (
                    "title",
                    "description",
                    "location",
                    "number_of_guards",
                )
            },
        ),
        (
            "Schedule",
            {
                "fields": (
                    "start_date",
                    "end_date",
                )
            },
        ),
        (
            "Remarks",
            {"fields": ("remarks",)},
        ),
        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
