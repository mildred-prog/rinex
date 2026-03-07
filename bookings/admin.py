from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "subservice",
        "selected_date",
        "selected_start_time",
        "selected_end_time",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "subservice",
        "selected_date",
        "created_at",
    )
    search_fields = (
        "full_name",
        "email",
        "phone",
        "postcode",
        "address_line1",
        "city",
    )
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)