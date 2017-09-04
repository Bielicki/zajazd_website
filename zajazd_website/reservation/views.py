from django.shortcuts import render
from django.views import View
from .models import Reservation
from .forms import reservation_form_list, ReservationFormStep1, ReservationCreationForm
from client.forms import client_form_list
from .validators import form_check


class BaseReservationView(View):
    pass


class ReservationView(View):
    def get(self, request):
        return render(request, 'reservation/reservation_form.html', {'form': ReservationFormStep1()})

    def post(self, request):
        for form in reservation_form_list + client_form_list:
            if form_check(form, request.POST):
                processed_form = form.process_form(request)
                if processed_form is None:
                    continue
                return render(request, 'reservation/reservation_form.html', processed_form)

        if form_check(ReservationCreationForm, request.session):
            processed_form = ReservationCreationForm.process_form(request)
            return render(request, 'reservation/reservation_form.html', processed_form)


class Pdf(View):
    def get(self, request):
        reservation = Reservation.objects.get(id=request.session['PDF'])
        return reservation.get_as_pdf()


