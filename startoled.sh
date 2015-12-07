#!/bin/sh
# Routine to autostart the oled.
# To be placed in /etc/init.d

# This sleep is needed for the pi2, since network does not seem to be ready.
sleep 10
python /home/pi/master/minioled/configinfo.py &
