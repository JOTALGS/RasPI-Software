#!/bin/bash

sudo apt install python3-mpv
sudo apt install feh
sudo apt install unclutter

SERVICE_FILE="/etc/systemd/system/rfidsens.service"

if [ ! -f "$SERVICE_FILE" ]; then
    echo "Creating rfidsens.service..."
    sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=RFID Sensor Startup Script
After=graphical.target network-online.target display-manager.service
Wants=graphical.target network-online.target
Requires=display-manager.service

[Service]
Type=simple
User=pi
Group=pi

ExecStartPre=/bin/sleep 10
# Use absolute path to Python and script
ExecStart=/usr/bin/python3 /home/pi/Documents/RasPI-Software-main/RFIDSensorVideoPlayer/main.py

# Working directory
WorkingDirectory=/home/pi/Documents/RasPI-Software-main/RFIDSensorVideoPlayer

# Logging
StandardOutput=append:/home/pi/Documents/RasPI-Software-main/RFIDSensorVideoPlayer/logs/systemd_stdout.log
StandardError=append:/home/pi/Documents/RasPI-Software-main/RFIDSensorVideoPlayer/logs/systemd_stderr.log

# Environment setup
Environment=DISPLAY=:0

# Restart policy
#Restart=on-failure
#RestartSec=10
#StartLimitIntervalSec=500
#StartLimitBurst=5

[Install]
WantedBy=multi-user.target
EOL

    echo "Enabling and starting the service..."
    sudo systemctl daemon-reload
    sudo systemctl disable rfidsens.service
    sudo systemctl enable rfidsens.service
    sudo systemctl start rfidsens.service
else
    echo "Service file already exists. Restarting service..."
    sudo systemctl restart rfidsens.service
fi
