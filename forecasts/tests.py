from django.test import TestCase
from .utility import GeocodeApiHelper, ForecastApiHelper, TestDataGenerator
from .models import Search, HourlyForecast, DailyForecast
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class GeocodeApiHelperTestCase(TestCase):
    def test_get_location_content(self):
        gc_helper = GeocodeApiHelper()
        old_latitude = gc_helper.latitude
        old_longitude = gc_helper.longitude
        entered_address = '1600 Amphitheatre Parkway, Mountain View, CA'
        expected_address = "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA"
        expected_latitude = 37.42231
        expected_longitude= -122.0846241
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
        longitude= -122.0846241
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


class BrowserTests(StaticLiveServerTestCase, TestDataGenerator):
    ENTERED_ADDRESS_NAME = "entered_address"
    SEARCH_BUTTON_XPATH = "/html/body/main/div/div/div/form/div/button"
    LOGIN_BUTTON_XPATH = "/html/body/main/div/div[1]/div/form/div/button"
    PAGINATION_FIRST_PAGE_BUTTON_XPATH = "/html/body/main/div/div/a[1]"
    PAGINATION_SECOND_PAGE_BUTTON_XPATH = "/html/body/main/div/div/a[2]"
    PAGINATION_NEXT_PAGE_BUTTON_XPATH = "/html/body/main/div/div/a[3]"
    PAGINATION_LAST_PAGE_BUTTON_XPATH = "/html/body/main/div/div/a[4]"
    FIRST_ID = "first"
    PREVIOUS_ID = "previous"
    NEXT_ID = "next"
    LAST_ID = "last"
    LOGOUT_LINK_ID = "logout"
    PRIOR_SEARCHES_ID = "priorSearches"
    USERNAME_ID = "username"
    PASSWORD_ID = "password"
    PREVIOUS_SEARCHES_TABLE_ID = "previousSearches"
    HOURLY_FORECAST_CONTAINER_ID = "hourlyForecastContainer"
    LOW_TEMPERATURE_CONTAINER_ID = "lowTemperatureContainer"
    HIGH_TEMPERATURE_CONTAINER_ID = "highTemperatureContainer"
    NO_SEARCHES_PARAGRAPH_ID = "noSearchesParagraph"
    FIRST_TEXT = "First"
    PREVIOUS_TEXT = "Previous"
    NEXT_TEXT = "Next"
    LAST_TEXT = "Last"

    VIEW_DAILY_FORECAST_LINK_XPATH = "/html/body/main/div/div/h1/a"
    VIEW_HOURLY_FORECAST_LINK_XPATH = "/html/body/main/div/div/h1/a"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def login_helper(self, username, password):
        self.selenium.get("%s%s" % (self.live_server_url, "/login/"))
        username_input = self.selenium.find_element_by_name(self.USERNAME_ID)
        username_input.send_keys(username)
        password_input = self.selenium.find_element_by_name(self.PASSWORD_ID)
        password_input.send_keys(password)
        self.selenium.find_element_by_xpath(self.LOGIN_BUTTON_XPATH).click()
        self.selenium.find_element_by_id(self.LOGOUT_LINK_ID)

    def logout_helper(self):
        self.selenium.find_element_by_id(self.LOGOUT_LINK_ID).click()

    def make_search_helper(self):
        # go to the home page.
        self.selenium.get("%s%s" % (self.live_server_url, "/"))
        entered_address_input = self.selenium.find_element_by_name(self.ENTERED_ADDRESS_NAME)
        entered_address_input.send_keys(self.TEST_SAMPLE_ADDRESS)
        self.selenium.find_element_by_xpath(self.SEARCH_BUTTON_XPATH).click()

        self.view_hourly_forecasts_helper()

        # view the daily forecasts.
        self.view_daily_forecasts_helper()

        # go back to the hourly forecasts.
        self.selenium.find_element_by_xpath(self.VIEW_HOURLY_FORECAST_LINK_XPATH).click() 
        self.view_hourly_forecasts_helper()

    def view_daily_forecasts_helper(self):
        self.selenium.find_element_by_xpath(self.VIEW_DAILY_FORECAST_LINK_XPATH).click() 
        self.selenium.find_element_by_id(self.LOW_TEMPERATURE_CONTAINER_ID)
        self.selenium.find_element_by_id(self.HIGH_TEMPERATURE_CONTAINER_ID)
        self.search_for_pagination_widget() # search for the pagination buttons.

    def view_hourly_forecasts_helper(self):
        self.selenium.find_element_by_id(self.HOURLY_FORECAST_CONTAINER_ID) # find the chart for the hourly forecast by ID.
        self.search_for_pagination_widget() # search for the pagination buttons.

    def search_for_pagination_widget(self):
        next_page_button = self.selenium.find_element_by_id(self.NEXT_ID)
        last_page_button = self.selenium.find_element_by_id(self.LAST_ID)
        self.assertEqual(next_page_button.text, self.NEXT_TEXT)
        self.assertEqual(last_page_button.text, self.LAST_TEXT)
        next_page_button.click()
        
        first_page_button = self.selenium.find_element_by_id(self.FIRST_ID)
        previous_page_button = self.selenium.find_element_by_id(self.PREVIOUS_ID)
        self.assertEquals(first_page_button.text, self.FIRST_TEXT)
        self.assertEquals(previous_page_button.text, self.PREVIOUS_TEXT)
        previous_page_button.click()

        next_page_button = self.selenium.find_element_by_id(self.NEXT_ID)
        last_page_button = self.selenium.find_element_by_id(self.LAST_ID)
        self.assertEqual(next_page_button.text, self.NEXT_TEXT)
        self.assertEqual(last_page_button.text, self.LAST_TEXT)

    def test_make_search_not_logged_in(self):
        self.make_search_helper()

    def test_make_search_logged_in(self):
        self.create_users()
        self.login_helper(self.TEST_NAME_ONE, self.TEST_PASSWORD)
        self.make_search_helper()

        self.logout_helper()
        self.delete_sample_data()

    def test_view_present_previous_searches(self):
        self.create_users()
        self.create_searches()
        self.login_helper(self.TEST_NAME_ONE, self.TEST_PASSWORD)

        self.view_previous_searches_helper()
        self.logout_helper()

        self.delete_sample_data()

    def view_previous_searches_helper(self):
        self.selenium.find_element_by_id(self.PRIOR_SEARCHES_ID).click()
        self.selenium.find_element_by_id(self.PREVIOUS_SEARCHES_TABLE_ID)
        self.search_for_pagination_widget() # search for the pagination buttons.
        self.selenium.find_element_by_id(self.PREVIOUS_SEARCHES_TABLE_ID)

    def test_view_no_previous_searches(self):
        self.create_users()
        self.login_helper(self.TEST_NAME_TWO, self.TEST_PASSWORD)

        self.view_no_previous_searches_helper()
        self.logout_helper()

        self.delete_sample_data()

    def view_no_previous_searches_helper(self):
        self.selenium.find_element_by_id(self.PRIOR_SEARCHES_ID).click()
        self.selenium.find_element_by_id(self.NO_SEARCHES_PARAGRAPH_ID)

