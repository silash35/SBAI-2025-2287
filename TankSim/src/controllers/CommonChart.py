from PySide6.QtCore import QObject


class ChartController(QObject):
    chart = None
    engine = None
    chartName = ""

    def set_engine(self, engine):
        self.engine = engine

    def getChartObject(self):
        if self.engine is not None:
            if self.chart is None:
                self.chart = self.engine.rootObjects()[0].findChild(
                    QObject, self.chartName
                )
            return self.chart
