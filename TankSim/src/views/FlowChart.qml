import QtCharts
import QtQuick

ChartView {
    id: flowChart

    function push_q(t, q) {
        series_q.append(t, q);
        adjustAxes(t);
    }

    function adjustAxes(t) {
        if (t + (t / 20) > axisX.max)
            axisX.max = t + (t / 20);

    }

    objectName: "flowChart"
    antialiasing: true

    ValueAxis {
        id: axisX

        titleText: "Time/s"
        min: 0
        max: 10
    }

    ValueAxis {
        id: axisY

        titleText: "Flow rate/(cm²s⁻¹)"
        min: 20
        max: 35
    }

    LineSeries {
        id: series_q

        name: "Flow rate (q)"
        axisX: axisX
        axisY: axisY
    }

}
