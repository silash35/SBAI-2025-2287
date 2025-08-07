import csv
import os
from typing import TypedDict


class Data(TypedDict):
    q: float
    h1_sensor: float
    h1_serial: float
    h2_sensor: float
    h2_serial: float


data_filename = "data.csv"

# Delete previous data
if os.path.exists(data_filename):
    os.remove(data_filename)


def push(data: Data):
    with open(data_filename, mode="a", newline="", encoding="utf-8") as csv_file:
        fieldnames = [
            # User inputs
            "sp",
            "h1_switch",
            "h2_switch",
            # Simulated sensors
            "h1_sensor",
            "h2_sensor",
            # Serial output
            "q",
            "h1_serial",
            "h2_serial",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if csv_file.tell() == 0:
            writer.writeheader()

        writer.writerow(data)
