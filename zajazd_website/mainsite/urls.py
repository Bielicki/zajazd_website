from django.conf.urls import url
from .views import Index, Contact, AboutUs


app_name = 'mainsite'

urlpatterns = [
    url(r'^$', Index.as_view(), name='main'),
    url(r'^about/$', AboutUs.as_view(), name='about'),
    url(r'^contact/$', Contact.as_view(), name='contact'),
]
