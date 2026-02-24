from django.contrib import admin
from .models import Purchase, Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "total_amount", "created_at", "balance")
    list_filter = ("client", "created_at")
    search_fields = ("id", "client__email", "client__username")
    inlines = [PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "purchase", "amount", "payment_date")
    list_filter = ("payment_date",)
    search_fields = ("purchase__id", "purchase__client__email", "purchase__client__username")
