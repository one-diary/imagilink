from django.db import models
from .utils import create_shortened_url
from django.utils import timezone
from django.contrib.auth.hashers import make_password
date_generated = models.DateTimeField(default=timezone.now)


class Links(models.Model):
    '''
    Mian links model
    ''' 
    created = models.DateTimeField(auto_now_add=True)
    seo_title = models.CharField(max_length=300, blank=True, null = True)
    seo_image = models.CharField(max_length=300, blank=True, null = True)
    seo_description = models.CharField(max_length=260, blank=True, null = True)
    custom_url = models.CharField(max_length=300, blank=True, null = True, unique=True)
    target_url = models.URLField(null = True, blank = True)
    short_url = models.URLField(null = True, blank = True)
    author = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "links"
        ordering = ["-created"]

    def __str__(self):
        return self.short_url

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = create_shortened_url(self)
        super().save(*args, **kwargs)