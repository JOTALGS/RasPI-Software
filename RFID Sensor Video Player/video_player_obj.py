import re
import sys
import mpv
import time
import signal
import serial
import logging
import threading
import tkinter as tk
from parse_xml import parse_xml

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class VideoSensorController:
    def __init__(self, serial_port="/dev/ttyUSB0", baud_rate=9600):
        self.player = VideoPlayer()
        self.current_video = 1
        self.running = True
        self.ser = serial.Serial(serial_port, baud_rate, timeout=1)  # Initialize RFID reader
        logging.basicConfig(level=logging.INFO)

    def setup(self):
        """Initialize the video player and start the RFID listener"""
        if not self.player.setup():
            logging.error("Failed to initialize video player")
            return False
        logging.info(f"Listening for RFID scans on {self.ser.portstr}...")
        return True
    
    def rfid_thread(self):
        """Monitor RFID scans in a separate thread"""
        logging.info("Starting RFID monitoring thread")
        while self.running:
            try:
                card_id = self.ser.readline().decode().strip()  # Read RFID data
                if card_id:
                    logging.info(f"RFID Card Scanned: {card_id}")
                    self.handle_rfid_scan(card_id)
            except Exception as e:
                logging.error(f"Error reading RFID: {str(e)}")
            time.sleep(0.1)
    
    def handle_rfid_scan(self, card_id):
        """Handle RFID scan events and change the video"""
        # Assuming card_id is mapped to video numbers in some way, modify as needed
        try:
            sensor_num = card_id  # You may need to adjust how card_id corresponds to video numbers
            if sensor_num != self.current_video:
                logging.info(f"Changing video to {sensor_num}")
                self.current_video = sensor_num
                self.player.play_video(sensor_num)
        except ValueError:
            logging.error(f"Invalid RFID card ID: {card_id}")

    def start(self):
        """Start video playback and RFID monitoring in parallel"""
        # Create and start RFID monitoring thread
        rfid_thread = threading.Thread(target=self.rfid_thread)
        rfid_thread.daemon = True  # Thread will exit when main program exits
        rfid_thread.start()

        # Start initial video
        #self.player.play_video(self.current_video)
        
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        self.ser.close()  # Close the serial port
        self.player.cleanup()


class VideoPlayer:
    def __init__(self):
        self.video_paths = []
        self.screensaver_path = None
        self.sensor_pins = None
        self.player = None
        self.running = True
        self._current_video = None
        self._play_lock = threading.Lock()
        self.black_screen_color = "0/0/0"

    def _process_end_file(self, event):
        try:
            event_str = str(event)
            if "reason': b'eof'" in event_str:
                #self.play_video(1)
                pass
        except Exception as e:
            logging.error(f"Error processing end file: {str(e)}")

    def setup(self):
        """Initialize player and load settings from XML"""
        try:
            logging.info("Starting setup...")
            
            # Parse XML configuration
            logging.debug("Parsing XML configuration...")
            self.video_paths, self.screensaver_path, self.sensor_pins = parse_xml()
            self.video_paths["1"] = self.screensaver_path
            logging.debug(f"Found {len(self.video_paths)} video paths")
            
            # Initialize MPV player with Raspberry Pi specific settings
            logging.debug("Initializing MPV player...")
            self.player = mpv.MPV(
                ytdl=True,
                vo='gpu',
                hwdec='rpi',
                fullscreen=True,
                loop=False,
                input_default_bindings=True,
                input_vo_keyboard=True,
                ontop=True,
                keepaspect=True,  # Maintain video aspect ratio
                screen=0,
            )
            
            # Set up end-file event callback
            @self.player.event_callback('end-file')
            def handle_end_file(event):
                # Process in a separate thread to minimize delay
                threading.Thread(target=self._process_end_file, args=(event,)).start()
            
            # Set up simple key binding for quit
            @self.player.on_key_press('q')
            def handle_q(*args):
                logging.info("Quit key pressed")
                self.cleanup()
            
            @self.player.on_key_press('ESC')
            def handle_esc(*args):
                logging.info("ESC key pressed")
                self.cleanup()
            
            # Register signal handlers
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            
            logging.info("Setup completed successfully")
            return True
            
        except Exception as e:
            logging.error(f"Setup failed: {str(e)}", exc_info=True)
            return False

    def play_video(self, video_index):
        """Play a specific video by index - non-blocking"""
        start_time = time.time()

        with self._play_lock:  # Ensure thread-safe video switching
            try:
                #logging.debug(f"Video paths: {self.video_paths}")

                logging.info(f"Attempting to play video index {video_index}")
                
                if not self.video_paths:
                    logging.error("No video paths available")
                    return
                    
                allowed_vids = [str(item).strip() for item in self.video_paths.keys()]

                video_index = re.sub(r'[\x00-\x1F\x7F]', '', str(video_index))

                if str(video_index) in allowed_vids:
                    video_file = self.video_paths[video_index]
                    logging.info(f"Playing video: {video_file}")
                    
                    # Verify file exists
                    """
                    try:
                        with open(video_file, 'r') as f:
                            pass
                    except IOError as e:
                        logging.error(f"Video file not accessible: {str(e)}")
                        return
                    """
                    
                    # Stop current video if playing
                    self.player.stop()
                    
                    # Start new video
                    self._current_video = video_index
                    self.player.play(video_file)
                    logging.debug("Video playback started")
                    
                else:
                    logging.error(f"Invalid video index {video_index}. Valid range: {list(self.video_paths.keys())}")
                logging.debug(f"Video change took {time.time() - start_time} seconds")
            except Exception as e:
                logging.error(f"Playback error: {str(e)}", exc_info=True)
    
    def cleanup(self):
        """Clean up resources and exit"""
        logging.info("Starting cleanup...")
        self.running = False
        if self.player:
            try:
                # First try to stop playback
                self.player.stop()
                # Give a small delay for the player to stop
                time.sleep(0.1)
                # Then terminate the player
                self.player.terminate()
                logging.info("Player terminated successfully")
            except Exception as e:
                logging.error(f"Error during player termination: {str(e)}")
                # If termination fails, try to force close the player
                try:
                    self.player._close()
                except:
                    pass
            finally:
                self.player = None
                sys.exit(0)
    
    def signal_handler(self, signum, frame):
        """Handle system signals (Ctrl+C)"""
        logging.info(f"Signal {signum} received. Cleaning up...")
        self.cleanup()
