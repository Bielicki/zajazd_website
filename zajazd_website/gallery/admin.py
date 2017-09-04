from django.contrib import admin
from .models import Photo, PhotoAlbum


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):

    list_display = ['title', 'album', 'added']
    exclude = ['thumbnail']

    class Meta:
        model = Photo
        verbose_app_name = 'Zdjęcia'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('admin_image',)
        return self.readonly_fields

    def get_exclude(self, request, obj=None):
        if obj:
            return self.exclude + ['image']
        else:
            return self.exclude


class PhotoMultiAdd(admin.TabularInline):
    model = Photo
    exclude = ['thumbnail']


@admin.register(PhotoAlbum)
class AlbumAdmin(admin.ModelAdmin):

    list_display = ['title', 'added']
    inlines = [PhotoMultiAdd]

    class Meta:
        model = PhotoAlbum
