function generateHourlyForecast(hourlyForecasts) {
    var yAxisLabel = "Temperature (In Fahrenheit)";
    var xAxisLabel = "Time And Date";
    var themeColor = "light1";
    var isAnimationEnabled = false;

    var hourlyForecastChartContainerName = "hourlyForecastContainer";
    var hourlyForecastChartTitle = "Hourly Forecasts";

    window.onload = function () {
        var hourlyForecastChart = generateForecastGraph(hourlyForecasts, hourlyForecastChartContainerName, hourlyForecastChartTitle, yAxisLabel, xAxisLabel, themeColor, isAnimationEnabled);
        hourlyForecastChart.render();
    }
}