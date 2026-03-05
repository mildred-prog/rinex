from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("services/", include(("services.urls", "services"), namespace="services")),
    path("book/", include(("bookings.urls", "bookings"), namespace="bookings")),
]
