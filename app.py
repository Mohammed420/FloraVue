import serial
import pandas as pd
import os
import time
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy
import platform

# Initialization status

def get_serial_port():
    system = platform.system()

    if system == 'Windows':
        return 'COM3'  # Change to your actual COM port (e.g., COM4, COM5)
    elif system == 'Linux':
        return '/dev/ttyUSB0'  # Or /dev/ttyACM0 depending on your device
    elif system == 'Darwin':  # macOS
        # Automatically find the first USB serial device
        for device in os.listdir('/dev'):
            if device.startswith('tty.usbserial') or device.startswith('tty.usbmodem'):
                return os.path.join('/dev', device)
        raise FileNotFoundError("No serial device found on macOS")
    else:
        raise EnvironmentError(f"Unsupported platform: {system}")

# Use the detected port
port = get_serial_port()
ser = serial.Serial(port, 9600)
print(f"Connected to {port}")  
#End of platform port cheking

csv_file = 'floraVue.csv'
st.title('🌱 FloraVue plant monitoring dashboard')

ph1 = st.empty()  # PLACE HOLDERS with average then chart place holders
average_ph1 = st.empty()
# ph1_cond = st.empty()
ph2 = st.empty()
average_ph2 = st.empty()
ph3 = st.empty()
average_ph3 = st.empty()
ph4 = st.empty()
average_ph4 = st.empty()
ph5 = st.empty()
average_ph5 = st.empty()
ph6 = st.empty()
average_ph6 = st.empty()
chart_temp = st.empty()
chart_hum = st.empty()
chart_soil = st.empty()
chart_air = st.empty()
chart_lig  = st.empty()

sensor_data = {}  # Dictionary to store incoming sensor values
x = 0  # Index offset

try:
    # If file doesn't exist or is empty, create it with header
    if not os.path.exists(csv_file) or os.stat(csv_file).st_size == 0:
        df = pd.DataFrame(columns=['Index', 'Temperature', 'Humidity', 'Soil Moisture', 'Air Quality', 'Light'])
        df.to_csv(csv_file, index=False)
    else:
        df = pd.read_csv(csv_file)
except FileNotFoundError:
    df = pd.DataFrame(columns=['Index','Temperature', 'Humidity', 'Soil Moisture', 'Air Quality', 'Light'])
    df.to_csv(csv_file, index=False)

if not df.empty:
    last_index = df['Index'].iloc[-1]
else:
    last_index = 0

with open("data.txt", "a") as file:
    file.write("Temp  Hum  Soil moist  Air quality  Light intense.\n")

# end on initialization
print("Logging started... Press Ctrl+C to stop.")

while True:
    line = ser.readline().decode('utf-8').strip()
    try:
        if "Temperature" in line and ":" in line:
            temp_str = line.split(":")[1].split("°")[0].strip()
            sensor_data['Temperature'] = float(temp_str)
        elif "Humidity" in line and ":" in line:
            hum_str = line.split(":")[1].split("%")[0].strip()
            sensor_data['Humidity'] = float(hum_str)
        elif "Soil Moisture" in line and ":" in line:
            soilM_str = line.split(":")[1].strip()
            sensor_data['Soil Moisture'] = int(soilM_str)
        elif "Air Quality" in line and ":" in line:
            airQ_str = line.split(":")[1].strip()
            sensor_data['Air Quality'] = float(airQ_str)
        elif "Light Intensity" in line and ":" in line:
            lig_str = line.split(":")[1].split("lx")[0].strip()
            sensor_data['Light'] = float(lig_str)
    except (ValueError, IndexError):
        continue
    
    if len(sensor_data) == 5:
        x += 1
        current_index = x + last_index
        
        # Append to CSV
        new_data = pd.DataFrame([{
            'Index': current_index,
            'Temperature': sensor_data['Temperature'],
            'Humidity': sensor_data['Humidity'],
            'Soil Moisture': sensor_data['Soil Moisture'],
            'Air Quality': sensor_data['Air Quality'],
            'Light': sensor_data['Light']
        }])
        new_data.to_csv(csv_file, mode='a', index=False, header=False)

        # Append to txt file
        with open("data.txt", 'a') as file: 
            file.write(str(current_index))
            file.write(" > " + str(sensor_data['Temperature']) + "      " +
                       str(sensor_data['Humidity']) + "      " +
                       str(sensor_data['Soil Moisture']) + "      " +
                       str(sensor_data['Air Quality']) + "      " +
                       str(sensor_data['Light']) + '\n')
        #----------------------------------------------------------------------- Calc avg min max
        # Update statistics using the updated CSV
        df = pd.read_csv(csv_file)

        temp_column = pd.to_numeric(df["Temperature"], errors='coerce')
        hum_column = pd.to_numeric(df["Humidity"], errors='coerce')
        soil_column = pd.to_numeric(df["Soil Moisture"], errors='coerce')
        air_column = pd.to_numeric(df["Air Quality"], errors='coerce')
        lig_column = pd.to_numeric(df["Light"], errors='coerce')

        average_temp = temp_column.mean()
        average_hum = hum_column.mean()
        average_soil = soil_column.mean()
        average_air = air_column.mean()
        average_lig = lig_column.mean()

        min_temp = temp_column.min()
        min_hum = hum_column.min()
        min_soil = soil_column.min()
        min_air = air_column.min()
        min_lig = lig_column.min()

        max_temp = temp_column.max()
        max_hum = hum_column.max()
        max_soil = soil_column.max()
        max_air = air_column.max()
        max_lig = lig_column.max()
        #----------------------------- End of avg min max
        #Condtions
        temp_cond = ""
        hum_cond = ""
        if(sensor_data["Temperature"] < 10):
            temp_cond = "Cold"
            color = 'blue'
        elif(sensor_data["Temperature"] > 10 and sensor_data['Temperature'] <= 27):
            temp_cond = "Normal"
            color = 'green'
        elif(sensor_data["Temperature"] >= 27.1): # >= 28
            temp_cond = "Hot"
            color = 'red'

        if(sensor_data['Humidity'] < 30):
            hum_cond = 'Low humidty'
            hum_color = 'red'
        elif(sensor_data['Humidity'] > 30 and sensor_data['Humidity'] <= 60):
            hum_cond = 'Normal humidty'
            hum_color = 'green'
        elif(sensor_data['Humidity'] > 60.1):
            hum_cond = 'High humidty'
            hum_color = 'red'

        soil_moist_percent = (800 - sensor_data['Soil Moisture']) / (800 - 200) * 100
        
        # Update UI metrics
        with ph1.container():#Index metric
            st.metric(label='Index', value=f"{x + last_index}")
        with ph2.container():# Temperature metric
            st.metric(label=f'**🌡️ Temperature (C)**', value=f"{sensor_data['Temperature']} °C")
            average_ph2.markdown(f"<span style='font-size: 12px; color: gray;'>Avg: {average_temp:.2f} Min: {min_temp} Max: {max_temp}°C</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 16px; color: {color};'>{temp_cond}</span>", unsafe_allow_html=True)
            
        with ph3.container():#Humidty metirc
            st.metric(label='**💧 Humidity %**', value=f"{sensor_data['Humidity']} %")
            average_ph3.markdown(f"<span style='font-size: 12px; color: gray;'>Avg: {average_hum:.2f} Min: {min_hum} Max: {max_hum}%</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 16px; {hum_color};'>{hum_cond}</span>", unsafe_allow_html=True)
        with ph4.container():# Soil moisture metric
            st.metric(label='**🪴 Soil Moisture**', value=f'{str(round(soil_moist_percent, 2))}%')
            average_ph4.markdown(f"<span style='font-size: 12px; color: gray;'>Avg: {average_soil:.2f} Min: {min_soil} Max: {max_soil}</span>", unsafe_allow_html=True)
        with ph5.container():#Air quality metric
            st.metric(label="**🌬️ Air Quality**", value=str(sensor_data['Air Quality']))
            average_ph5.markdown(f"<span style='font-size: 12px; color: gray;'>Avg: {average_air:.2f} Min: {min_air} Max: {max_air}</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 12px; color: gray;'>Lower is more quality</span>", unsafe_allow_html=True)
        with ph6.container():#Light intenseity metric
            st.metric(label="**💡 Light Intensity**", value=f"{sensor_data['Light']} lx")
            average_ph6.markdown(f"<span style='font-size: 12px; color: gray;'>Avg: {average_lig:.2f} Min: {min_lig} Max: {max_lig}lx</span>", unsafe_allow_html=True)
        #End of metrics place holders
        
        #start chart, chart place holders
        #-------------------------------------------------
        def plot_sensor_chart(container, df, column_name, title, ylabel, color):
            # Create a clean copy and convert to numpy arrays
            df_clean = df[['Index', column_name]].copy()
            
            # Convert to numeric values
            df_clean['Index'] = pd.to_numeric(df_clean['Index'], errors='coerce')
            df_clean[column_name] = pd.to_numeric(df_clean[column_name], errors='coerce')
            
            # Drop NA and reset index
            df_clean = df_clean.dropna().reset_index(drop=True)
            
            with container.container():
                if not df_clean.empty:
                    fig, ax = plt.subplots()
                    
                    # Convert to primitive numpy arrays
                    x = df_clean['Index'].to_numpy().flatten()  # Explicit flattening
                    y = df_clean[column_name].to_numpy().flatten()
                    
                    # Use matplotlib directly for plotting
                    ax.plot(x, y, color=color, marker='o', markersize=3, linestyle='-')
                    
                    ax.set_title(title)
                    ax.set_ylabel(ylabel)
                    ax.set_xlabel("Reading Index")
                    st.pyplot(fig)
                else:
                    st.warning(f"No data available for {column_name}")
        #-------------------------------------------------
        #Defention for use for the 5 charts
        plot_sensor_chart(chart_temp, df, "Temperature", "🌡️ Temperature over Time", "°C", "tomato")
        plot_sensor_chart(chart_hum, df, "Humidity", "💧 Humidity over Time", "%", "skyblue")
        plot_sensor_chart(chart_soil, df, "Soil Moisture", "🌱 Soil Moisture over Time", "", "green")
        plot_sensor_chart(chart_air, df, "Air Quality", "🍃 Air Quality over Time", "", "orange")
        plot_sensor_chart(chart_lig, df, "Light", "💡 Light Intensity over Time", "lx", "gold")
        # End of charts
                
        sensor_data = {}  # Clear after logging

    time.sleep(0.1)
