from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("full_name", "subservice", "preferred_date", "time_window", "status", "created_at")
    list_filter = ("status", "subservice__service_group", "subservice")
    search_fields = ("full_name", "email", "phone", "postcode")
    readonly_fields = ("created_at",)
