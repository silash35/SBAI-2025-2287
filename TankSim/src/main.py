import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtWidgets import QApplication

from controllers.FlowChart import flowChartController
from controllers.LevelChart import levelChartController
from daemon import DaemonThread

QQuickStyle.setStyle("Imagine")

os.environ["QT_QPA_PLATFORM"] = "xcb"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.abspath("icon.png")))

    engine = QQmlApplicationEngine()
    engine.load("src/views/Main.qml")

    # Load controllers
    levelChartController.set_engine(engine)
    # engine.rootContext().setContextProperty("levelChartController", levelChartController)
    flowChartController.set_engine(engine)
    # engine.rootContext().setContextProperty("flowChartController", flowChartController)

    if not engine.rootObjects():
        sys.exit(-1)
    else:
        daemon = DaemonThread(engine)
        daemon.run()
    sys.exit(app.exec())
