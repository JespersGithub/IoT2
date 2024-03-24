import time
import paho.mqtt.publish as publish
from mcp3021 import MCP3021

# Define ADC pin (connected to MCP3021)
adc = MCP3021()

# Define battery parameters
max_voltage = 2.05  # Maximum voltage of battery when fully charged
min_voltage = 1.42  # Minimum voltage of battery when nearly discharged

def battery_percentage(voltage):
    # Calculate percentage based on voltage
    percentage = ((voltage - min_voltage) / (max_voltage - min_voltage)) * 100
    return max(0, min(100, percentage))  # Ensure percentage is between 0 and 100

try:
    while True:
        # Read ADC value (10-bit resolution, returns value between 0 and 1)
        voltage_value = float(adc.get_voltage())

        # Calculate battery percentage
        percentage = battery_percentage(voltage_value)

        # Publish battery percentage via MQTT
        publish.single("battery/percentage", str(percentage), hostname="40.67.233.215")

        # Wait for some time before taking the next reading
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram terminated by user.")
