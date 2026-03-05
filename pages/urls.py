from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("car-care/", views.car_wash_service, name="car_care"),
    path("home-cleaning/", views.home_cleaning, name="home_cleaning"),
    path("upholstery-cleaning/", views.upholstery_cleaning, name="upholstery_cleaning"),
    path("office-shop-cleaning/", views.office_shop_cleaning, name="office_shop_cleaning"),
    path("move-in-out-cleaning/", views.move_in_out_cleaning, name="move_in_out_cleaning"),
   
]
