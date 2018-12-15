from django.shortcuts import render
from .rent_crawl import *
from .rent_mysql import *
# from django.template import loader
# from django.http import HttpResponse

# Create your views here.

def index_views(request):
    return render(request, "rentBase.html", locals())

def search_views(request):
    work_location = request.GET.get("work-location")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")

    rent_crawl(work_location)

    search = Housing_Resources('localhost','root','123456')
    search.useDB()
    search.handleData(price_min,price_max)
    search.getDataByPrice(work_location)
    houseAmagin = search.regetData()
    house_list=""
    for house in houseAmagin:
        house_str="#".join(house)
        house_list+=house_str+"*"

    return render(request, 'rent.html',locals())
