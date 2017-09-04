from django.contrib import admin
from .models import Room, Reservation


@admin.register(Reservation)
class ReservationsAdmin(admin.ModelAdmin):
    list_display = ['room', 'date_from', 'date_to', 'advance_paid']
    list_editable = ['advance_paid']
    readonly_fields = ['price', 'advance']
    fieldsets = (
        ('Dodaj Rezerwację', {
            'fields': (('client',),
                       ('date_from', 'date_to'),
                       ('room', 'guests_number', 'breakfast'),
                       ('price', 'advance', 'advance_paid')),
            'description': "Uzupełnij pola aby dokonać rezerwacji",

        }),
        ('Dodatkowe', {
            'classes': ('collapse',),
            'fields': ('additional_info',),
        })
    )

    def price(self, obj):
        return obj.total_price
    price.short_description = 'Cena'

    def advance(self, obj):
        return obj.advance
    advance.short_description = 'Zaliczka'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

