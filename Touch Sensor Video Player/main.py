import sys
import logging
import threading
import time
from video_player_obj import VideoSensorController
from image_saver import open_image_fullscreen_non_blocking

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():

    IMAGE_PATH = '/home/pi/Pictures/abstract-textured-w.jpg'
    open_image_fullscreen_non_blocking(IMAGE_PATH)
    
    logging.info("Starting video player application")
    
    controller = VideoSensorController()
    if not controller.setup():
        logging.error("Failed to initialize controller")
        sys.exit(1)
    
    try:
        controller.start()
        # Keep main thread alive
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        background.close()
        logging.info("Keyboard interrupt received")
    except Exception as e:
        background.close()
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
    finally:
        background.close()
        controller.cleanup()

if __name__ == "__main__":
    main()
