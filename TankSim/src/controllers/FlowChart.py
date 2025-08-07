from PySide6.QtCore import Slot

from controllers.CommonChart import ChartController


class FlowChartController(ChartController):
    chartName = "flowChart"

    @Slot(float, float)
    def push_q(self, t, q):
        chart = self.getChartObject()
        if chart:
            chart.push_q(t, q)


flowChartController = FlowChartController()
