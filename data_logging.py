from datetime import datetime

def log_data_to_file(humidity, temperature, pressure, soil_moisture, rain):
    with open("sensor_data.log", "a") as file:
        file.write("{},{:.1f},{:.1f},{:.1f},{},{}\n".format(
            datetime.now().isoformat(), humidity, temperature, pressure, soil_moisture, rain))
