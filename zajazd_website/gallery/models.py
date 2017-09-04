import os
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models


class Photo(models.Model):

    title = models.CharField(max_length=32)

    image = models.ImageField(upload_to='gallery',
                              null=False,
                              blank=False)

    added = models.DateTimeField(auto_now_add=True)

    album = models.ForeignKey('PhotoAlbum',
                              blank=True,
                              null=True,
                              related_name="photos",
                              on_delete=models.SET_NULL)

    thumbnail = models.ImageField(null=True,
                                  upload_to='gallery_thumbnails')

    class Meta:
        ordering = ["-added"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        update = False
        if self.id:
            update = True
        self.create_thumbnail()

        super(Photo, self).save(*args, **kwargs, force_update=update)

    def create_thumbnail(self):

        if not self.image:
            return
        if self.thumbnail:
            return

        img_type = self.image.file.content_type

        if img_type == 'image/jpeg':
            pil_type = 'jpeg'
            extension = 'jpg'
        elif img_type == 'image/png':
            pil_type = 'png'
            extension = 'png'

        image = Image.open(BytesIO(self.image.read()))

        thumb_size = (400, 400)

        image.thumbnail(thumb_size, Image.ANTIALIAS)

        temp = BytesIO()
        image.save(temp, pil_type)
        temp.seek(0)

        thumbnail = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp.read(), content_type=img_type)

        self.thumbnail.save(
            '%s_thumbnail.%s' % (os.path.splitext(thumbnail.name)[0], extension),
            thumbnail,
            save=False
        )


class PhotoAlbum(models.Model):

    title = models.CharField(max_length=64,)

    cover = models.ForeignKey(Photo,
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL)

    description = models.TextField(null=True,
                                   blank=True,
                                   verbose_name='Opis')

    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-added"]

    def __str__(self):
        return self.title