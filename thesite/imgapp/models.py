from datetime import datetime

from django.db import models
from django.core.files.base import ContentFile
import PIL.Image
from io import BytesIO
import os

from .imgmeta import GetExif


class Image(models.Model):
    """
    Contains a single image
    """
    # Full-size image
    image =             models.ImageField(upload_to="image")
    # 1440p resized image
    image_normal =      models.ImageField(upload_to="image_normal", null=True, editable=False)
    # small resized image
    image_thumbnail =   models.ImageField(upload_to="image_thumbnail", null=True, editable=False)
    caption =           models.TextField()
    created_at =        models.DateTimeField(auto_now_add=True)
    updated_at =        models.DateTimeField(auto_now=True)

    exifdata = None

    def load_metadata_dict(self):
        """
        Load metadata before image has been sent to storage
        """
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
    
    def make_resizes(self):
        image = PIL.Image.open(self.image)
        image.thumbnail((1920, 1080), PIL.Image.ANTIALIAS)
        
        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_normal' + thumb_extension

        if thumb_extension in ['.jpeg', '.jpg']:
            FTYPE = 'JPEG'
        elif thumb_extension in ['.gif']:
            FTYPE = 'GIF'
        elif thumb_extension in ['.png']:
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type
        
        # Save thumbnail to memory
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)
        
        # set save=False to avoid an infinite loop
        self.image_normal.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


    def save(self, *args, **kwargs):
        # Check if we have a new file to process
        if not self.image.closed:
            self.load_metadata_dict()
            self.make_resizes()
        super(Image, self).save(*args, **kwargs)
        if not self.image.closed:
            self.update_metadata()

    def __str__(self) -> str:
        return self.caption

class ImageMetadata(models.Model):
    """
    Metadata for a single image
    """
    capture_date =  models.DateTimeField()
    camera =        models.CharField(max_length=80)
    lens =          models.CharField(max_length=80)
    focallength =   models.CharField(max_length=10)
    fnumber =       models.CharField(max_length=10)
    shutterspeed =  models.CharField(max_length=10)
    iso =           models.CharField(max_length=10)
    
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
