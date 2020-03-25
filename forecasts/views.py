from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView,
    ListView
)
from .models import Search, DailyForecast, HourlyForecast
from .utility import GeocodeApiHelper, ForecastApiHelper, ParseForecasts, ApiInvokeHelper
from django.contrib.auth.mixins import LoginRequiredMixin


class SearchCreateView(CreateView):
    model = Search
    fields = ["entered_address"]

    template_name = "forecasts/search_form.html"

    def form_valid(self, form):
        # before the form is submitted take the instance of the form and set the user if one is logged in.
        user = self.request.user
        address = form.instance.entered_address

        helper = ApiInvokeHelper()
        fc_helper = helper.make_search(address, user)

        form.instance = fc_helper.search
        
        return super().form_valid(form)


class DailyForecastListView(ListView):
    model = DailyForecast
    template_name = "forecasts/daily_forecasts.html"
    context_object_name = "forecasts"
    paginate_by = 5

    def get_queryset(self):
        search = get_object_or_404(Search, pk=self.kwargs.get("searchId"))
        daily_forecasts = DailyForecast.objects.filter(search=search)
        pf = ParseForecasts()
        return pf.parse_daily_forecasts(daily_forecasts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchId'] = self.kwargs['searchId']
        return context
        

class HourlyForecastListView(ListView):
    model = HourlyForecast
    template_name = "forecasts/hourly_forecasts.html"
    context_object_name = "forecasts"
    paginate_by = 5

    def get_queryset(self):
        search = get_object_or_404(Search, pk=self.kwargs.get("searchId"))
        hourly_forecasts = HourlyForecast.objects.filter(search=search)
        pf = ParseForecasts()
        return pf.parse_hourly_forecasts(hourly_forecasts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchId'] = self.kwargs['searchId']
        return context


class SearchListView(LoginRequiredMixin, ListView):
    model = Search
    template_name = "forecasts/user_searches.html"
    context_object_name = "searches"
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return Search.objects.filter(user=user).order_by("unformatted_time_of_search")
