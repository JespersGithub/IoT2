import RPi.GPIO as GPIO
import time
import json
import paho.mqtt.publish as publish

# Set GPIO pins
TRIG_PIN = 17
ECHO_PIN = 18

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    pulse_start = time.time()
    pulse_end = time.time()
    
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound is 343 m/s, but sound travels forth and back
    distance = round(distance, 2)

    return distance

def cleanup():
    GPIO.cleanup()

def publish_distance():
    try:
        setup()
        while True:
            distance = measure_distance()
            data = {"distance": distance}
            publish.single("paho/test/topic", json.dumps(data), hostname="40.67.233.215")
            print("Distance published:", distance, "cm")
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()

if __name__ == '__main__':
    publish_distance()
