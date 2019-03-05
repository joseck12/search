from django.shortcuts import render
from django.http import HttpResponse
import datetime as dt
from django.http import Http404
from django.shortcuts import render,redirect
from .models import Image,Category,Location

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

def gallerys_today(request):
    date = dt.date.today()
    gallerys = Image.today_gallerys()
    return render(request, 'my-galleries/today-galleries.html', {"date": date,"gallerys":gallerys})

def convert_dates(dates):

    day_number = dt.date.weekday(dates)

    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    day = days[day_number]
    return day

def past_days_gallerys(request,past_date):

    try:
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        raise Http404()
    if date == dt.date.today():
        return redirect (gallerys_of_today)

    gallerys = Image.days_gallerys(date)
    return render(request, 'all-gallerys/past-gallerys.html',{"date": date,"gallerys": gallerys})

def search_results(request):
    if 'image' in request.GET and request.GET['image']:
        search_term = request.GET.get('image')
        searched_images = Image.search_by_category(search_term)
        message = f"{search_term}"

        return render(request, 'my-galleries/search.html',{"message":message,"images": searched_images})
    else:
        message = "you haven't searched for any term"
        return render(request, 'my-galleries/search.html',{"message":message})

def category_image(request):
    gallerys = Category.images()
    for x in gallerys:
        print(x.image_upload)
    return render(request, 'my-galleries/category.html', {"gallerys":gallerys})


def location(request,location_id):
    locations = Image.objects.filter(location_id=location_id)
    return render(request, 'my-galleries/location.html', {"locations":locations})
