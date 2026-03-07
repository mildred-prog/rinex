from django.shortcuts import render, get_object_or_404, redirect
from services.models import SubService
from .models import Booking
from .forms import (
    CarCareBookingForm,
    HomeCleaningBookingForm,
    OfficeShopBookingForm,
    MoveInOutBookingForm,
    UpholsteryBookingForm,
)

from services.google_calendar import GoogleCalendarService


FORM_MAP = {
    "car-care": (CarCareBookingForm, "bookings/car_care_booking.html"),
    "home-cleaning": (HomeCleaningBookingForm, "bookings/home_cleaning_booking.html"),
    "office-shop-cleaning": (OfficeShopBookingForm, "bookings/office_shop_booking.html"),
    "move-in-out": (MoveInOutBookingForm, "bookings/move_in_out_booking.html"),
    "upholstery-fabric": (UpholsteryBookingForm, "bookings/upholstery_booking.html"),
}


def book_subservice(request, subservice_slug):
    print(f"Looking for service with slug: {subservice_slug}")
    subservice = get_object_or_404(SubService, slug=subservice_slug, active=True)
    print(f"Found service: {subservice.name}")
    form_cls, template_name = FORM_MAP[subservice.service_group]

    availability = []
    availability_by_date = {}
    calendar_error = None

    try:
        calendar_service = GoogleCalendarService()
        availability = calendar_service.get_availability(
            subservice=subservice,
            days_ahead=14,
        )
    except Exception:
        calendar_error = (
            "We could not load live availability right now. "
            "Please try again shortly or contact Rinex Shine directly."
        )

    for slot in availability:
        date_str = slot["date"].strftime("%Y-%m-%d")
        if date_str not in availability_by_date:
            availability_by_date[date_str] = []
        availability_by_date[date_str].append(slot)

    availability_by_date = {
        date: availability_by_date[date]
        for date in sorted(availability_by_date.keys())
    }

    if request.method == "POST":
        form = form_cls(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.subservice = subservice

            if subservice.requires_address:
                missing = []
                if not booking.postcode:
                    missing.append("postcode")
                if not booking.address_line1:
                    missing.append("address")
                if not booking.city:
                    missing.append("city")

                if missing:
                    form.add_error(None, "Address details are required for this service.")
                    return render(
                        request,
                        template_name,
                        {
                            "form": form,
                            "subservice": subservice,
                            "availability_by_date": availability_by_date,
                            "calendar_error": calendar_error,
                        },
                    )

            extra = {}
            for key in form.cleaned_data:
                if key not in form.Meta.fields:
                    extra[key] = form.cleaned_data[key]
            booking.extra = extra

            booking.save()
            return redirect("bookings:thank_you")

    else:
        form = form_cls()

        if "date" in request.GET and "selected_date" in form.fields:
            form.fields["selected_date"].initial = request.GET.get("date")

        if "start_time" in request.GET and "selected_start_time" in form.fields:
            form.fields["selected_start_time"].initial = request.GET.get("start_time")

        if "end_time" in request.GET and "selected_end_time" in form.fields:
            form.fields["selected_end_time"].initial = request.GET.get("end_time")

    return render(
        request,
        template_name,
        {
            "form": form,
            "subservice": subservice,
            "availability_by_date": availability_by_date,
            "calendar_error": calendar_error,
        },
    )


def thank_you(request):
    return render(request, "bookings/thank_you.html")