function generateDailyForecasts(lowTemperatureList, highTemperatureList) {
    var yAxisLabel = "Temperature (In Fahrenheit)";
    var xAxisLabel = "Time And Date";
    var themeColor = "light1";
    var isAnimationEnabled = false;

    var lowTemperatureChartContainerName = "lowTemperatureContainer";
    var lowTemperatureChartTitle = "Daily Forecast (Low Temperatures)";
    var highTemperatureChartContainerName = "highTemperatureContainer";
    var highTemperatureChartTitle = "Daily Forecast (High Temperatures)";

    window.onload = function () {
        var lowTempChart = generateForecastGraph(lowTemperatureList, lowTemperatureChartContainerName, lowTemperatureChartTitle, yAxisLabel, xAxisLabel, themeColor, isAnimationEnabled);
        var highTempChart = generateForecastGraph(highTemperatureList, highTemperatureChartContainerName, highTemperatureChartTitle, yAxisLabel, xAxisLabel, themeColor, isAnimationEnabled);
        lowTempChart.render();
        highTempChart.render();
    }  
}

