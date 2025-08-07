import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: menu

    property double speed: 0
    property double q_value: 21.5
    property double noise_intensity: 0.5
    property double alfa1: 0.56
    property double alfa2: 0.3

    objectName: "menu"
    spacing: 32

    Text {
        text: "TankSim"
        font.bold: true
        font.pointSize: 24
    }

    ColumnLayout {
        Text {
            text: "Flow Rate (q): " + slider_q.value.toFixed(1)
        }

        Slider {
            id: slider_q

            from: 21.5
            to: 34
            stepSize: 0.5
            value: menu.q_value
            Layout.fillWidth: true
            onValueChanged: {
                menu.q_value = value;
            }
        }

    }

    ColumnLayout {
        Layout.alignment: Qt.AlignHCenter
        spacing: 16

        RowLayout {
            spacing: 4

            Text {
                text: "h1"
            }

            Switch {
                id: switch_h1

                objectName: "switch_h1"
                checked: true
            }

        }

        RowLayout {
            Text {
                text: "h2"
            }

            Switch {
                id: switch_h2

                objectName: "switch_h2"
                checked: true
            }

        }

    }

    RowLayout {
        Layout.alignment: Qt.AlignHCenter

        Text {
            text: "Speed:"
        }

        ComboBox {
            id: speedComboBox

            Layout.fillWidth: true
            model: ["Slow Motion (0.5x)", "Real Time (1x)", "Double Speed (2x)", "Max Speed"]
            currentIndex: 3
            onCurrentIndexChanged: {
                switch (currentIndex) {
                case 0:
                    menu.speed = 0.5;
                    break;
                case 1:
                    menu.speed = 1;
                    break;
                case 2:
                    menu.speed = 2;
                    break;
                case 3:
                    menu.speed = 0;
                    break;
                default:
                    menu.speed = 1;
                }
            }
        }

    }

    ColumnLayout {
        Text {
            text: "Noise intensity: " + slider_noise.value.toFixed(1)
        }

        Slider {
            id: slider_noise

            from: 0
            to: 2
            stepSize: 0.1
            value: menu.noise_intensity
            Layout.fillWidth: true
            onValueChanged: {
                menu.noise_intensity = value;
            }
        }

    }

    ColumnLayout {
        Text {
            text: "α\u2081: " + slider_alfa1.value.toFixed(2)
        }

        Slider {
            id: slider_alfa1

            from: 0
            to: 1
            stepSize: 0.01
            value: menu.alfa1
            Layout.fillWidth: true
            onValueChanged: {
                menu.alfa1 = value;
            }
        }

        Text {
            text: "α\u2082: " + slider_alfa2.value.toFixed(2)
        }

        Slider {
            id: slider_alfa2

            from: 0
            to: 1
            stepSize: 0.01
            value: menu.alfa2
            Layout.fillWidth: true
            onValueChanged: {
                menu.alfa2 = value;
            }
        }

    }

}
