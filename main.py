import time
import json
from datetime import datetime
import requests
from gpiozero import LED
from sensors import read_dht_sensor, read_bme280_sensor, read_soil_moisture, check_for_rain, read_air_quality, read_npk_sensor
from display import display_sensor_data
from data_logging import log_data_to_file
from server_communication import send_data_to_server
from crop_recommendation import find_best_crop
from alerts import check_alerts
from secret import IPadd, PORT

# Constants
HIGH_TEMP_THRESHOLD = 35.0
HIGH_SOil_MOISTURE_THRESHOLD = 80.0
HIGH_AQI_THRESHOLD = 1000

def main():
    while True:
        humidity, temperature = read_dht_sensor()
        bme_temp, pressure, bme_humidity = read_bme280_sensor()
        soil_moisture = read_soil_moisture()
        rain = check_for_rain()
        air_quality_index = read_air_quality()
        nitrogen, phosphorus, potassium = read_npk_sensor()

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
