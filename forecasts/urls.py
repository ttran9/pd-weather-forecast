from django.urls import path
from .views import ( 
    SearchCreateView, 
    DailyForecastListView, 
    HourlyForecastListView, 
    SearchListView
)

urlpatterns = [
    # if we want to do a reverse look-up and having a unique name can help us perform this look-up.
    path("", SearchCreateView.as_view(), name="forecasts-home"),
    path("search/<int:searchId>/dailyforecasts/", DailyForecastListView.as_view(), name="view-dailyforecasts"),
    path("search/<int:searchId>/hourlyforecasts/", HourlyForecastListView.as_view(), name="view-hourlyforecasts"),
    path("user_searches/", SearchListView.as_view(), name="view-searches"),
]