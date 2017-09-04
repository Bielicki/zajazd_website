from django.conf.urls import url
from .views import Albums, Gallery, PhotoView


app_name = 'gallery'

urlpatterns = [
    url(r'^$', Albums.as_view(), name='albums'),
    url(r'^(?P<album_id>(\d)+)/$', Gallery.as_view(), name='photos'),
    url(r'^photo/(?P<photo_id>(\d)+)', PhotoView.as_view(), name='photo')
]
