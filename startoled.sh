#!/bin/sh
# Routine to autostart the oled.
# To be placed in /etc/init.d

# This sleep is needed to the pi2, since network does not seem to be ready.
sleep 5
python /home/pi/minioled/OLEDip.py &
