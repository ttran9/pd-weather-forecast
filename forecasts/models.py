from django.db import models
from django.contrib.auth.models import User


class Search(models.Model):
    time_of_search = models.CharField(max_length=50)
    entered_address = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class AbstractForecast(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    summary = models.CharField(max_length=150)


class HourlyForecast(AbstractForecast):
    time = models.CharField(max_length=50)
    temperature = models.DecimalField(max_digits=4, decimal_places=2)


class DailyForecast(AbstractForecast):
    high_temperature_time = models.CharField(max_length=50)
    high_temperature = models.DecimalField(max_digits=4, decimal_places=2)
    low_temperature_time = models.CharField(max_length=50)
    low_temperature = models.DecimalField(max_digits=4, decimal_places=2) 