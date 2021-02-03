from django.urls import path
from .views import Weather, weather_api

urlpatterns = [
  path('', Weather.as_view(), name = 'weather'),  
  path('api', weather_api, name = 'weather-api')  
]