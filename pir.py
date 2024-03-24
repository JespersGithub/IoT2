import RPi.GPIO as GPIO
from time import sleep

# Define GPIO pin numbers for the PIR sensor and stepper motor
PIR_PIN = 12  # Example pin, adjust as per your setup
IN1 = 10  # jp1 - 8 = jp3 - 10
IN2 = 7 #jp1 -8 = jp3 -10
IN3 = 8 #jp1 -10 = jp3 - 8
IN4 = 11 #

# Set up GPIO for the PIR sensor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)

# Set up GPIO for the stepper motor
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

pins = [IN1, IN2, IN3, IN4]

sequence_clockwise = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
sequence_counterclockwise = list(reversed(sequence_clockwise))  # Reverse the sequence for counterclockwise rotation

try:
    print("PIR sensor test (Press Ctrl+C to exit)")
    pir_triggered = 0

    while True:
        if GPIO.input(PIR_PIN) == GPIO.HIGH:  # If motion is detected
            print("Motion detected!")
            pir_triggered += 1
            if pir_triggered == 1:  # After first movement
                print("Rotating 90 degrees counterclockwise")
                for _ in range(512):  # 512 steps for 90 degrees, adjust as needed for your motor
                    for step in sequence_counterclockwise:
                        for i in range(len(pins)):
                            GPIO.output(pins[i], step[i])
                        sleep(0.01)
                break  # Exit the loop after counterclockwise rotation
        else:
            print("No motion")
        sleep(0.5)  # Adjust delay as needed for motion detection frequency

    while True:  # Wait for second movement to rotate clockwise
        if GPIO.input(PIR_PIN) == GPIO.HIGH:  # If motion is detected again
            print("Second motion detected!")
            print("Rotating 90 degrees clockwise")
            for _ in range(512):  # 512 steps for 90 degrees, adjust as needed for your motor
                for step in sequence_clockwise:
                    for i in range(len(pins)):
                        GPIO.output(pins[i], step[i])
                    sleep(0.01)
            break  # Exit the loop after clockwise rotation
        else:
            print("No motion")
        sleep(0.5)  # Adjust delay as needed for motion detection frequency

except KeyboardInterrupt:
    print("\nExiting program")
finally:
    GPIO.cleanup()


