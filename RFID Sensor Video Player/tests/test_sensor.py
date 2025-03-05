import serial

# Change to your device's USB port (use `ls /dev/ttyUSB*` to check)
SERIAL_PORT = "/dev/ttyUSB0"  
BAUD_RATE = 9600  

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Listening for RFID scans on {SERIAL_PORT}...")
    
    while True:
        card_id = ser.readline().decode().strip()
        if card_id:
            print(f"Card Scanned: {card_id}")

except serial.SerialException as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("\nExiting...")
