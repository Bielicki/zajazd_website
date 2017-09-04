from django.db.models import QuerySet


class RoomQuerySet(QuerySet):
    def available_rooms(self, date_from, date_to):
        return self.exclude(
            reservations__date_from__gte=date_from,
            reservations__date_to__lte=date_to).exclude(
            reservations__date_from__lt=date_from,
            reservations__date_to__gt=date_from).exclude(
            reservations__date_from__lt=date_to,
            reservations__date_to__gt=date_to)
