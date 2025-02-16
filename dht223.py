import time
import board
import adafruit_dht

# Sensor type and pin configuration
DHT_SENSOR = adafruit_dht.DHT22(board.D26)

def read_dht22():                                                                                                                                                                                                                                                                                                                                                                                                                              
    try:
        temperature = DHT_SENSOR.temperature
        humidity = DHT_SENSOR.humidity
        if humidity is not None and temperature is not None:
            print(f"Temp={temperature:.1f}C  Humidity={humidity:.1f}%")
        else:
            print("Failed to retrieve data from humidity sensor")
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])

if __name__ == "__main__":
    while True:
        read_dht22()
        time.sleep(2)