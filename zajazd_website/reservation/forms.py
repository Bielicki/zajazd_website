from datetime import date
from django import forms
from .models import Reservation, Room
from django.core.validators import ValidationError
from client.forms import ClientCheckForm


class BaseModelForm(forms.ModelForm):
    def __init__(self, date_from=None, date_to=None,  *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

        self.date_from = date_from
        self.date_to = date_to
        # self.max = max


class BaseReservationForm(BaseModelForm):
    """
    Form contains all Reservation ModelForm custom validations
    """

    def clean(self):
        cleaned_data = super(BaseReservationForm, self).clean()

        if 'date_from' in cleaned_data and 'date_to' in cleaned_data:
            date_from, date_to = cleaned_data['date_from'], cleaned_data['date_to']

            if date_from < date.today():
                raise ValidationError(message='Data przyjazdu nieprawidłowa')

            if date_from > date_to:
                raise ValidationError(message='Data przyjazdu musi być przed datą odjazdu')

            if not Room.objects.available_rooms(cleaned_data['date_from'], cleaned_data['date_to']):
                raise ValidationError(message='Nie ma dostępnego pokoju w danym terminie')

            if date_from == date_to:
                raise ValidationError(message='Minimalna długość pobytu to 1 dzień')

        return cleaned_data


class ReservationFormStep3(BaseReservationForm):
    next_step = ClientCheckForm

    class Meta:
        model = Reservation
        fields = ['guests_number', 'breakfast', 'additional_info']

    def __init__(self, *args, **kwargs):
        super(ReservationFormStep3, self).__init__(*args, **kwargs)
        # if maximum:
        #     self.fields['guests_number'].widget.attrs.update({'max': maximum})


class ReservationFormStep2(BaseReservationForm):
    next_step = ReservationFormStep3

    class Meta:
        model = Reservation
        fields = ['room']

    def __init__(self, *args, **kwargs):
        super(ReservationFormStep2, self).__init__(*args, **kwargs)
        if self.date_from and self.date_to:
            self.fields['room'].queryset = Room.objects.available_rooms(date_from=self.date_from, date_to=self.date_to)


class ReservationFormStep1(BaseReservationForm):
    next_step = ReservationFormStep2

    class Meta:
        model = Reservation
        fields = ['date_from', 'date_to']

    def __init__(self, *args, **kwargs):
        super(ReservationFormStep1, self).__init__(*args, **kwargs)
        self.fields['date_from'].widget.attrs.update({'id': 'from'})
        self.fields['date_to'].widget.attrs.update({'id': 'to'})


class ReservationCreationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['client', 'date_from', 'date_to', 'room', 'guests_number', 'breakfast', 'additional_info']

reservation_form_list = [ReservationFormStep1,
                         ReservationFormStep2,
                         ReservationFormStep3]