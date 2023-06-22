from django.contrib import admin

from .models import Image, ImageMetadata, DayPage

class ImageMetadataAdmin(admin.StackedInline):
    model = ImageMetadata
    readonly_fields = ['image']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = [
        'created_at',
        'updated_at',
        'uuid',
        'original_filename',
        'day',
        'image_normal',
        'image_small',
        'image_thumbnail',
        'width',
        'height'
    ]
    inlines = [ImageMetadataAdmin]

@admin.register(DayPage)
class DayPageAdmin(admin.ModelAdmin):
    readonly_fields = [
        'date'
    ]

    class ImageInline(admin.TabularInline):
        model = Image
        extra = 0

    inlines = [ImageInline]
