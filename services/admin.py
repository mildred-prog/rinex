from django.contrib import admin
from .models import SubService

@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "service_group", "min_price", "max_price", "duration_minutes", "active")
    list_filter = ("service_group", "active", "requires_address")
    search_fields = ("name", "short_description", "long_description")
    prepopulated_fields = {"slug": ("name",)}
