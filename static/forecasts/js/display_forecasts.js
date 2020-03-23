function generateForecastGraph(forecastList, containerName, chartTitle, yAxisLabel, xAxisLabel, themeColor, isAnimationEnabled) {
    var chart = new CanvasJS.Chart(containerName, {
        theme: themeColor, // "light2", "dark1", "dark2"
        animationEnabled: isAnimationEnabled, // change to true		
        title:{
            text: chartTitle
        },
        axisY: {
            title: yAxisLabel
        },
        axisX: {
            title: xAxisLabel
        },
        data: [
            {
                // Change type to "bar", "area", "spline", "pie", etc.
                type: "column",
                dataPoints: forecastList
            }
        ]
    });
    return chart;
}