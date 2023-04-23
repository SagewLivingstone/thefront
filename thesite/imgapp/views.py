from django.shortcuts import render
from django.http import HttpResponse

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
