# TankSim

This directory contains the code for the TankSim software, developed in Python using the [Qt framework](https://www.qt.io/). TankSim simulates a tank system, allows flow Rate adjustments, and communicates with the Arduino via serial connection.

The code was tested on Linux. It may work if you are using Windows, but it has not been tested.

This python project utilizes **UV** to manage dependencies and ensure that the correct versions of Python and libraries are installed.

## How to Run

1. **Install UV**: Follow the installation instructions provided in the [UV documentation](https://docs.astral.sh/uv/).

1. **Install Python and required dependencies**: This project uses a `pyproject.toml` file to list all necessary dependencies and the correct python version. After setting up UV, install these dependencies by running:

   ```bash
   uv sync
   ```

1. **Connect the Arduino**: Before running the application, make sure that your Arduino is properly connected to your computer via USB. Also, ensure that the Arduino is running the appropriate Arduino code that communicates with this software.

1. **Edit the `src/daemon.py` file**: This file contains the configuration for serial communication with the Arduino. You'll need to edit the serial port used for communication. Locate the following line in daemon.py:

   ```python
   ser = serial.Serial("/dev/ttyACM0", 19200, timeout=5)
   ```

   The string `/dev/ttyACM0` refers to the serial port that the Arduino is connected to on your system. This may vary depending on your operating system and how your Arduino is connected. The simplest way to find which port your Arduino is connected to is by opening the Arduino IDE and checking.

1. Run the TankSim software. Just execute the following command:

   ```bash
   uv run ./src/main.py
   ```

   The simulation data will be saved on the file `src/data.csv`. Every time the application is opened, this file will be overwritten with new data. If you want to save the simulation data for later analysis, rename the data.csv file before running the application again.

1. Generating Graphs: To visualize the simulation data, you can generate graphs based on your .csv file by running the `src/image-generator.py` script.

   To use this script:

   Edit the data_filename variable in the `src/image-generator.py` file to match the name of your .csv file. For example:

   ```python
   data_filename = "my-CSV-file-without-extension"
   ```

   Once this is set, you can run the image-generator.py script to generate graphs based on the data.

   ```bash
   uv run ./src/image-generator.py
   ```
