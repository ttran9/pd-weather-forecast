import http.client, json, time, os, datetime
from pytz import timezone
from django.contrib.auth.models import AnonymousUser
from .models import Search, HourlyForecast, DailyForecast
import urllib.parse 


class GeocodeApiHelper:

    def __init__(self):
        self.address = ""
        self.latitude = 0.0
        self.longitude = 0.0

    def get_location_content(self, address):
        conn = http.client.HTTPSConnection('maps.googleapis.com')
        headers = {'Content-type': 'application/json'}
        api_key = os.environ['GOOGLE_MAPS_GC_KEY']
        encoded_address = urllib.parse.quote_plus(address)
        conn.request('GET', f"/maps/api/geocode/json?address={encoded_address}&key={api_key}", headers=headers)
        response = conn.getresponse()
        object = response.read()
        json_object = json.loads(object)
        results = json_object['results']
        location_object = results[0]
        geometry = location_object['geometry']
        location = geometry['location']
        self.latitude = location['lat']
        self.longitude = location['lng']
        self.address = location_object['formatted_address']


class ForecastApiHelper:

    def __init__(self):
        self.search = None
        
    def get_forecasts(self, lat, lng, searched_address, user=None):
        api_key = os.environ['DARK_SKY_KEY']
        conn = http.client.HTTPSConnection('api.darksky.net')
        headers = {'Content-type': 'application/json'}
        conn.request('GET', f"/forecast/{api_key}/{lat},{lng}", headers=headers)
        response = conn.getresponse()
        object = response.read()
        content = json.loads(object)
        search = Search()
        time_zone = content["timezone"]
        search_time_in_milliseconds = content['currently']['time']
        search.time_of_search = self.get_date_from_milliseconds(search_time_in_milliseconds, time_zone)
        search.entered_address = searched_address
        search.unformatted_time_of_search = search_time_in_milliseconds

        hourly_forecasts = content['hourly']['data']
        daily_forecasts = content['daily']['data']

        if user is not None or user is not AnonymousUser:
            search.user = user
        
        search.save() # must persist to be able to write this into the database.

        self.parse_hourly_forecast(hourly_forecasts, search, time_zone)
        self.parse_daily_forecast(daily_forecasts, search, time_zone)

        self.search = search


    def get_date_from_milliseconds(self, milliseconds, current_timezone):
        format = "%b %d, %Y at %-I:%M %p"
        current_time = datetime.datetime.fromtimestamp(milliseconds)
        target_time = current_time.astimezone(timezone(current_timezone))
        return target_time.strftime(format)
        
    def parse_hourly_forecast(self, hourly_forecasts, search_object, time_zone):
        for h_forecast in hourly_forecasts:
            hourly_forecast = HourlyForecast()
            milliseconds = h_forecast['time']
            hourly_forecast.search = search_object
            hourly_forecast.summary = h_forecast['summary']
            hourly_forecast.temperature = h_forecast['temperature'] 
            hourly_forecast.time = self.get_date_from_milliseconds(milliseconds, time_zone)
            hourly_forecast.unformatted_time = milliseconds
            hourly_forecast.save()

    def parse_daily_forecast(self, daily_forecasts, search_object, time_zone):
         for d_forecast in daily_forecasts:
            daily_forecast = DailyForecast()
            milliseconds = d_forecast['time']
            daily_forecast.search = search_object
            daily_forecast.summary = d_forecast['summary']
            daily_forecast.high_temperature = d_forecast['temperatureHigh']
            temp_high_in_milliseconds = d_forecast['temperatureHighTime']
            daily_forecast.high_temperature_time = self.get_date_from_milliseconds(temp_high_in_milliseconds, time_zone)
            daily_forecast.low_temperature = d_forecast['temperatureLow']
            temp_low_in_milliseconds = d_forecast['temperatureLowTime']
            daily_forecast.low_temperature_time = self.get_date_from_milliseconds(temp_low_in_milliseconds, time_zone)
            daily_forecast.save()

   
class ParseForecasts:
    def parse_hourly_forecasts(self, hourly_forecasts):
        results = []
        for forecast in hourly_forecasts:
            forecast_content = []
            forecast_content.append(forecast.time)
            forecast_content.append(str(forecast.temperature))
            results.append(forecast_content)
        
        return results