function generateDailyForecasts(dailyForecastList) {
    var lowTemperatures = [];
    var highTemperatures = [];

    /*
    * take the daily forecast content and put it into two separate lists.
    * note: I tried to do this in the backend and I was having issues with the Paginator object so I decided to
    * do some light parsing in the front-end.
    */
    for (var i = 0; i < dailyForecastList.length; i++) {
        var dailyForecast = dailyForecastList[i];
        var lowTempContent = dailyForecast.lowTemperature;
        var highTempContent = dailyForecast.highTemperature;
        lowTemperatures.push({
            label: lowTempContent.label,
            y: lowTempContent.y,
        });
        highTemperatures.push({
            label: highTempContent.label,
            y: highTempContent.y,
        });
    }

    var yAxisLabel = "Temperature (In Fahrenheit)";
    var xAxisLabel = "Time And Date";
    var themeColor = "light1";
    var isAnimationEnabled = false;

    var lowTemperatureChartContainerName = "lowTemperatureContainer";
    var lowTemperatureChartTitle = "Daily Forecast (Low Temperatures)";
    var highTemperatureChartContainerName = "highTemperatureContainer";
    var highTemperatureChartTitle = "Daily Forecast (High Temperatures)";

    window.onload = function () {
        var lowTempChart = generateForecastGraph(lowTemperatures, lowTemperatureChartContainerName, lowTemperatureChartTitle, yAxisLabel, xAxisLabel, themeColor, isAnimationEnabled);
        var highTempChart = generateForecastGraph(highTemperatures, highTemperatureChartContainerName, highTemperatureChartTitle, yAxisLabel, xAxisLabel, themeColor, isAnimationEnabled);
        lowTempChart.render();
        highTempChart.render();
    }  
}

