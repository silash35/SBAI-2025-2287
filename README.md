# SBAI 2025 Article 2287

This repository contains all materials associated with the paper _“Embarque de Rede Neural Recorrente Fenomenologicamente Informada para Controle de Nível em Tanques Esféricos”_ (Embedding of a Physics-Informed Recurrent Neural Network for Level Control in Spherical Tanks), accepted for publication at the **XVII Simpósio Brasileiro de Automação Inteligente (SBAI 2025)**.

The paper presents the implementation of a Physics-Informed Recurrent Neural Network (PIRNN) on a low-cost microcontroller, where the PIRNN serves as a virtual analyzer in a cascade spherical tank system. A Proportional-Integral (PI) controller is also deployed on the microcontroller to regulate the tank levels in real time.

This repository includes the full system implementation: the PIRNN training pipeline, the Arduino firmware, and the TankSim simulation environment. All necessary files and instructions are provided to fully replicate the Hardware-in-the-Loop (HIL) setup described in the article.

The work was presented at SBAI 2025, held in São João del-Rei, Minas Gerais, Brazil. Please note that some parts of the code, such as comments and image generation functions, are written in Portuguese, as the visual outputs and documentation were tailored for a Portuguese-speaking audience.

## 📁 Folder Structure

This project organizes its components into distinct folders, with each containing a markdown file that provides detailed guidance when necessary.

### 📂 `Arduino/`

This folder contains the code that runs on the Arduino UNO microcontroller. It handles serial communication with TankSim, implements the PIRNN in C++, and includes a PI controller.

### 📂 `LaTeX/`

> ⚠️ **Note:** All materials in this folder are written in **Portuguese**, as the event took place in Brazil.

This folder contains the LaTeX source files for the presentation slides and the technical article.

### 📂 `PyTorch/`

This folder contains the code used to create and train the PIRNN using the PyTorch library.

### 📂 `TankSim/`

This folder contains the code for the TankSim software, developed in Python using the Qt framework. It simulates the tank system, enables setpoint adjustments, and communicates with the Arduino via serial connection.

## Citation

> **Accepted for publication – awaiting proceedings** 
