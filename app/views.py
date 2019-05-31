from django.shortcuts import render_to_response, redirect
from django.urls import reverse
import csv
from django.http import HttpResponse
from app import settings
from django.core.paginator import Paginator
import webbrowser


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    station_list = []
    with open(settings.BUS_STATION_CSV, encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile)
        for station in reader:
            station_dict = {}
            station_dict['Name'] = station['Name']
            station_dict['Street'] = station['Street']
            station_dict['District'] = station['District']
            station_list.append(station_dict)
    current_page = Paginator(station_list, 10)
    page_number = request.GET.get('page')

    if page_number == None:
        return HttpResponse(webbrowser.open(('http://127.0.0.1:8000/bus_stations?page=1'), new=0))

    elif page_number == '1':
        page_number = 1
        prev_page = None
        next_page_url = 'bus_stations?page=' + str(int(page_number) + 1)

    else:
        prev_page = 'bus_stations?page=' + str(int(page_number) - 1)
        next_page_url = 'bus_stations?page=' + str(int(page_number) + 1)
        page_number = int(page_number)

    return render_to_response('index.html', context={
        'bus_stations': current_page.page(page_number),
        'current_page': page_number,
        'prev_page_url': prev_page,
        'next_page_url': next_page_url
})
