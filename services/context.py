SERVICE_GROUPS = [
    {"slug": "car-care", "title": "Car Care"},
    {"slug": "home-cleaning", "title": "Home Cleaning"},
    {"slug": "office-shop-cleaning", "title": "Office & Shop Cleaning"},
    {"slug": "move-in-out", "title": "Move In / Move Out"},
    {"slug": "upholstery-fabric", "title": "Upholstery & Fabric"},
]

SERVICE_GROUP_CHOICES = [(g["slug"], g["title"]) for g in SERVICE_GROUPS]
SERVICE_GROUP_SLUGS = {g["slug"] for g in SERVICE_GROUPS}
