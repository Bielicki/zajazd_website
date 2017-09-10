from django.shortcuts import render
from django.views import View
from .models import Reservation
from .forms import reservation_form_list, ReservationFormStep1, ReservationCreationForm
from client.forms import client_form_list
from .forms_processing import ReservationFormProcessor
from client.forms_processing import ClientFormProcessor


class ReservationView(View):

    def get(self, request):
        request.session.flush()
        return render(request, 'reservation/reservation_form.html', {'form': ReservationFormStep1()})

    def post(self, request):
        reservation_processor = ReservationFormProcessor(reservation_form_list, request)
        client_processor = ClientFormProcessor(client_form_list, request)

        reservation_processor.form_check()
        if reservation_processor.form:
            form = reservation_processor.process_form()

        client_processor.form_check()
        if client_processor.form:
            form = client_processor.process_form()

        if form:
            return render(request, 'reservation/reservation_form.html', {'form': form})
        else:
            form = ReservationCreationForm(request.session)
            if form.is_valid():
                reservation = form.save()
                request.session['PDF'] = reservation.id
                return render(request, 'reservation/reservation_form.html', {'reservation': reservation})


class Pdf(View):
    def get(self, request):
        reservation = Reservation.objects.get(id=request.session['PDF'])
        return reservation.get_as_pdf()
