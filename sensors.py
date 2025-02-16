import time
import board
import adafruit_dht
from gpiozero import InputDevice
import smbus2
import bme280s
from mq135 import read_mq135

# Constants
DHT_SENSOR = adafruit_dht.DHT22(board.D26)
RAIN_PIN = 17
SOIL_MOISTURE_PIN = 27
BME280_ADDRESS = 0x76
DEBUG = 1  # Set this to 0 to disable debug prints

# Initialize sensors
rain_sensor = InputDevice(RAIN_PIN)
soil_moisture_sensor = InputDevice(SOIL_MOISTURE_PIN)

# Initialize BME280 sensor
bus = smbus2.SMBus(1)
calibration_params = bme280s.load_calibration_params(bus, BME280_ADDRESS)

def debug_print(message):
    if DEBUG:
        print(message)

def read_dht_sensor():
    try:
        temperature = DHT_SENSOR.temperature
        humidity = DHT_SENSOR.humidity
        debug_print(f"DHT Sensor - Temperature: {temperature}, Humidity: {humidity}")
        return humidity, temperature
    except RuntimeError as error:
        print(f"DHT Sensor error: {error.args[0]}")
        return None, None
    except Exception as e:
        print(f"Unexpected error reading DHT sensor: {str(e)}")
        return None, None

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def read_bme280_sensor():
    try:
        data = bme280s.sample(bus, BME280_ADDRESS, calibration_params)
        temperature_celsius = data.temperature
        pressure = data.pressure
        humidity = data.humidity
        temperature_fahrenheit = celsius_to_fahrenheit(temperature_celsius)
        debug_print(f"BME280 Sensor - Temperature: {temperature_celsius} °C, {temperature_fahrenheit} °F, Pressure: {pressure} hPa, Humidity: {humidity} %")
        return temperature_celsius, pressure, humidity
    except Exception as e:
        print(f"Unexpected error reading BME280 sensor: {str(e)}")
        return None, None, None

def read_soil_moisture():
    try:
        is_active = soil_moisture_sensor.is_active
        debug_print(f"Soil Moisture Sensor - Is Active: {is_active}")
        return is_active
    except Exception as e:
        print(f"Unexpected error reading soil moisture sensor: {str(e)}")
        return None

def check_for_rain():
    try:
        is_active = rain_sensor.is_active
        debug_print(f"Rain Sensor - Is Active: {is_active}")
        return is_active
    except Exception as e:
        print(f"Unexpected error reading rain sensor: {str(e)}")
        return None

def read_air_quality():
    ppm = read_mq135()
    debug_print(f"MQ135 Sensor - CO2 PPM: {ppm}")
    return ppm






