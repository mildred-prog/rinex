from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("thank-you/", views.thank_you, name="thank_you"),
    path("<slug:subservice_slug>/", views.book_subservice, name="book_subservice"),
]
