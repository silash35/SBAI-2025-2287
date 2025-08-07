from PySide6.QtCore import Slot

from controllers.CommonChart import ChartController


class LevelChartController(ChartController):
    chartName = "levelChart"

    @Slot(float, float, float)
    def push_serial(self, t, h1_serial, h2_serial):
        chart = self.getChartObject()
        if chart:
            chart.push_serial(t, h1_serial, h2_serial)

    @Slot(float, float, float)
    def push_sensor(self, t, h1_sim, h2_sim):
        chart = self.getChartObject()
        if chart:
            chart.push_sensor(t, h1_sim, h2_sim)


levelChartController = LevelChartController()
