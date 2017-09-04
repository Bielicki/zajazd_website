from django.contrib import admin
from .models import Client


@admin.register(Client)
class ReservationsAdmin(admin.ModelAdmin):
    pass
