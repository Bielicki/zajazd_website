from django.db import models


class About(models.Model):
    paragraph_title = models.CharField(max_length=64,
                                       blank=True,
                                       null=True,
                                       verbose_name='Tytuł akapitu')

    paragraph_content = models.TextField(blank=False,
                                         null=False,
                                         verbose_name='Zawartośc akapitu')

    class Meta:
        verbose_name = 'O Nas'
        verbose_name_plural = 'O nas'
        ordering = ['on_site_order']

    def __str__(self):
        if self.paragraph_title:
            return self.paragraph_title
        return self.paragraph_content[:32] + '...'
