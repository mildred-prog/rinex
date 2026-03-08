from django.db import models
from services.models import SubService


class Booking(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    subservice = models.ForeignKey(
        SubService,
        on_delete=models.PROTECT,
        related_name="bookings"
    )

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    selected_date = models.DateField(null=True, blank=True)
    selected_start_time = models.TimeField(null=True, blank=True)
    selected_end_time = models.TimeField(null=True, blank=True)

    postcode = models.CharField(max_length=20, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)

    notes = models.TextField(blank=True)
    consent = models.BooleanField(default=False)

    extra = models.JSONField(default=dict, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    google_event_id = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.subservice.name} ({self.selected_date} {self.selected_start_time})"