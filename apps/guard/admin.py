from django.contrib import admin
from .models import Guard


@admin.register(Guard)
class GuardAdmin(admin.ModelAdmin):
    list_display = (
        "badge_number",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "address",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "badge_number",
        "address",
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__username",
    )

    ordering = ("-created_at",)

    @admin.display(description="First Name")
    def first_name(self, obj):
        return obj.user.first_name if obj.user else "-"

    @admin.display(description="Last Name")
    def last_name(self, obj):
        return obj.user.last_name if obj.user else "-"

    @admin.display(description="Email")
    def email(self, obj):
        return obj.user.email if obj.user else "-"
