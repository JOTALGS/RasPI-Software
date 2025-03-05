

import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM (Broadcom SOC channel numbering)
SENSORS = [17, 27]  # GPIO pins for n sensors

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in SENSORS:
    GPIO.setup(pin, GPIO.IN)

try:
    while True:
        for i, pin in enumerate(SENSORS, start=1):
            if GPIO.input(pin):
                print(f"Sensor {i} Touched!")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
