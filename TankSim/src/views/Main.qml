import "."
import QtCharts
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root

    width: 16 * 96
    height: 9 * 96
    visible: true
    title: "TankSim"

    RowLayout {
        anchors.fill: parent
        anchors.margins: 32
        spacing: 16

        Menu {
            Layout.alignment: Qt.AlignTop
            Layout.fillHeight: true
            Layout.fillWidth: false
            Layout.preferredWidth: 196
        }

        ColumnLayout {
            FlowChart {
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            LevelChart {
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

        }

    }

}
