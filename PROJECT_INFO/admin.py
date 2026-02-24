from django.contrib import admin
from .models import ProjectInfo


@admin.register(ProjectInfo)
class ProjectInfoAdmin(admin.ModelAdmin):
    list_display = ("title",)
