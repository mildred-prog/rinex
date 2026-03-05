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

FORM_MAP = {
    "car-care": (CarCareBookingForm, "bookings/car_care_booking.html"),
    "home-cleaning": (HomeCleaningBookingForm, "bookings/home_cleaning_booking.html"),
    "office-shop-cleaning": (OfficeShopBookingForm, "bookings/office_shop_booking.html"),
    "move-in-out": (MoveInOutBookingForm, "bookings/move_in_out_booking.html"),
    "upholstery-fabric": (UpholsteryBookingForm, "bookings/upholstery_booking.html"),
}

def book_subservice(request, subservice_slug):
    subservice = get_object_or_404(SubService, slug=subservice_slug, active=True)

    form_cls, template_name = FORM_MAP[subservice.service_group]

    # Get availability data for the booking calendar
    availability = []
    calendar_error = None
    
    try:
        # Optional Google Calendar import
        try:
            from services.google_calendar import GoogleCalendarService
            GOOGLE_CALENDAR_AVAILABLE = True
        except ImportError:
            GOOGLE_CALENDAR_AVAILABLE = False
        
        if GOOGLE_CALENDAR_AVAILABLE:
            calendar_service = GoogleCalendarService()
            availability = calendar_service.get_availability(days_ahead=14)
        else:
            # Create sample availability for demonstration
            from datetime import datetime, timedelta
            availability_by_date = {}
            
            # Generate sample slots for the next 14 days
            for i in range(14):
                current_date = datetime.now() + timedelta(days=i)
                date_str = current_date.strftime('%Y-%m-%d')
                weekday = current_date.strftime('%A').lower()
                
                # Skip Sundays (closed)
                if weekday == 'sunday':
                    continue
                
                # Generate 2-4 sample slots per day
                import random
                num_slots = random.randint(2, 4)
                slots = []
                
                for j in range(num_slots):
                    # Generate random times between 9 AM and 5 PM
                    hour = random.randint(9, 16)
                    minute = random.choice([0, 30])
                    start_time = current_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    end_time = start_time + timedelta(hours=1, minutes=30)
                    
                    slots.append({
                        'date': current_date.date(),
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration_minutes': 90
                    })
                
                if slots:
                    availability_by_date[date_str] = slots
            
            availability = []
            for date_str, slots in availability_by_date.items():
                availability.extend(slots)
        
    except Exception as e:
        calendar_error = str(e)
    
    # Group availability by date for easier template rendering
    availability_by_date = {}
    for slot in availability:
        date_str = slot['date'].strftime('%Y-%m-%d')
        if date_str not in availability_by_date:
            availability_by_date[date_str] = []
        availability_by_date[date_str].append(slot)
    
    # Sort dates
    sorted_dates = sorted(availability_by_date.keys())
    availability_by_date = {date: availability_by_date[date] for date in sorted_dates}

    if request.method == "POST":
        form = form_cls(request.POST)
        if form.is_valid():
            booking: Booking = form.save(commit=False)
            booking.subservice = subservice

            # Enforce address if required
            if subservice.requires_address:
                missing = []
                if not booking.postcode: missing.append("postcode")
                if not booking.address_line1: missing.append("address")
                if not booking.city: missing.append("city")
                if missing:
                    form.add_error(None, "Address details are required for this service.")
                    return render(request, template_name, {
                        "form": form, 
                        "subservice": subservice,
                        "availability_by_date": availability_by_date,
                        "calendar_error": calendar_error
                    })

            # Store service-specific fields into JSON
            extra = {}
            for key in form.cleaned_data:
                if key not in form.Meta.fields:
                    extra[key] = form.cleaned_data[key]
            booking.extra = extra

            booking.save()
            return redirect("bookings:thank_you")
    else:
        form = form_cls()
        
        # Pre-fill date and time if provided in URL
        if 'date' in request.GET and 'preferred_date' in form.fields:
            form.fields['preferred_date'].initial = request.GET.get('date')
        
        if 'time' in request.GET and 'time_window' in form.fields:
            # Map time to time window
            time_str = request.GET.get('time')
            if '09:00' <= time_str <= '12:00':
                form.fields['time_window'].initial = 'morning'
            elif '12:00' < time_str <= '17:00':
                form.fields['time_window'].initial = 'afternoon'
            else:
                form.fields['time_window'].initial = 'evening'

    return render(request, template_name, {
        "form": form, 
        "subservice": subservice,
        "availability_by_date": availability_by_date,
        "calendar_error": calendar_error
    })

def thank_you(request):
    return render(request, "bookings/thank_you.html")
