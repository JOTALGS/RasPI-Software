import RPi.GPIO as GPIO
import time
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GPIOController:
    def __init__(self, sensors=[17, 27]):
        """Initialize GPIO Controller with sensor pins and logging"""
        self.sensors = sensors
        self.setup_gpio()

    def setup_gpio(self):
        """Initialize GPIO pins for sensors."""
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            for pin in self.sensors:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Use pull-down to avoid floating values
                logging.debug(f"Setup GPIO pin {pin} as INPUT with PULL_DOWN")
            
            logging.info("GPIO setup completed successfully.")
        except Exception as e:
            logging.error(f"GPIO setup failed: {str(e)}")
            raise

    def monitor_sensors(self):
        """Continuously monitor sensors and log which one is touched."""
        logging.info("Starting sensor monitoring...")
        try:
            while True:
                for i, pin in enumerate(self.sensors, start=1):
                    sensor_state = GPIO.input(pin)
                    if sensor_state:
                        logging.info(f"Sensor {i} (GPIO {pin}) Touched!")
                        print(f"Sensor {i} Touched!")  # Keep this for real-time feedback
                time.sleep(0.1)
        except KeyboardInterrupt:
            logging.info("Exiting due to KeyboardInterrupt...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup GPIO resources on exit."""
        GPIO.cleanup()
        logging.info("GPIO cleanup completed.")
