# FloraVue Project

## Read requairements file to install crucial dependices
## FloraVueSketch have to be uploaded to own arduino device
## You have to install the app.py file along with the start_app of choice as start_up doesnt have code for the moniotor it only start the app

## Overview

**FloraVue** is a plant monitoring system that utilizes an **Arduino** for sensor readings, displaying the data in a user-friendly **Streamlit** dashboard built with Python. This system allows you to monitor the health and environment of your plants in real-time.

## Features
- Real-time monitoring of:
  - Air quality (using **MQ-135** sensor)
  - Temperature and humidity (using **DHT22** sensor)
  - Light intensity (using **BH1750** sensor)
  - Soil moisture levels (using a **soil moisture sensor**)
- Display of sensor data in a clear, interactive web dashboard.
- Easy setup and use through a simple Python-based UI (Streamlit).

## Hardware Components
- **Arduino Uno**: The microcontroller that collects data from the sensors and sends it to the Python application.
- **MQ-135 Sensor**: Measures air quality (e.g., CO2 levels).
- **DHT22 Sensor**: Measures temperature and humidity.
- **BH1750 Sensor**: Measures ambient light intensity.
- **Soil Moisture Sensor**: Monitors soil moisture to gauge plant watering needs.

## Software
- **Python 3.x**
- **Streamlit**: Web UI framework for building the interactive dashboard.
- **PySerial**: For serial communication between the Arduino and the Python application.
- **Sensor Libraries**: Libraries specific to each sensor for easy data reading (e.g., `Adafruit_DHT` for the DHT22 sensor).

## How to Run the Project

### 1. Clone the repository:
```bash
git clone https://github.com/username/FloraVueProject.git
cd FloraVueProject

