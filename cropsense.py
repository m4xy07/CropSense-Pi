import time
import json
import Adafruit_DHT
import Adafruit_BME280
import RPi.GPIO as GPIO
from datetime import datetime
import requests
from gpiozero import LED
from smbus2 import SMBus
from bme280 import BME280
from cropsense3 import find_best_crop
from secret import IPadd, PORT
from luma.core.interface.serial import spi
from luma.lcd.device import ili9341

# Constants
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
RAIN_PIN = 17
SOIL_MOISTURE_PIN = 27
LED_PIN = 22
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 480
BME280_ADDRESS = 0x76

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RAIN_PIN, GPIO.IN)
GPIO.setup(SOIL_MOISTURE_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

# Initialize TFT LCD display
serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)
disp = ili9341(serial, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

# Initialize BME280 sensor
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus, i2c_addr=BME280_ADDRESS)

# Server details
HOST = IPadd
PORT = PORT

def read_dht_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return humidity, temperature

def read_bme280_sensor():
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    return temperature, pressure, humidity

def read_soil_moisture():
    return GPIO.input(SOIL_MOISTURE_PIN)

def check_for_rain():
    return GPIO.input(RAIN_PIN) == 0

def display_sensor_data(humidity, temperature, pressure, soil_moisture, rain):
    with disp.canvas() as draw:
        draw.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), outline="white", fill="black")
        draw.text((10, 10), "Humidity: {:.1f}%".format(humidity), fill="white")
        draw.text((10, 30), "Temp: {:.1f}C".format(temperature), fill="white")
        draw.text((10, 50), "Pressure: {:.1f}hPa".format(pressure), fill="white")
        draw.text((10, 70), "Soil Moisture: {}".format("Wet" if soil_moisture else "Dry"), fill="white")
        draw.text((10, 90), "Raining: {}".format("Yes" if rain else "No"), fill="white")

def log_data_to_file(humidity, temperature, pressure, soil_moisture, rain):
    with open("sensor_data.log", "a") as file:
        file.write("{},{:.1f},{:.1f},{:.1f},{},{}\n".format(
            datetime.now().isoformat(), humidity, temperature, pressure, soil_moisture, rain))

def send_data_to_server(humidity, temperature, pressure, soil_moisture, rain):
    data = {
        "time": datetime.now().isoformat(),
        "humidity": humidity,
        "temperature": temperature,
        "pressure": pressure,
        "soil_moisture": soil_moisture,
        "rain": rain
    }
    response = requests.post(f"http://{HOST}:{PORT}/data", json=data)
    print("Server response:", response.text)

HIGH_TEMP_THRESHOLD = 35.0
HIGH_SOIL_MOISTURE_THRESHOLD = 80.0
HIGH_AQI_THRESHOLD = 1000

def check_alerts(temperature, soil_moisture, air_quality_index):
    if temperature > HIGH_TEMP_THRESHOLD:
        print("Alert: High Temperature Detected!")
    if soil_moisture > HIGH_SOIL_MOISTURE_THRESHOLD:
        print("Alert: High Soil Moisture Detected!")
    if air_quality_index > HIGH_AQI_THRESHOLD:
        print("Alert: High AQI Detected! Potential Fire Hazard!")

def main():
    while True:
        humidity, temperature = read_dht_sensor()
        bme_temp, pressure, bme_humidity = read_bme280_sensor()
        soil_moisture = read_soil_moisture()
        rain = check_for_rain()
        air_quality_index = 0  # Placeholder for air quality index

        if humidity is not None and temperature is not None:
            display_sensor_data(humidity, temperature, pressure, soil_moisture, rain)
            log_data_to_file(humidity, temperature, pressure, soil_moisture, rain)
            send_data_to_server(humidity, temperature, pressure, soil_moisture, rain)
            
            # Find the best crop
            month = datetime.now().strftime("%B")
            best_crop = find_best_crop(temperature, humidity, soil_moisture, month)
            if best_crop:
                print(f"Best crop to plant: {best_crop}")
            else:
                print("No suitable crop found for current conditions.")
            
            # Check alerts
            check_alerts(temperature, soil_moisture, air_quality_index)
        else:
            print("Failed to retrieve data from DHT sensor")

        time.sleep(60)

if __name__ == "__main__":
    main()
