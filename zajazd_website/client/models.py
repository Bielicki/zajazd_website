from django.db import models
from .validators import phone_valid


class Client(models.Model):

    first_name = models.CharField(max_length=32,
                                  verbose_name='Imię')

    last_name = models.CharField(max_length=32,
                                 verbose_name='Nazwisko')

    phone = models.CharField(validators=[phone_valid],
                             max_length=15,
                             verbose_name='Telefon')

    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'Klient'
        verbose_name_plural = 'Klienci'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

