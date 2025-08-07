# Arduino Code

This directory contains the code that runs on the Arduino microcontroller. It includes an implementation of a PID controller and a C++ implementation of the PIRNN.

The article uses a PI controller, but the code already implements a PID controller, with the default value for the derivative constant (Kd) set to zero. You can experiment by modifying this parameter and observe how it affects the system.

## How to Run

The code has been tested on **Arduino UNO** and **Arduino Nano**, but it should work on other compatible boards. To upload the code to your board, follow these steps:

1. Install [Visual Studio Code](https://code.visualstudio.com/) (VS Code).
1. Open this directory in VS Code.
1. Make sure all recommended extensions in `.vscode/extensions.json` are installed.
1. Connect your Arduino to your computer via USB.
1. Compile and upload the code to the board using PlatformIO.

If you're familiar with Arduino, you are not obligated to use VS Code. You can upload the code using your preferred IDE or method.

For more details on using PlatformIO, refer to the [PlatformIO website](https://platformio.org/) and the [PlatformIO documentation](https://docs.platformio.org/en/latest/).

## How to Modify the Code

To edit the code, we recommend using VS Code with the project's recommended extensions.

You can modify some aspects of the code without changing the actual code by simply editing the **`src/config.hpp`** file. This file allows you to configure general settings, including the PID controller constants.

Similarly, if you want to use your own Neural Network, you can modify the **`src/model.hpp`** file to adjust the model parameters to your needs.

Before making modifications, read the PlatformIO documentation and familiarize yourself with the project files. This will help prevent compilation errors and ensure the system runs correctly.
