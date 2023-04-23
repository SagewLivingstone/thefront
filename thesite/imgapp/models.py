from datetime import datetime

from django.db import models
from django.utils import timezone

from .imgmeta import GetExif


class Image(models.Model):
    """
    Contains a single image
    """
    image = models.ImageField(upload_to="image")
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    exifdata = None

    def load_metadata_dict(self):
        if (not hasattr(self.image.file, 'image')): return
        self.exifdata = GetExif(self.image.file.image)

    def update_metadata(self):
        if (self.exifdata is None): return

        try:
            self.metadata = ImageMetadata.objects.get(image=self)
        except ImageMetadata.DoesNotExist:
            self.metadata = ImageMetadata(image=self)
        self.metadata.fill(self.exifdata)
        self.metadata.save()

    def save(self, *args, **kwargs):
        self.load_metadata_dict()
        super(Image, self).save(*args, **kwargs)
        self.update_metadata()

    def __str__(self) -> str:
        return self.caption

class ImageMetadata(models.Model):
    """
    Metadata for a single image
    """
    capture_date = models.DateTimeField()
    camera = models.CharField(max_length=80)
    lens = models.CharField(max_length=80)
    focallength = models.CharField(max_length=10)
    fnumber = models.CharField(max_length=10)
    shutterspeed = models.CharField(max_length=10)
    iso = models.CharField(max_length=10)
    
    image = models.OneToOneField(
        Image,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='metadata'
    )

    def fill(self, exifdict):
        datestring = exifdict.get('DateTimeOriginal')
        formatstring = '%Y:%m:%d %H:%M:%S'
        self.capture_date = datetime.strptime(datestring, formatstring)
        self.camera = exifdict.get('Model')
        self.lens = exifdict.get('LensModel')
        self.focallength = exifdict.get('FocalLength')
        self.fnumber = exifdict.get('FNumber')
        self.shutterspeed = exifdict.get('ExposureTime')
        self.iso = exifdict.get('ISOSpeedRatings')

    def __str__(self) -> str:
        return f'EXIF: [{self.image.caption}]'
