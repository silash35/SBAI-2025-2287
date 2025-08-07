import QtCharts
import QtQuick

ChartView {
    id: levelChart

    function push_serial(t, h1_serial, h2_serial) {
        series_h1_serial.append(t, h1_serial);
        series_h2_serial.append(t, h2_serial);
        adjustAxes(t);
    }

    function push_sensor(t, h1_sensor, h2_sensor) {
        series_h1_sensor.append(t, h1_sensor);
        series_h2_sensor.append(t, h2_sensor);
        adjustAxes(t);
    }

    function push_sp(t, sp) {
        series_sp.append(t, sp);
        adjustAxes(t);
    }

    function adjustAxes(t) {
        if (t + (t / 20) > axisX.max)
            axisX.max = t + (t / 20);

    }

    objectName: "levelChart"
    antialiasing: true

    ValueAxis {
        id: axisX

        titleText: "Time / s"
        min: 0
        max: 10
    }

    ValueAxis {
        id: axisY

        titleText: "Level / cm"
        min: 0
        max: 30
    }

    ScatterSeries {
        id: series_h1_sensor

        name: "h1 (Sensor)"
        axisX: axisX
        axisY: axisY
        markerShape: ScatterSeries.MarkerShapeCircle
        markerSize: 8
        borderColor: "transparent"
    }

    ScatterSeries {
        id: series_h2_sensor

        name: "h2 (Sensor)"
        axisX: axisX
        axisY: axisY
        markerShape: ScatterSeries.MarkerShapeCircle
        markerSize: 8
        borderColor: "transparent"
    }

    LineSeries {
        id: series_h1_serial

        name: "h1 (Serial)"
        axisX: axisX
        axisY: axisY
    }

    LineSeries {
        id: series_h2_serial

        name: "h2 (Serial)"
        axisX: axisX
        axisY: axisY
    }

    LineSeries {
        id: series_sp

        name: "h2 (SP)"
        axisX: axisX
        axisY: axisY
    }

}
