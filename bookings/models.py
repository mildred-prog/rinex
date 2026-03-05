from django.db import models
from services.models import SubService

class Booking(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    subservice = models.ForeignKey(SubService, on_delete=models.PROTECT, related_name="bookings")

    # Global fields (wireframe)
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    preferred_date = models.DateField()
    time_window = models.CharField(
        max_length=20,
        choices=[("morning", "Morning"), ("afternoon", "Afternoon"), ("evening", "Evening")],
    )

    # Address (conditionally required based on subservice.requires_address)
    postcode = models.CharField(max_length=20, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)

    notes = models.TextField(blank=True)
    consent = models.BooleanField(default=False)

    # Service-specific answers
    extra = models.JSONField(default=dict, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.subservice.name} ({self.preferred_date})"
