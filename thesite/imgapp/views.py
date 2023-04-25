from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import datetime
import calendar

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
        image.aspect_ratio = image.width / image.height
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

    has_days = len(days_set) > 0

    # Build a list of days, from 0 -> last day found in the month
    days_list = []
    if days_set.count():
        for i in range(1, days_set.last().day.day+1):
            day = days_set.filter(day__day=i).first()
            if (day):
                day.top_image = day.image_set.first()
                days_list.append(day)
            else:
                days_list.append(None)

    context = {
        'days_set': days_list,
        'fill_days': range(days_set.first().day.weekday()) if has_days else 0, # Days from the previous month to fill
        'days_range': range(days_set.last().day.day) if has_days else 0,
        'month_name': calendar.month_name[month],
        'year': str(year),
        'last_month': month-1,
        'next_month': month+1
    }
    return render(request, 'imgapp/month.html', context)
