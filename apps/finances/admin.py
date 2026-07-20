from django.contrib import admin

from .models import Billing, Invoice, Payment


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = (
        "billing_number",
        "contract",
        "billing_period_start",
        "billing_period_end",
        "total_amount",
        "status",
    )

    list_filter = (
        "status",
        "issue_date",
        "created_at",
    )

    search_fields = (
        "billing_number",
        "contract__contract_number",
        "contract__title",
        "contract__client__name",
        "contract__client__organization",
        "contract__client__client_id",
    )

    readonly_fields = (
        "billing_number",
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "contract",
        "contract__client",
    )

    ordering = (
        "-billing_period_start",
        "-created_at",
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "billing",
        "issue_date",
        "due_date",
        "display_total_amount",
        "status",
    )

    list_filter = (
        "status",
        "issue_date",
    )

    search_fields = (
        "invoice_number",
        "billing__billing_number",
        "billing__contract__contract_number",
        "billing__contract__title",
        "billing__contract__client__name",
        "billing__contract__client__organization",
        "billing__contract__client__client_id",
    )

    readonly_fields = (
        "invoice_number",
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "billing",
        "billing__contract",
        "billing__contract__client",
    )

    ordering = ("-issue_date",)

    @admin.display(description="Total Amount")
    def display_total_amount(self, obj):
        return obj.total_amount


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_number",
        "invoice",
        "payment_date",
        "amount",
        "payment_method",
        "status",
    )

    list_filter = (
        "status",
        "payment_method",
        "payment_date",
    )

    search_fields = (
        "payment_number",
        "reference_number",
        "invoice__invoice_number",
        "invoice__billing__billing_number",
        "invoice__billing__contract__contract_number",
        "invoice__billing__contract__title",
        "invoice__billing__contract__client__name",
        "invoice__billing__contract__client__organization",
        "invoice__billing__contract__client__client_id",
    )

    readonly_fields = (
        "payment_number",
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "invoice",
        "invoice__billing",
        "invoice__billing__contract",
        "invoice__billing__contract__client",
    )

    ordering = (
        "-payment_date",
        "-created_at",
    )
