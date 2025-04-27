
#include <Wire.h>
#include <BH1750.h>
#include <DHT.h>

#define DHTPIN 2          // DHT22 connected to digital pin 2
#define DHTTYPE DHT22     // DHT22 type
#define SOIL_PIN A0       // Soil moisture sensor on A0
#define MQ135_PIN A1     // MQ-135 sensor on A1

DHT dht(DHTPIN, DHTTYPE);
BH1750 lightMeter;

void setup() {
    Serial.begin(9600);
    Wire.begin();
    dht.begin();
    lightMeter.begin();
    
    pinMode(SOIL_PIN, INPUT);
    pinMode(MQ135_PIN, INPUT);
}

void loop() {
    // Read DHT22 sensor data
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    // Read Soil Moisture Sensor
    int soilMoisture = analogRead(SOIL_PIN);
    
    // Read MQ-135 Air Quality Sensor
    int airQuality = analogRead(MQ135_PIN);
        
    // Read BH1750 Light Intensity Sensor
    float lux = lightMeter.readLightLevel();

    // Print sensor values
    Serial.println("Sensor Readings:");
    Serial.print("Temperature: "); Serial.print(temperature); Serial.println(" °C");
    Serial.print("Humidity: "); Serial.print(humidity); Serial.println(" %");
    Serial.print("Soil Moisture: "); Serial.println(soilMoisture);
    Serial.print("Air Quality (MQ135): "); Serial.println(airQuality);
    Serial.print("Light Intensity (BH1750): "); Serial.print(lux); Serial.println(" lx");
    Serial.println("---------------------------");

    delay(2000); // Delay for readability
}
