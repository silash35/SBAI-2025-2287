import threading

import numpy as np
import serial
from PySide6.QtCore import QObject

from controllers.FlowChart import flowChartController
from controllers.LevelChart import levelChartController
from database import Data, push
from simulator import simulator

ser = serial.Serial("/dev/ttyACM0", 19200, timeout=5)


def add_noise(h_values: list, noise_intensity: float):
    h_values = np.array(h_values)
    noise = np.random.normal(loc=0.0, scale=noise_intensity, size=(2))
    return (h_values + noise).tolist()


class DaemonThread:
    t = 0
    h_sim = [2.9745, 10.3644]
    h_sensor = h_sim
    speed = 0

    def __init__(self, engine):
        self.engine = engine
        self.root = engine.rootObjects()[0]
        self.menu_component = self.root.findChild(QObject, "menu")
        self.switch_h1 = self.root.findChild(QObject, "switch_h1")
        self.switch_h2 = self.root.findChild(QObject, "switch_h2")

    def run(self):
        if not ser.is_open:
            print("Unable to connect to Arduino. Try restarting the application.")
            ser.open()

        # Get data from interface
        self.speed = float(self.menu_component.property("speed"))
        q = float(self.menu_component.property("q_value"))
        noise_intensity = float(self.menu_component.property("noise_intensity"))
        h1_switch = self.switch_h1.property("checked")
        h2_switch = self.switch_h2.property("checked")

        # Update alfas
        alfa_1 = float(self.menu_component.property("alfa1"))
        alfa_2 = float(self.menu_component.property("alfa2"))
        simulator.update_alfas(alfa_1, alfa_2)

        # Get data from simulator and Arduino
        h_sim = simulator.get_next_point(q, self.h_sim[0], self.h_sim[1])
        h_sensor = add_noise(h_sim, noise_intensity)

        serial_input = f"{self.h_sensor[0] if h1_switch else "" },{self.h_sensor[1] if h2_switch else ""},{q}"
        ser.write(serial_input.encode())
        serial_output = ser.readline().strip().decode()

        print("Serial output:", serial_output)

        if len(serial_output) > 3:
            output_split = serial_output.strip().split(",")
            h1_serial = float(output_split[0])
            h2_serial = float(output_split[1])
            data: Data = {
                "q": q,
                "h1_sensor": h_sensor[0],
                "h1_serial": h1_serial,
                "h2_sensor": h_sensor[1],
                "h2_serial": h2_serial,
                "h1_switch": h1_switch,
                "h2_switch": h2_switch,
            }
            push(data)
            levelChartController.push_serial(self.t, h1_serial, h2_serial)
            levelChartController.push_sensor(self.t, h_sensor[0], h_sensor[1])
            flowChartController.push_q(self.t, q)
            self.h_sim = h_sim
            self.h_sensor = h_sensor
            self.t += simulator.dt

        if self.speed > 0:
            timer = threading.Timer(simulator.dt / self.speed, self.run)
        else:
            timer = threading.Thread(target=self.run)
        timer.daemon = True
        timer.start()
