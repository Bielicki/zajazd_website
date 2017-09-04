from django.views.generic import ListView, DetailView
from .models import PhotoAlbum, Photo


class Albums(ListView):
    model = PhotoAlbum
    template_name = 'gallery/albums.html'
    context_object_name = 'albums'


class Gallery(DetailView):
    model = PhotoAlbum
    pk_url_kwarg = 'album_id'
    template_name = 'gallery/gallery.html'
    context_object_name = 'album'


class PhotoView(DetailView):
    model = Photo
    pk_url_kwarg = 'photo_id'
    template_name = 'gallery/photo.html'
