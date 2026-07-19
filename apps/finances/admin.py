from django.contrib import admin

from .models import Billing, Invoice, Payment


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = (
        "billing_number",
        "client",
        "contract",
        "billing_period_start",
        "billing_period_end",
        "total_amount",
        "status",
    )
    list_filter = (
        "status",
        "billing_date",
        "created_at",
    )
    search_fields = (
        "billing_number",
        "client__name",
        "contract__contract_number",
    )
    readonly_fields = (
        "billing_number",
        "created_at",
        "updated_at",
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "billing",
        "issue_date",
        "due_date",
        "status",
        "total_amount",
    )
    list_filter = (
        "status",
        "issue_date",
    )
    search_fields = (
        "invoice_number",
        "billing__billing_number",
        "billing__client__name",
    )
    readonly_fields = (
        "invoice_number",
        "created_at",
        "updated_at",
    )


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
        "invoice__invoice_number",
        "invoice__billing__client__name",
        "reference_number",
    )
    readonly_fields = (
        "payment_number",
        "created_at",
        "updated_at",
    )
