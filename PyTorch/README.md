# PyTorch Code

This directory contains the code for creating and training the PIRNN (Predictive Recurrent Neural Network) using the PyTorch library. It also includes the code for conducting velocity tests that compare the PIRNN with other numerical methods.

The code was tested on **Linux**. If you are using **Windows**, you can use **WSL** (Windows Subsystem for Linux) to run the code in a Linux-like environment.

This project uses **UV** to automatically manage and install all the necessary dependencies, ensuring the correct versions of both Python and the required libraries are installed.

## How to Run

1. Install [UV](https://docs.astral.sh/uv/).

1. Install [Visual Studio Code](https://code.visualstudio.com/) (VS Code).

1. Open this directory in **VS Code**.

1. The project utilizes a `pyproject.toml` file to list necessary Python packages. After setting up UV, install these dependencies by running:

   ```bash
   uv sync
   ```

1. Open `src/main.ipynb` in VS Code. Select the UV managed kernel from the kernel selection menu (`.venv`). You can now execute the notebook cells.
