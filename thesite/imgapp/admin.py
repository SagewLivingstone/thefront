from django.contrib import admin

from .models import Image, ImageMetadata

class ImageMetadataAdmin(admin.StackedInline):
    model = ImageMetadata
    readonly_fields = ['image']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = [
        'created_at',
        'updated_at',
        'image_normal',
        'image_small',
        'image_thumbnail'
    ]
    inlines = [ImageMetadataAdmin]
