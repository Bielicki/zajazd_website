from django.core.validators import RegexValidator

phone_valid = RegexValidator(regex=r'^\.?1?\d{9,15}$', message='Numer telefonu musi mieć od 9 do 15 cyfr')