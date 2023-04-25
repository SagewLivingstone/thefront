import os
import uuid
import PIL.Image
from datetime import datetime, date
from io import BytesIO

from django.db import models
from django.core.files.base import ContentFile
from django.utils import timezone

from .imgmeta import GetExif


class DayPage(models.Model):
    day = models.DateField()
    caption = models.TextField()

    def get_next_day(self):
        next = DayPage.objects.filter(
            day__gt=self.day
        ).order_by('day') .first()
        if next:
            return next.day

    def get_prev_day(self):
        prev = DayPage.objects.filter(
            day__lt=self.day
        ).order_by('day') .last()
        if prev:
            return prev.day

    def __str__(self) -> str:
        return "Day: " + str(self.day)

class Image(models.Model):
    """
    Contains a single image
    """
    # 4k max image
    image =             models.ImageField(upload_to="image")
    # 1080p resized image
    image_normal =      models.ImageField(upload_to="image", null=True, editable=False)
    # small resized image
    image_small =       models.ImageField(upload_to="image", null=True, editable=False)
    # thumbnail resized image
    image_thumbnail =   models.ImageField(upload_to="image", null=True, editable=False)
    uuid =              models.CharField(max_length=36, default=uuid.uuid4, null=False, editable=False)
    original_filename = models.CharField(max_length=50, null=True, editable=False)
    caption =           models.TextField()
    created_at =        models.DateTimeField(auto_now_add=True)
    updated_at =        models.DateTimeField(auto_now=True)
    width =             models.IntegerField(null=True, editable=False)
    height =            models.IntegerField(null=True, editable=False)

    day =               models.ForeignKey(DayPage, on_delete=models.PROTECT, null=True, blank=True, editable=False)

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

    def save_resized(self, field, size):
        """
        make a resize of <size> and save it in self.<field>
        """
        pil_image = PIL.Image.open(self.image)
        pil_image.thumbnail(size, PIL.Image.ANTIALIAS)
        
        _, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = str(self.uuid) + '_' + str(size[1]) + thumb_extension

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
        pil_image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)
        
        # set save=False to avoid an infinite loop
        getattr(self, field).save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True
    
    def make_resizes(self):
        """
        resize the image to different sizes
        """
        resizes = [
            ('image_normal', (1920, 1080)),
            ('image_small', (1280, 720)),
            ('image_thumbnail', (640, 360)),
            ('image', (3840, 2160)),  # Finally, resize the image itself to 4k
        ]

        for (field, size) in resizes:
            if not self.save_resized(field, size):
                print(f'Failed to resize to {size} for: {self}')

    def update_day(self):
        if not self.metadata.capture_date: return
        (day, created) = DayPage.objects.get_or_create(day=self.metadata.capture_date)
        self.day = day

        return created

    def update_dimensions(self):
        self.width = self.image.width
        self.height = self.image.height
    
    def update_dimensions_all():
        all = Image.objects.all()
        
        for i, image in enumerate(all):
            print(image, f'[{i}/{len(all)}]')
            try:
                image.update_dimensions()
                image.save()
            except Exception as e:
                print(f"ERROR: {image} -", e)


    def save(self, *args, **kwargs):
        image_changed = not self.image.closed

        if not self.uuid: # In case the uuid doens't get set
            self.uuid = uuid.uuid4()

        # Check if we have a new file to process
        if image_changed:
            self.load_metadata_dict()
            self.original_filename = self.image.name
            self.make_resizes()
        super().save(*args, **kwargs)
        if image_changed:
            self.update_metadata()
            self.update_dimensions()
        self.update_day()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (datetime.strftime(self.day.day, '%m/%d/%y') if self.day else 'DATEERROR') + '\n' + self.caption

class ImageMetadata(models.Model):
    """
    Metadata for a single image
    """
    capture_date =  models.DateTimeField(null=True, blank=True)
    camera =        models.CharField(max_length=80, null=True, blank=True)
    lens =          models.CharField(max_length=80, null=True, blank=True)
    focallength =   models.CharField(max_length=10, null=True, blank=True)
    fnumber =       models.CharField(max_length=10, null=True, blank=True)
    shutterspeed =  models.CharField(max_length=20, null=True, blank=True)
    iso =           models.CharField(max_length=10, null=True, blank=True)
    location =      models.CharField(max_length=30, null=True, blank=True)
    
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
        self.camera = exifdict.get('Model') or self.camera
        self.lens = exifdict.get('LensModel') or self.lens
        self.focallength = exifdict.get('FocalLength') or self.focallength
        self.fnumber = exifdict.get('FNumber') or self.fnumber
        self.shutterspeed = exifdict.get('ExposureTime') or self.shutterspeed
        self.iso = exifdict.get('ISOSpeedRatings') or self.iso

    def __str__(self) -> str:
        return f'EXIF: [{self.image.caption}]'