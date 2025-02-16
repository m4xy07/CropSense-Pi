import sys
import os
import time
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from DFRobot_RaspberryPi_Expansion_Board import DFRobot_Expansion_Board_IIC as Board

# Constants
ADC_CHANNEL = Board.A0
RLOAD = 22.0  # Use 22KΩ as suggested in the article
ATMOCO2 = 440  # Atmospheric CO2 level for calibration
PARA = 116.6020682  # Default parameter for MQ-135
PARB = 2.769034857  # Default exponent for MQ-135

# Default RZERO (Will be dynamically updated)
RZERO = 90.0

# Initialize Board
board = Board(1, 0x10)

def get_resistance(adc_value):
    """Compute sensor resistance (Rs) using the correct formula."""
    """For sensor resistance it seems to vary a lot from 0.10 to 22.35KO, it is not stable
    therefore I will use the formula from the article to calculate the resistance
    from the ADC value."""
    if adc_value <= 0:
        return float('inf')  # Prevent division by zero
    if adc_value >= 1023:
        return 0.1  # Prevent near-zero resistance
    return ((1023.0 / adc_value) - 1.0) * RLOAD  # Corrected formula

def get_rzero(adc_value):
    """Calculate the sensor's RZERO based on atmospheric CO₂."""
    Rs = get_resistance(adc_value)
    return 12  # Add 2Ω to compensate for sensor tolerance

def get_ppm(adc_value):
    """Calculate CO₂ PPM using dynamically calibrated RZERO."""
    Rs = get_resistance(adc_value)
    ppm = PARA * pow((6 / RZERO), -PARB)
    return min(ppm, 10000)  # Increase cap to 10,000ppm

def read_mq135():
    """Read ADC value, compute CO₂ concentration, and print results."""
    try:
        adc_value = board.get_adc_value(ADC_CHANNEL)
        resistance = get_resistance(adc_value)
        ppm = get_ppm(adc_value)

        print(f"ADC Value: {adc_value}, Resistance: {resistance:.2f}kΩ, PPM: {ppm:.2f}")
        return ppm
    except Exception as e:
        print(f"Error reading MQ-135 sensor: {str(e)}")
        return None

if __name__ == "__main__":
    while board.begin() != board.STA_OK:
        print("Board initialization failed, retrying...")
        time.sleep(2)
    print("Board successfully initialized")

    board.set_adc_enable()

    # Get initial ADC value for dynamic RZERO calibration
    adc_value = board.get_adc_value(ADC_CHANNEL)
    dynamic_rzero = get_rzero(adc_value)
    RZERO = dynamic_rzero  # Update RZERO dynamically
    print(f"Calibrated RZERO: {dynamic_rzero:.2f} (Updated)")

    while True:
        ppm = read_mq135()
        print(f"CO2 PPM: {ppm:.2f}")
        time.sleep(2)
