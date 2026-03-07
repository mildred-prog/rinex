from django.core.management.base import BaseCommand
from services.models import SubService
from decimal import Decimal


class Command(BaseCommand):
    help = "Create competitive services for Rinex Shine"

    def handle(self, *args, **options):
        services = [
            # Car Care
            (
                "basic-wash",
                "car-care",
                "Basic Wash",
                "Perfect for regular maintenance",
                Decimal("19.99"),
                None,
                45,
            ),
            (
                "premium-detail",
                "car-care",
                "Premium Detail",
                "Monthly deep cleaning and maintenance",
                Decimal("35.00"),
                None,
                90,
            ),
            (
                "full-valet",
                "car-care",
                "Full Valet",
                "Complete restoration inside and out",
                Decimal("55.00"),
                None,
                120,
            ),

            # Home Cleaning
            (
                "basic-cleaning",
                "home-cleaning",
                "Basic Cleaning",
                "Regular home maintenance",
                Decimal("45.00"),
                None,
                75,
            ),
            (
                "deep-cleaning",
                "home-cleaning",
                "Deep Cleaning",
                "Thorough top-to-bottom clean",
                Decimal("75.00"),
                None,
                120,
            ),
            (
                "premium-cleaning",
                "home-cleaning",
                "Premium Cleaning",
                "Luxury cleaning service",
                Decimal("120.00"),
                None,
                180,
            ),

            # Upholstery
            (
                "basic-upholstery",
                "upholstery-fabric",
                "Basic Upholstery",
                "Refresh your furniture",
                Decimal("25.00"),
                None,
                50,
            ),
            (
                "deep-upholstery",
                "upholstery-fabric",
                "Deep Upholstery",
                "Deep stain removal",
                Decimal("45.00"),
                None,
                90,
            ),
            (
                "premium-upholstery",
                "upholstery-fabric",
                "Premium Upholstery",
                "Complete fabric restoration",
                Decimal("80.00"),
                None,
                150,
            ),

            # Office / Shop
            (
                "regular-office-cleaning",
                "office-shop-cleaning",
                "Regular Office Cleaning",
                "Weekly office maintenance",
                Decimal("65.00"),
                None,
                90,
            ),
            (
                "deep-office-cleaning",
                "office-shop-cleaning",
                "Deep Office Cleaning",
                "Monthly deep clean",
                Decimal("120.00"),
                None,
                150,
            ),
            (
                "retail-cleaning",
                "office-shop-cleaning",
                "Retail Cleaning",
                "Shop floor and window cleaning",
                Decimal("80.00"),
                None,
                120,
            ),

            # Move In / Out
            (
                "move-in-cleaning",
                "move-in-out",
                "Move In Cleaning",
                "Fresh start for your new home",
                Decimal("95.00"),
                None,
                150,
            ),
            (
                "move-out-cleaning",
                "move-in-out",
                "Move Out Cleaning",
                "Get your deposit back",
                Decimal("95.00"),
                None,
                150,
            ),
            (
                "complete-move-package",
                "move-in-out",
                "Complete Move Package",
                "Full move in/out service",
                Decimal("160.00"),
                None,
                200,
            ),
        ]

        created_count = 0
        updated_count = 0

        for slug, service_group, name, description, min_price, max_price, duration in services:
            _, created = SubService.objects.update_or_create(
                slug=slug,
                defaults={
                    "service_group": service_group,
                    "name": name,
                    "short_description": description,
                    "min_price": min_price,
                    "max_price": max_price,
                    "duration_minutes": duration,
                    "active": True,
                    "requires_address": True,
                },
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created: {name} - Starting from £{min_price}")
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Updated: {name} - Starting from £{min_price}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Services created/updated!\n"
                f"New services: {created_count}\n"
                f"Updated services: {updated_count}\n"
                f"Total: {len(services)} services"
            )
        )