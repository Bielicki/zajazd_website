from django.conf.urls import url
from .views import ReservationView, Pdf


app_name = 'reservation'

urlpatterns = [
    url(r'^$', ReservationView.as_view(), name='reservation'),
    url(r'^pdf_get/$', Pdf.as_view(), name='PDF'),
]
