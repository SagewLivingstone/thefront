import datetime

from django.db import models
from django.utils import timezone


class Image(models.Model):
    image = models.ImageField()