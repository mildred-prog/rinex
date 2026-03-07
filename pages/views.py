from django.shortcuts import render
from services.models import SubService

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
    
    context = {
        'subservices': subservices,
    }
    
    return render(request, "pages/car_care.html", context)

def home_cleaning(request):
    # Get home cleaning subservices
    from services.models import SubService
    subservices = SubService.objects.filter(service_group='home-cleaning', active=True)
    
    context = {
        'subservices': subservices,
    }
    
    return render(request, "pages/home_cleaning.html", context)

def upholstery_cleaning(request):
    # Get upholstery subservices
    from services.models import SubService
    subservices = SubService.objects.filter(service_group='upholstery-fabric', active=True)
    
    context = {
        'subservices': subservices,
    }
    
    return render(request, "pages/upholstery_cleaning.html", context)

def office_shop_cleaning(request):
    # Get office/shop subservices
    from services.models import SubService
    subservices = SubService.objects.filter(service_group='office-shop-cleaning', active=True)
    
    context = {
        'subservices': subservices,
    }
    
    return render(request, "pages/office_shop_cleaning.html", context)

def move_in_out_cleaning(request):
    # Get move in/out subservices
    from services.models import SubService
    subservices = SubService.objects.filter(service_group='move-in-out', active=True)
    
    context = {
        'subservices': subservices,
    }
    
    return render(request, "pages/move_in_out_cleaning.html", context)
