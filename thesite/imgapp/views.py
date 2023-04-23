from django.shortcuts import render
from django.http import HttpResponse
import datetime

from .models import Image

def index(request):
    return HttpResponse("Image lib index")

def image_list(request):
    images_list = Image.objects.all()
    context = { 'image_list': images_list }
    return render(request, 'imgapp/image_list.html', context)

def image(request, image_id):
    image = Image.objects.get(pk=image_id)
    context = { 'image': image }
    return render(request, 'imgapp/image.html', context)

def day(request, year, month, day):
    date = datetime.date(year, month, day)
    image_set = Image.objects.filter(
        metadata__capture_date__year=year,
        # metadata__capture_date__month=month,
        # metadata__capture_date__year=day
    )
    for image in image_set:
        image.aspect_ratio = image.image.width / image.image.height
    context = { 'images': image_set,
                'date': date }
    return render(request, 'imgapp/day.html', context)
