import psutil
import os
import subprocess
import serial

# Change to your device's USB port (use `ls /dev/ttyUSB*` to check)
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600


def check_and_kill_port_usage(port='/dev/ttyUSB0'):
    # Run lsof to check if the port is being used by any process
    try:
        # Use subprocess to run the lsof command to get the PID of the process using the port
        result = subprocess.run(['lsof', port], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # If no output is returned, the port is not in use
        if result.stdout:
            # Decode the result
            result_str = result.stdout.decode('utf-8')

            # Split the output into lines, the second line contains the PID
            lines = result_str.splitlines()
            pid_line = lines[1].split()
            pid = int(pid_line[1])

            # Kill the process
            os.kill(pid, 9)
            print(f"Process {pid} using {port} has been killed.")
        else:
            print(f"{port} is not being used by any process.")
    except Exception as e:
        print(f"Error: {e}")

try:
    print("Press << Ctrl + c >> to exit.")
    check_and_kill_port_usage()
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    print(f"Listening for RFID scans on {SERIAL_PORT}...")

    while True:
        card_id = ser.readline().decode().strip()
        if card_id:
            print(f"Card Scanned: {card_id}")

except serial.SerialException as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("\nExiting...")
