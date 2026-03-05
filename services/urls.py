from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("<slug:group_slug>/", views.service_group_page, name="service_group"),
    path("<slug:group_slug>/<slug:subservice_slug>/", views.subservice_detail, name="subservice_detail"),
]
