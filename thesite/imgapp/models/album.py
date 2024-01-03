from django.db import models

from .image import Image


class Album(models.Model):
    title = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=64)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class AlbumImage(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    caption = models.TextField()

    class PlacementType(models.IntegerChoices):
        AUTO = 0, "auto",
        LEFT = 1, "left",
        RIGHT = 2, "right",
        CENTER = 3, "center"
    placement = models.IntegerField(choices=PlacementType.choices, default=PlacementType.AUTO)
