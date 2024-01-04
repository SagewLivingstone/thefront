from django.contrib import admin

from .models import Image, ImageMetadata, DayPage, Album, AlbumImage

class ImageMetadataAdmin(admin.StackedInline):
    model = ImageMetadata
    readonly_fields = ['image']

class AlbumImageInline(admin.StackedInline):
    autocomplete_fields = ['album', 'image']
    model = AlbumImage
    extra = 0

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
    search_fields = ['description', 'day__date']
    inlines = [ImageMetadataAdmin, AlbumImageInline]

@admin.register(DayPage)
class DayPageAdmin(admin.ModelAdmin):
    readonly_fields = [
        'date'
    ]

    class ImageInline(admin.TabularInline):
        model = Image
        extra = 0

    inlines = [ImageInline]

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['title', 'subtitle']
    inlines = [AlbumImageInline]
