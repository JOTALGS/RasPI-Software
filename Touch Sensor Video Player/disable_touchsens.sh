#!/bin/bash

SERVICE_NAME="touchsens.service"

echo "Stopping and disabling $SERVICE_NAME..."
sudo systemctl stop $SERVICE_NAME
sudo systemctl disable $SERVICE_NAME
sudo systemctl status $SERVICE_NAME --no-pager