from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import datetime
import calendar

from .models import Image, DayPage

def index(request):
    return render(request, 'imgapp/home.html', {})

def image_list(request):
    images_list = Image.objects.all()
    context = { 'image_list': images_list }
    return render(request, 'imgapp/image_list.html', context)

def image(request, image_id):
    image = Image.objects.get(pk=image_id)
    context = { 'image': image }
    return render(request, 'imgapp/image.html', context)

def date(request, year, month, day):
    date = datetime.date(year, month, day)
    daypage = get_object_or_404(DayPage, date=date)

    image_set = daypage.image_set.all()
    counter = day+month+year # Flip left-right every day, adding so no repeat eg. Feb 29 (leap) -> Mar 1
    for image in image_set:
        image.aspect_ratio = image.width / image.height
        image.wide = image.aspect_ratio > 1.4
        if not image.wide:
            image.left = counter % 2
            counter = counter + 1

    # Build page links
    prev = daypage.get_prev_day()
    next = daypage.get_next_day()

    month_url = f'/month/{year}/{month}/'
    prev_url = f'/day/{prev.year}/{prev.month}/{prev.day}/' if prev else month_url
    next_url = f'/day/{next.year}/{next.month}/{next.day}/' if next else month_url

    context = {
        'images': image_set,
        'caption': daypage.caption,
        'date': date,
        'date_str': datetime.date.strftime(date, '%m/%d/%y'),
        'prev_url': prev_url,
        'next_url': next_url,
        'month_url': month_url
    }

    return render(request, 'imgapp/day.html', context)

def _get_days_list(year, month):
    """
    Gets the list of DayPages in a month

    Returns
    days_list: list of DayPages for the month, with empty days filled with Nones (index = day of month)
    fill_days: the number of "empty" weekdays that should be filled before this month's days start
    """

    days_set = DayPage.objects.filter(date__year=year, date__month=month).order_by('date')

    first_weekday, _ = calendar.monthrange(year, month)

    # Build a list of days, from 0 -> last day found in the month
    days_list = []
    if days_set.count():
        # Go through each day in the month, ignoring if we're missing the end of the month
        for i in range(1, days_set.last().date.day+1):
            day = days_set.filter(date__day=i).first()

            if (day):
                day.top_image = day.image_set.first() # Save thumbnail image
                days_list.append(day)
            else:
                days_list.append(None)

    fill_days = (first_weekday + 1) % 7 if days_set.count() else 0
    
    return (
        days_list,
        fill_days
    )

def month(request, year, month):
    days_list, fill_days = _get_days_list(year, month)

    context = {
        'days_set': days_list,
        'fill_days': range(fill_days),
        'month_name': calendar.month_name[month],
        'month_abbr': calendar.month_abbr[month],
        'year': str(year),
        'last_month': (month-2) % 12 + 1, # TODO: Need to handle next/prev year, lol
        'next_month': (month % 12) + 1
    }

    return render(request, 'imgapp/month.html', context)

def year(request, year):
    
    months = {}
    for i in range(1, 13):
        days_list, fill_days = _get_days_list(year, i)
        months[i] = {
            'days_set': days_list,
            'fill_days': range(fill_days),
            'has_days': any(_ is not None for _ in days_list),
            'name': calendar.month_name[i],
        }

    context = {
        'year': str(year),
        'months': months,
        # ...
    }
    return render(request, 'imgapp/year.html', context)

def album(request, id):
    context = {
        'images': image_set, #TODO: Rename these
        'caption': daypage.caption, # TODO: Refactor to be a dict of captions and image indices?
        'date': date, #TODO: Remove, replace with alternative
        'date_str': datetime.date.strftime(date, '%m/%d/%y'), #TODO: Also remove
        'prev_url': prev_url, #TODO: Make optional
        'next_url': next_url,
        'month_url': month_url #TODO: Make this more like a "back" url
    }

    return render(request, 'imgapp/gallery.html', context)