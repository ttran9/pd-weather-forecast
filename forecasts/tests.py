from django.test import TestCase
from .utility import GeocodeApiHelper, ForecastApiHelper
from .models import Search, HourlyForecast, DailyForecast


class GeocodeApiHelperTestCase(TestCase):
    def test_get_location_content(self):
        gc_helper = GeocodeApiHelper()
        old_latitude = gc_helper.latitude
        old_longitude = gc_helper.longitude
        entered_address = '1600+Amphitheatre+Parkway,+Mountain+View,+CA'
        expected_address = "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA"
        expected_latitude = 37.42231
        expected_longitude= -122.0846243
        gc_helper.get_location_content(entered_address)

        self.assertNotEqual(old_latitude, gc_helper.latitude)
        self.assertNotEqual(old_longitude, gc_helper.longitude)
        self.assertEqual(gc_helper.address, expected_address)
        self.assertEqual(expected_latitude, gc_helper.latitude)
        self.assertEqual(expected_longitude, gc_helper.longitude)


class ForecastApiHelperTestCase(TestCase):
    def test_get_forecasts(self):
        fc_helper = ForecastApiHelper()
        latitude = 37.42231
        longitude= -122.0846243
        address = "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA"
        expected_count = 0
        number_of_searches = Search.objects.count()
        number_of_daily_forecasts = DailyForecast.objects.count()
        number_of_hourly_forecasts = HourlyForecast.objects.count()
        self.assertEqual(expected_count, number_of_searches)
        self.assertEqual(expected_count, number_of_daily_forecasts)
        self.assertEqual(expected_count, number_of_hourly_forecasts)
        
        fc_helper.get_forecasts(latitude, longitude, address)
        
        # now check to see if there is a search object saved into the database as well as daily and hourly forecasts.
        updated_number_of_searches = Search.objects.count()
        updated_number_of_daily_forecasts = DailyForecast.objects.count()
        updated_number_of_hourly_forecasts = HourlyForecast.objects.count()

        self.assertNotEqual(expected_count, updated_number_of_searches)
        self.assertNotEqual(expected_count, updated_number_of_daily_forecasts)
        self.assertNotEqual(expected_count, updated_number_of_hourly_forecasts)
