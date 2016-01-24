#!/bin/bash
# written by Wil Black wilblack21@gmail.com Jan. 24, 2015


cd  /home/pi/projects/rpi-bike-odometer
#sudo chmod 755 RPi_Server_Code.py

NOW=$(date +"%Y-%m-%dT%T %Z")
echo "[$NOW] Starting and ardyh client"

modprobe i2c-bcm2708
modprobe i2c-dev

python server.py