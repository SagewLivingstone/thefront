import datetime

from django.db import models
from django.utils import timezone


class Image(models.Model):
    image = models.ImageField(upload_to="image")
    caption = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.caption