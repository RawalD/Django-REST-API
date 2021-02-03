from django.db import models
from django.utils import timezone

# Create your models here.
class WeatherApi(models.Model):
  city      = models.CharField(max_length=255)
  from_time = models.TimeField()
  to_time   = models.TimeField()

  def __str__(self):
    return f'{self.city}-{self.period}'