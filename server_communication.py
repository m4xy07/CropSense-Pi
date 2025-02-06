import requests
from datetime import datetime
from secret import IPadd, PORT

def send_data_to_server(humidity, temperature, pressure, soil_moisture, rain):
    data = {
        "time": datetime.now().isoformat(),
        "humidity": humidity,
        "temperature": temperature,
        "pressure": pressure,
        "soil_moisture": soil_moisture,
        "rain": rain
    }
    response = requests.post(f"http://{IPadd}:{PORT}/data", json=data)
    print("Server response:", response.text)
