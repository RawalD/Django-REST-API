#Python imports
import datetime
import time
import json
import requests


#Django imports
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


#REST framework
from rest_framework.parsers import JSONParser

#Serializer, model
from .serializers import WeatherSerializer
from .models import WeatherApi


#Get median of the temperatures function
def get_median(arr):

#Sort given array
    arr.sort()

    if len(arr) > 2:

        #Find median depending if array is even length or odd length
        if len(arr) % 2 == 0:
            i1 = int((len(arr)/2)-1)
            i2 = i1+1
            v1 = arr[i1]
            v2 = arr[i2]
            avg = (v1+v2)/2
            return (avg, i1)

        else:
            i = int(((len(arr)/2)+1)-1)
            return (arr[i], i)
    
    elif len(arr) == 2:
        return (arr[0], '')
    
    elif len(arr) == 1:
        return (arr[0], '')

# Create your views here.
class Weather(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'home.html', context)

#Weather API function
@csrf_exempt
def weather_api(request, *args, **kwargs):

#OpenWeatherAPI key
    api_key = 'd86fb9a016d21bae31c09fd97eee8838'

#Grab today information for input of start time
    today = datetime.date.today()
    today_now = datetime.datetime.now()
    today_now_dt = int(time.mktime(datetime.datetime.strptime(
        str(today_now), "%Y-%m-%d %H:%M:%S.%f").timetuple()))
    
    arr_dt = []
    
    temp_arr = []
    temp = ''
    
    temp_min = ''
    temp_min_arr = []
    
    temp_max = ''
    temp_max_arr = []
    
    hum_arr = []
    hum = ''

#If request is GET send all information in the serializer
    if request.method == 'GET':
        
        weathers = WeatherApi.objects.all()
        serializer = WeatherSerializer(weathers, many=True)

        return JsonResponse(serializer.data, safe=False)

#If POST method
    elif request.method == 'POST':
        
        city = ''
        from_time = ''
        to_time = ''

        if len(request.POST) == 0:
            data = JSONParser().parse(request)
            serializer = WeatherSerializer(data=data)
        
            if serializer.is_valid():
                city = data['city']
                from_time = data['from_time']
                to_time = data['to_time']
        
            else:
                return JsonResponse({'status': 400, 'msg': 'Invalid input, please see your START and END Time correctly'}, status=400)
        
        else:

            _i = request.POST
            inputs = dict(_i.lists())
            city = inputs['city'][0]
            from_time = inputs['from_time'][0]
            to_time = inputs['to_time'][0]

        from_time_dt = int(time.mktime(datetime.datetime.strptime(
            (str(today) + ' '+from_time), "%Y-%m-%d %H:%M").timetuple()))
        to_time_dt = int(time.mktime(datetime.datetime.strptime(
            (str(today) + ' '+to_time), "%Y-%m-%d %H:%M").timetuple()))

        #Conditional error checker
        if from_time_dt >= to_time_dt:
            return JsonResponse({'status': 400, 'msg': 'From Time cannot be greather than To Time'}, status=400)
        
        elif from_time_dt < today_now_dt:
            return JsonResponse({'status': 400, 'msg': 'No historical data, Please check your Start Time'}, status=400)

        try:
            url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}'
            r = requests.get(url)
            r_data = json.loads(r.text)
            r_list = r_data['list']

            for item in r_list:
        
                if item['dt'] >= from_time_dt and item['dt'] <= to_time_dt:
                    arr_dt.append(item)
        
            if len(arr_dt) == 0:

                url_1 = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'

                r1 = requests.get(url_1)
                r1_data = json.loads(r1.text)

                temp_ar = [temp, temp_max, temp_min]
                temp_ar.sort()
                temp_mean = temp_ar[1]
        
                current = {
                    'temp': r1_data['main']['temp'],
                    'temp_min': r1_data['main']['temp_min'],
                    'temp_max': r1_data['main']['temp_max'],
                    'temp_avg': round(((r1_data['main']['temp_min'])+(r1_data['main']['temp_max']))/2),
                    'temp_mean': temp_mean,
                    'humidity': r1_data['main']['humidity'],
                    'city': city
                }
        
                return JsonResponse(current, status=200)
        
            else:
                for item in arr_dt:
        
                    temp_arr.append(item['main']['temp'])
                    temp_min_arr.append(item['main']['temp_min'])
                    temp_max_arr.append(item['main']['temp_max'])

                    hum_arr.append(item['main']['humidity'])

                    temp_min = temp_min_arr[0] if len(
                        temp_min_arr) == 1 else min(*temp_min_arr)

                    temp_max = temp_max_arr[0] if len(
                        temp_min_arr) == 1 else max(*temp_max_arr)

                    temp_avg = temp_arr[0] if len(temp_arr) == 1 else round(
                        sum(temp_arr)/len(temp_arr))

                    temp, _ = (temp_arr[0], '') if len(
                        temp_arr) == 1 else get_median(temp_arr)

                    hum, _ = (hum_arr[0], '') if len(
                        hum_arr) == 1 else get_median(hum_arr)

                current = {
                    'temp': temp,
                    'temp_min': temp_min,
                    'temp_max': temp_max,
                    'temp_avg': temp_avg,
                    'temp_mean': temp,
                    'humidity': hum,
                    'city': city
                }
        
        except Exception as exception:
            return JsonResponse({'status': 400, 'msg': 'API Calls Failed'}, status=400)
        return JsonResponse(current, status=200)
