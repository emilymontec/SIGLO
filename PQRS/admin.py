from django.contrib import admin
from .models import PQRS


@admin.register(PQRS)
class PQRSAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "type", "status")
    list_filter = ("type", "status")
    search_fields = ("id", "client__email", "client__username", "message")
