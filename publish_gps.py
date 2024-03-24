import serial
import pynmea2
from datetime import datetime
import paho.mqtt.publish as publish
import json 

while True:
    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=2)
    
    # Read data from the serial port
    newdata = ser.readline().decode('latin-1')
    
    # Check if the sentence is $GPRMC
    if newdata.startswith("$GPRMC"):
        # Parse the $GPRMC sentence
        newmsg = pynmea2.parse(newdata)
        
        # Extract latitude and longitude
        lat = newmsg.latitude
        lng = newmsg.longitude
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        # Publish GPS data to MQTT broker
        payload = {
            "timestamp": timestamp,
            "latitude": lat,
            "longitude": lng
        }
        publish.single("paho/test/topic", json.dumps(payload), hostname="40.67.233.215")
        
        # Print timestamp, latitude, and longitude
        print("[{}] Latitude={}, Longitude={}".format(timestamp, lat, lng))
