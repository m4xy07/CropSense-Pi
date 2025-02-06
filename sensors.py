import Adafruit_DHT
import RPi.GPIO as GPIO
from smbus2 import SMBus
from bme280 import BME280

# Constants
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
RAIN_PIN = 17
SOIL_MOISTURE_PIN = 27
BME280_ADDRESS = 0x76

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RAIN_PIN, GPIO.IN)
GPIO.setup(SOIL_MOISTURE_PIN, GPIO.IN)

# Initialize BME280 sensor
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus, i2c_addr=BME280_ADDRESS)

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
