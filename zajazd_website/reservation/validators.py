from django.core.validators import RegexValidator
from django.forms import CheckboxInput

phone_valid = RegexValidator(regex=r'^\.?1?\d{9,15}$', message='Numer telefonu musi mieć od 9 do 15 cyfr')

# More to come


def form_check(form, querydict):
    non_checkbox_fields = [field for field in form().fields
                           if form().fields[field].widget.__class__.__name__ != CheckboxInput.__name__]
    for field in non_checkbox_fields:
        if field not in querydict:
            return False
    return True
