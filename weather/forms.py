from django import forms

class WeatherForm(forms.Form):
  city      = forms.CharField(max_length=255)
  from_time = forms.TimeField()
  to_time   = forms.TimeField()
