import datetime

from django.db import models
from django.utils import timezone


class Image(models.Model):
    image = models.ImageField(upload_to="image")
    caption = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.caption