from luma.core.interface.serial import spi
from luma.lcd.device import ili9341

# Constants
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 480

# Initialize TFT LCD display
serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)
disp = ili9341(serial, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

def display_sensor_data(humidity, temperature, pressure, soil_moisture, rain):
    with disp.canvas() as draw:
        draw.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), outline="white", fill="black")
        draw.text((10, 10), "Humidity: {:.1f}%".format(humidity), fill="white")
        draw.text((10, 30), "Temp: {:.1f}C".format(temperature), fill="white")
        draw.text((10, 50), "Pressure: {:.1f}hPa".format(pressure), fill="white")
        draw.text((10, 70), "Soil Moisture: {}".format("Wet" if soil_moisture else "Dry"), fill="white")
        draw.text((10, 90), "Raining: {}".format("Yes" if rain else "No"), fill="white")
