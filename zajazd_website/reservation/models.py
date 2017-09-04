import os
from datetime import date
from django.db import models
from datetime import datetime
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .query import RoomQuerySet
from django.dispatch import receiver
from django.core.mail import send_mail
from client.models import Client


class Room(models.Model):

    objects = RoomQuerySet.as_manager()

    room_number = models.PositiveIntegerField(unique=True,
                                              verbose_name='Nr. Pokoju')

    capacity = models.PositiveIntegerField(verbose_name='Maksymalna ilośc gości')

    lake_view = models.BooleanField(default=False,
                                    verbose_name='Widok na jezioro')

    class Meta:
        verbose_name = 'Pokój'
        verbose_name_plural = 'Pokoje'

    def __str__(self):
        return f'Pokój nr. {self.room_number}'


class Reservation(models.Model):

    client = models.ForeignKey(Client,
                               related_name='reservations',
                               verbose_name='Klient')

    date_from = models.DateField(verbose_name='Od')

    date_to = models.DateField(verbose_name='Do')

    room = models.ForeignKey(Room,
                             related_name='reservations',
                             verbose_name='Pokój')

    guests_number = models.PositiveIntegerField(verbose_name='Liczba gości')

    breakfast = models.BooleanField(default=False,
                                    verbose_name='Śniadanie')

    additional_info = models.TextField(null=True,
                                       blank=True,
                                       verbose_name='Dodatkowe informacje')

    advance_paid = models.BooleanField(default=False,
                                       verbose_name='Zaliczka opłacona')

    class Meta:
        verbose_name = 'Rezerwacja'
        verbose_name_plural = 'Rezerwacje'
        unique_together = ("date_from", "date_to", "room")

    def __str__(self):
        return f'Rezerwacja na {self.room}  od:{self.date_from} do:{self.date_to}'

    @property
    def total_price(self):
        if self.id:
            if isinstance(self.date_to, str) and isinstance(self.date_from, str):
                date_to = datetime.strptime(self.date_to, '%Y-%m-%d')
                date_from = datetime.strptime(self.date_from, '%Y-%m-%d')

            else:
                date_to = self.date_to
                date_from = self.date_from

            days = (date_to - date_from).days

            return self.guests_number * days * 100
        return ''

    @property
    def advance(self):
        if self.total_price:
            return 0.5 * self.total_price
        return ''

    def get_as_pdf(self):
        year = date.today().year
        line_1 = f'Rezerwacja nr. Z/{self.id}/{year}'
        line_2 = f'{self.client.first_name} {self.client.last_name}'
        line_3 = f'{self.room} Liczba miejsc: {self.guests_number}'
        line_4 = f'OD:  {self.date_from}   DO:  {self.date_to}'
        line_5 = f'Łączna kwota do zapłaty: {self.total_price}'
        line_6 = f'Zaliczka: {self.advance}'
        recipe = [line_1, line_2, line_3, line_4, line_5, line_6]

        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(os.path.dirname(root), 'logo_raw_black.png')

        response_pdf = HttpResponse(content_type='application/pdf')
        response_pdf['Content-Disposition'] = 'attachment; filename="reservation.pdf"'

        # Register font with Polish signs
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

        # Create the PDF object, using the response object as its "file."
        pdf = canvas.Canvas(response_pdf, pagesize=A5)
        pdf.setFont('Arial', 12)

        pdf.drawImage(logo_path, 15, 430, width=150, height=150, mask='auto')

        text_pos = 560

        for line in recipe:
            pdf.drawString(190, text_pos, line)
            text_pos -= 15

        pdf.showPage()
        pdf.save()
        return response_pdf


@receiver(signal=models.signals.post_save, sender=Reservation)
def reservation_emails(instance, **kwargs):
    message_admin = f"""
    Otrzymałeś rezerwacje na {instance.room}
    Od {instance.date_from} Do {instance.date_to}
    Dane klienta:
    {instance.client}
    {instance.client.email}
    {instance.client.phone}
    """

    message = 'Szczegóły rezerwacji:'

    send_mail(
        'Otrzymałeś nową rezerwację',
        message_admin,
        'from@example.com',
        ['rafalbielicki@op.pl'],
        fail_silently=False,
    )

    send_mail(
        'Dokonałeś rezerwacji',
        message,
        'from@example.com',
        [instance.client.email],
        fail_silently=False,
    )
