from django import forms
from django.core.validators import RegexValidator

class ContactForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone number'
        })
    )
    
    city = forms.ChoiceField(
        choices=[
            ('', 'Select a city'),
            ('nottingham', 'Nottingham'),
            ('derby', 'Derby'),
            ('leicester', 'Leicester'),
            ('mansfield', 'Mansfield'),
            ('worksop', 'Worksop'),
            ('other', 'Other'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    service_type = forms.ChoiceField(
        choices=[
            ('', 'Select Service'),
            ('home-cleaning', 'Home Cleaning'),
            ('car-care', 'Car Care & Detailing'),
            ('office-cleaning', 'Office/Shop Cleaning'),
            ('upholstery', 'Upholstery & Fabric Cleaning'),
            ('move-in-out', 'Move In/Out Cleaning'),
            ('other', 'Other'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Tell us about your cleaning needs...'
        })
    )
