from django.shortcuts import render
from services.models import SubService
from datetime import datetime, timedelta

# Optional Google Calendar import
try:
    from services.google_calendar import GoogleCalendarService
    GOOGLE_CALENDAR_AVAILABLE = True
except ImportError:
    GOOGLE_CALENDAR_AVAILABLE = False

def home(request):
    return render(request, "pages/home.html")

def about(request):
    return render(request, "pages/about.html")

def contact(request):
    return render(request, "pages/contact.html")

def car_wash_service(request):
    # Get car care subservices
    from services.models import SubService
    subservices = SubService.objects.filter(service_group='car-care', active=True)
    
    # Hardcoded version with sample calendar availability
    availability = []
    calendar_error = None
    
    if GOOGLE_CALENDAR_AVAILABLE:
        try:
            # Try to get calendar availability
            calendar_service = GoogleCalendarService()
            availability = calendar_service.get_availability(days_ahead=14)
            
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
            
        except Exception as e:
            calendar_error = str(e)
            availability_by_date = {}
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
        
        calendar_error = "Sample availability shown. Set up Google Calendar for real-time availability."
    
    context = {
        'subservices': subservices,
        'availability_by_date': availability_by_date,
        'calendar_error': calendar_error,
        'total_available_slots': sum(len(slots) for slots in availability_by_date.values()),
        'google_calendar_available': GOOGLE_CALENDAR_AVAILABLE
    }
    
    return render(request, "pages/car_care.html", context)

def home_cleaning(request):
    # Get home cleaning subservices
    from services.models import SubService
    subservices = SubService.objects.filter(service_group='home-cleaning', active=True)
    
    # Hardcoded version with sample calendar availability
    availability = []
    calendar_error = None
    
    if GOOGLE_CALENDAR_AVAILABLE:
        try:
            # Try to get calendar availability
            calendar_service = GoogleCalendarService()
            availability = calendar_service.get_availability(days_ahead=14)
            
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
            
        except Exception as e:
            calendar_error = str(e)
            availability_by_date = {}
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
        
        calendar_error = "Sample availability shown. Set up Google Calendar for real-time availability."
    
    context = {
        'subservices': subservices,
        'availability_by_date': availability_by_date,
        'calendar_error': calendar_error,
        'total_available_slots': sum(len(slots) for slots in availability_by_date.values()),
        'google_calendar_available': GOOGLE_CALENDAR_AVAILABLE
    }
    
    return render(request, "pages/home_cleaning.html", context)

def upholstery_cleaning(request):
    # Get upholstery subservices
    from services.models import SubService
    subservices = SubService.objects.filter(service_group='upholstery-fabric', active=True)
    
    # Hardcoded version with sample calendar availability
    availability = []
    calendar_error = None
    
    if GOOGLE_CALENDAR_AVAILABLE:
        try:
            # Try to get calendar availability
            calendar_service = GoogleCalendarService()
            availability = calendar_service.get_availability(days_ahead=14)
            
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
            
        except Exception as e:
            calendar_error = str(e)
            availability_by_date = {}
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
        
        calendar_error = "Sample availability shown. Set up Google Calendar for real-time availability."
    
    context = {
        'subservices': subservices,
        'availability_by_date': availability_by_date,
        'calendar_error': calendar_error,
        'total_available_slots': sum(len(slots) for slots in availability_by_date.values()),
        'google_calendar_available': GOOGLE_CALENDAR_AVAILABLE
    }
    
    return render(request, "pages/upholstery_cleaning.html", context)

def office_shop_cleaning(request):
    # Get office/shop subservices
    from services.models import SubService
    subservices = SubService.objects.filter(service_group='office-shop-cleaning', active=True)
    
    # Hardcoded version with sample calendar availability
    availability = []
    calendar_error = None
    
    if GOOGLE_CALENDAR_AVAILABLE:
        try:
            # Try to get calendar availability
            calendar_service = GoogleCalendarService()
            availability = calendar_service.get_availability(days_ahead=14)
            
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
            
        except Exception as e:
            calendar_error = str(e)
            availability_by_date = {}
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
        
        calendar_error = "Sample availability shown. Set up Google Calendar for real-time availability."
    
    context = {
        'subservices': subservices,
        'availability_by_date': availability_by_date,
        'calendar_error': calendar_error,
        'total_available_slots': sum(len(slots) for slots in availability_by_date.values()),
        'google_calendar_available': GOOGLE_CALENDAR_AVAILABLE
    }
    
    return render(request, "pages/office_shop_cleaning.html", context)

def move_in_out_cleaning(request):
    # Get move in/out subservices
    from services.models import SubService
    subservices = SubService.objects.filter(service_group='move-in-out', active=True)
    
    # Hardcoded version with sample calendar availability
    availability = []
    calendar_error = None
    
    if GOOGLE_CALENDAR_AVAILABLE:
        try:
            # Try to get calendar availability
            calendar_service = GoogleCalendarService()
            availability = calendar_service.get_availability(days_ahead=14)
            
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
            
        except Exception as e:
            calendar_error = str(e)
            availability_by_date = {}
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
        
        calendar_error = "Sample availability shown. Set up Google Calendar for real-time availability."
    
    context = {
        'subservices': subservices,
        'availability_by_date': availability_by_date,
        'calendar_error': calendar_error,
        'total_available_slots': sum(len(slots) for slots in availability_by_date.values()),
        'google_calendar_available': GOOGLE_CALENDAR_AVAILABLE
    }
    
    return render(request, "pages/move_in_out_cleaning.html", context)
