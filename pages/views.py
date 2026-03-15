from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from services.models import SubService
from .forms import ContactForm

def home(request):
    return render(request, "pages/home.html")

def about(request):
    return render(request, "pages/about.html")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get cleaned data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            city = form.cleaned_data['city']
            service_type = form.cleaned_data['service_type']
            message = form.cleaned_data['message']
            
            # Create email content
            email_subject = f'New Contact Form Submission from {first_name} {last_name}'
            email_message = f'''
            New Contact Form Submission
            
            Name: {first_name} {last_name}
            Email: {email}
            Phone: {phone}
            City: {city}
            Service Type: {service_type}
            
            Message:
            {message}
            '''
            
            # Send email
            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['rinexshine@gmail.com'],  # Your email
                    fail_silently=False,
                )
                messages.success(request, 'Thank you for your message! We will get back to you soon.')
                print(f"Email sent successfully to rinexshine@gmail.com")
            except Exception as e:
                messages.error(request, f'Sorry, there was an error sending your message: {str(e)}')
                print(f"Email sending failed: {str(e)}")
                print(f"Email backend: {settings.EMAIL_BACKEND}")
                print(f"Email host: {settings.EMAIL_HOST}")
                print(f"Email user: {settings.EMAIL_HOST_USER}")
            
            # Redirect to prevent form resubmission
            return render(request, 'pages/contact.html', {'form': ContactForm()})
    else:
        form = ContactForm()
    
    return render(request, 'pages/contact.html', {'form': form})

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
