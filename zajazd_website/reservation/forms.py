from datetime import date
from django import forms
from .models import Reservation, Room
from django.core.validators import ValidationError
from client.forms import ClientCheckForm


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


    @classmethod
    def create_form_session(cls, request):
        for field in cls._meta.fields:
            if field == 'breakfast' and field not in request.POST:
                request.session['breakfast'] = False
            else:
                request.session[field] = request.POST[field]

    @classmethod
    def process_form(cls, request):
        if cls(request.POST).is_valid():
            cls.create_form_session(request)
            return {'form': cls.next_step()}
        else:
            return {'form': cls(request.POST)}


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

#    def __init__(self, maximum=None, *args, **kwargs):
#        super(ReservationFormStep3, self).__init__(*args, **kwargs)
#        if maximum:
#            self.fields['guests_number'].widget.attrs.update({'max': maximum})


class ReservationFormStep2(BaseReservationForm):
    next_step = ReservationFormStep3

    class Meta:
        model = Reservation
        fields = ['room']

    def __init__(self, date_from=None, date_to=None, *args, **kwargs):
        super(ReservationFormStep2, self).__init__(*args, **kwargs)
        if date_from and date_to:
            self.fields['room'].queryset = Room.objects.available_rooms(date_from=date_from, date_to=date_to)

    @classmethod
    def process_form(cls, request):
        date_from = request.session['date_from']
        date_to = request.session['date_to']

        if cls(date_from, date_to, request.POST).is_valid():
  #          maximum = Room.objects.get(id=request.POST['room']).capacity
            cls.create_form_session(request)
            return {'form': cls.next_step()}
        else:
            return {'form': cls(date_from, date_to, request.POST)}


class ReservationFormStep1(BaseReservationForm):
    next_step = ReservationFormStep2

    class Meta:
        model = Reservation
        fields = ['date_from', 'date_to']

    def __init__(self, *args, **kwargs):
        super(ReservationFormStep1, self).__init__(*args, **kwargs)
        self.fields['date_from'].widget.attrs.update({'id': 'from'})
        self.fields['date_to'].widget.attrs.update({'id': 'to'})

    @classmethod
    def process_form(cls, request):
        if cls(request.POST).is_valid():
            cls.create_form_session(request)
            date_from = request.session['date_from']
            date_to = request.session['date_to']
            return {'form': cls.next_step(date_to=date_to, date_from=date_from)}
        else:
            return {'form': cls(request.POST)}


class ReservationCreationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['client', 'date_from', 'date_to', 'room', 'guests_number', 'breakfast', 'additional_info']

    @classmethod
    def check_data(cls, request):
        for field in cls._meta.fields:
            if field not in request.session:
                return False
        return True

    @classmethod
    def process_form(cls, request):
        reservation = cls(request.session).save()
        cls.session_clear(request)
        print('Zakończone session_clear')
        request.session['PDF'] = reservation.id
        print('Dodano PDF do sesji')
        return {'reservation': reservation}

    @classmethod
    def session_clear(cls, request):
        for field in cls._meta.fields:
            if field in request.session:
                del request.session[field]
                print(f'Usunięto {field}')


reservation_form_list = [ReservationFormStep1,
                         ReservationFormStep2,
                         ReservationFormStep3]
