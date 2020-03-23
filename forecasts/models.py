from django.db import models
from django.contrib.auth.models import User
import time
from django.urls import reverse


class Search(models.Model):
    time_of_search = models.CharField(max_length=50)
    entered_address = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    unformatted_time_of_search = models.IntegerField(default=time.time())

    def get_absolute_url(self):
        return reverse("view-hourlyforecasts", kwargs={"searchId": self.id})

class AbstractForecast(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    summary = models.CharField(max_length=150)


class HourlyForecast(AbstractForecast):
    unformatted_time = models.IntegerField(default=time.time())
    time = models.CharField(max_length=50)
    temperature = models.DecimalField(max_digits=4, decimal_places=2)

    def parse_to_json(self):
        hf_json = {'label': self.time, 'y': float(self.temperature)}
        return hf_json


class DailyForecast(AbstractForecast):
    high_temperature_time = models.CharField(max_length=50)
    high_temperature = models.DecimalField(max_digits=4, decimal_places=2)
    low_temperature_time = models.CharField(max_length=50)
    low_temperature = models.DecimalField(max_digits=4, decimal_places=2)

    def parse_temperatures_to_json(self):
        df_json = {"lowTemperature": {'label': self.low_temperature_time, 'y': float(self.low_temperature)}, 
        "highTemperature": {'label': self.high_temperature_time, 'y': float(self.high_temperature)}}
        return df_json