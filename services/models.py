from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from .context import SERVICE_GROUP_CHOICES


class SubService(models.Model):
    service_group = models.CharField(max_length=40, choices=SERVICE_GROUP_CHOICES)
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    short_description = models.CharField(max_length=255, blank=True)
    long_description = models.TextField(blank=True)

    requires_address = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    # ✅ Price range
    min_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Lower end of price range (e.g., 46.00)"
    )
    max_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Upper end of price range (e.g., 77.00)"
    )

    # ✅ Duration estimate (minutes)
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Estimated duration in minutes (e.g., 90)"
    )

    class Meta:
        ordering = ["service_group", "name"]

    def __str__(self):
        return f"{self.get_service_group_display()} - {self.name}"
