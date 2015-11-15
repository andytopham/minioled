#!/usr/bin/python
# OLEDip.py
# This calls on info from guyc at py-gaugette on github and raspi.tv.
# GPIO docs are here...
# https://pypi.python.org/pypi/RPi.GPIO
# http://raspi.tv/2015/rpi-gpio-new-feature-gpio-rpi_info-replaces-gpio-rpi_revision

import gaugette.ssd1306
import time
import os
import sys
import socket
import fcntl
import struct
#import RPi.GPIO as GPIO
from RPi import GPIO

# Collect the info for the ip address
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

# Setup which pins we are using to control the oled
RESET_PIN = 15
DC_PIN    = 16
TEXT = ''

led = gaugette.ssd1306.SSD1306(reset_pin=RESET_PIN, dc_pin=DC_PIN)
led.begin()
led.clear_display()

# This sets TEXT equal to whatever your IP address is, or isn't
try:
    TEXT = get_ip_address('wlan0') # WiFi address of WiFi adapter. NOT ETHERNET
except IOError:
    try:
        TEXT = get_ip_address('eth0') # WiFi address of Ethernet cable. NOT ADAPTER
    except IOError:
        TEXT = ('NO INTERNET!')

# The actual printing of TEXT
led.clear_display()

hostname = os.uname()[1]
host_string = 'Hostname:'+hostname

rev = GPIO.RPI_INFO['P1_REVISION']
rpi_board = 'RPi board rev:'+str(rev)
pi_rev = GPIO.RPI_INFO['REVISION']
pi_type = GPIO.RPI_INFO['TYPE']
print 'RPi board revision: ',rev
rpi_rev = 'Other:'+str(pi_rev)+' '+str(pi_type)
ip = 'IP addr:'+TEXT

print GPIO.RPI_INFO


pin=19
GPIO.setmode(GPIO.BOARD)
func = GPIO.gpio_function(pin)
if func == GPIO.SPI:
	print 'SPI enabled'
else:
	print 'Warning: SPI not enabled!'


led.draw_text2(0,0,host_string,1)
led.draw_text2(0,8, ip, 1)
led.draw_text2(0,16,rpi_board,1)
led.draw_text2(0,24,rpi_rev,1)
led.display()
