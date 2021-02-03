from rest_framework import serializers
from .models import WeatherApi


class WeatherSerializer(serializers.Serializer):
  city      = serializers.CharField(max_length=255)
  from_time = serializers.TimeField()
  to_time   = serializers.TimeField()

  def create(self, validated_data):
    return WeatherApi.objects.create(**validated_data)
  
  def update(self, instance, validate_data):
    instance.city      = validate_data.get('city', instance.title)
    instance.from_time = validate_data.get('from_time', instance.from_time)
    instance.to_time   = validate_data.get('to_time', instance.to_time)
    instance.save()
    return instance