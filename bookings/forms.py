from django import forms
from .models import Booking


class BaseBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "full_name",
            "email",
            "phone",
            "selected_date",
            "selected_start_time",
            "selected_end_time",
            "postcode",
            "address_line1",
            "address_line2",
            "city",
            "notes",
            "consent",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),

            "selected_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "selected_start_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "selected_end_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),

            "postcode": forms.TextInput(attrs={"class": "form-control"}),
            "address_line1": forms.TextInput(attrs={"class": "form-control"}),
            "address_line2": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),

            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "consent": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_consent(self):
        if self.cleaned_data.get("consent") is not True:
            raise forms.ValidationError("Consent is required to submit your booking.")
        return True


class CarCareBookingForm(BaseBookingForm):
    vehicle_type = forms.ChoiceField(
        choices=[("car", "Car"), ("suv", "SUV"), ("van", "Van")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    vehicle_size = forms.ChoiceField(
        choices=[("small", "Small"), ("medium", "Medium"), ("large", "Large")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    package = forms.ChoiceField(
        choices=[("exterior", "Exterior"), ("interior", "Interior"), ("full", "Full Valet")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    water_access = forms.ChoiceField(
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    electricity_access = forms.ChoiceField(
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.Select(attrs={"class": "form-control"})
    )


class HomeCleaningBookingForm(BaseBookingForm):
    property_type = forms.ChoiceField(
        choices=[("flat", "Flat"), ("house", "House")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    bedrooms = forms.IntegerField(
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    bathrooms = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    frequency = forms.ChoiceField(
        choices=[("one-off", "One-off"), ("weekly", "Weekly"), ("fortnightly", "Fortnightly"), ("monthly", "Monthly")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    supplies_provided = forms.ChoiceField(
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )


class OfficeShopBookingForm(BaseBookingForm):
    business_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    premises_type = forms.ChoiceField(
        choices=[("office", "Office"), ("retail", "Retail/Shop"), ("salon", "Salon"), ("other", "Other")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    size_band = forms.ChoiceField(
        choices=[("small", "Small"), ("medium", "Medium"), ("large", "Large")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    toilets = forms.IntegerField(
        min_value=0,
        max_value=50,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    schedule = forms.ChoiceField(
        choices=[("one-off", "One-off"), ("weekly", "Weekly"), ("2-3", "2–3x weekly"), ("daily", "Daily")],
        widget=forms.Select(attrs={"class": "form-control"})
    )


class MoveInOutBookingForm(BaseBookingForm):
    cleaning_type = forms.ChoiceField(
        choices=[("move-in", "Move-in"), ("end-tenancy", "End of tenancy")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    bedrooms = forms.IntegerField(
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    bathrooms = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    furnished = forms.ChoiceField(
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    oven_clean = forms.BooleanField(required=False)
    carpet_clean = forms.BooleanField(required=False)


class UpholsteryBookingForm(BaseBookingForm):
    item_type = forms.ChoiceField(
        choices=[("sofa", "Sofa"), ("armchair", "Armchair"), ("dining-chairs", "Dining chairs"), ("mattress", "Mattress"), ("other", "Other")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    quantity = forms.IntegerField(
        min_value=1,
        max_value=50,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    fabric_type = forms.ChoiceField(
        choices=[("fabric", "Fabric"), ("leather", "Leather"), ("velvet", "Velvet"), ("unsure", "Unsure")],
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )
    stains_present = forms.BooleanField(required=False)
    odour_treatment = forms.BooleanField(required=False)