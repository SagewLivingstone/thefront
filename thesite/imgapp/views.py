from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import datetime

from .models import Image, DayPage

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
    daypage = get_object_or_404(DayPage, day=date)

    image_set = daypage.image_set.all()
    counter = day+month+year # Flip left-right every day, adding so no repeat eg. Feb 29 (leap) -> Mar 1
    for image in image_set:
        image.aspect_ratio = image.image.width / image.image.height
        image.wide = image.aspect_ratio > 1.4
        if not image.wide:
            image.left = counter % 2
            counter = counter + 1

    prev = daypage.get_prev_day()
    next = daypage.get_next_day()
    if prev:
        prev_url = f'/day/{prev.year}/{prev.month}/{prev.day}/'
    else:
        prev_url = '/imglist/'
    if next:
        next_url = f'/day/{next.year}/{next.month}/{next.day}/'
    else:
        next_url = '/imglist/'

    context = {
        'images': image_set,
        'date': date,
        'prev_url': prev_url,
        'next_url': next_url
    }

    return render(request, 'imgapp/day.html', context)

def month(request, year, month):
    days_set = DayPage.objects.filter(day__year=year, day__month=month).order_by('day')

    # Build head image set
    for day in days_set:
        day.top_image = day.image_set.first()
    
    has_days = len(days_set) > 0

    context = {
        'days_set': days_set,
        'fill_days': range(days_set.first().day.weekday()) if has_days else 0, # Days from the previous month to fill
        'days_range': range(days_set.last().day.day) if has_days else 0
    }
    return render(request, 'imgapp/month.html', context)
