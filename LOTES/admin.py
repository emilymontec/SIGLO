from django.contrib import admin
from .models import Stage, Lot


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ("code", "stage", "area_m2", "price", "status")
    list_filter = ("stage", "status")
    search_fields = ("code",)
