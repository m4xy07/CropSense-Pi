import serial

def read_npk_sensor():
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.flush()
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            npk_values = line.split(',')
            nitrogen = float(npk_values[0])
            phosphorus = float(npk_values[1])
            potassium = float(npk_values[2])
            return nitrogen, phosphorus, potassium
    except Exception as e:
        print(f"Error reading NPK sensor: {e}")
        return None, None, None
