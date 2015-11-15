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

def decode_ip_address():
	retstr = ''
	try:
		retstr = get_ip_address('wlan0') # WiFi address of WiFi adapter. NOT ETHERNET
	except IOError:
		try:
			retstr = get_ip_address('eth0') # WiFi address of Ethernet cable. NOT ADAPTER
		except IOError:
			retstr = ('No ip connection')
	return(retstr)

def decode_rpi_revision(rev):
	if rev == '0002':
		return('Model B Revision 1.0')
	if rev == '0003':
		return('Model B Revision 1.0 + Fuses mod and D14 removed')
	if rev == '0004':
		return('Model B Revision 2.0 256MB')
	if rev == '0005':
		return('Model B Revision 2.0 256MB')
	if rev == '0006':
		return('Model B Revision 2.0 256MB')
	if rev == '0007':
		return('Model A Revision 2.0 256MB')
	if rev == '0008':
		return('Model A Revision 2.0 256MB')
	if rev == '0009':
		return('Model A Revision 2.0 256MB')
	if rev == '000d':
		return('Model B Revision 2.0 512MB')
	if rev == '000e':
		return('Model B Revision 2.0 512MB')
	if rev == '000f':
		return('Model B Revision 2.0 512MB')
	return('unknown')

def rpi_gpio_chk_function():
	pin=19
	GPIO.setmode(GPIO.BOARD)
	func = GPIO.gpio_function(pin)
	if func == GPIO.SPI:
		print 'SPI enabled'
	else:
		print 'Warning: SPI not enabled!'
	return(0)

# Setup which pins we are using to control the oled
RESET_PIN = 15
DC_PIN    = 16

oled = gaugette.ssd1306.SSD1306(reset_pin=RESET_PIN, dc_pin=DC_PIN)
oled.begin()
oled.clear_display()

ip_info = decode_ip_address()

oled.clear_display()

hostname = os.uname()[1]
host_string = 'Hostname:'+hostname

rev = GPIO.RPI_INFO['P1_REVISION']
rpi_board = 'RPi board rev:'+str(rev)
pi_rev = GPIO.RPI_INFO['REVISION']
rpi_rev = decode_rpi_revision(pi_rev)
pi_type = GPIO.RPI_INFO['TYPE']			# only works well with rpi2.
print 'RPi board revision: ',rev
# rpi_rev = 'Other:'+str(pi_rev)+' '+str(pi_type)
ip = 'IP addr:'+ip_info

print GPIO.RPI_INFO

rpi_gpio_chk_function()		# just prints pin funtion on console

oled.draw_text2(0,0,host_string,1)
oled.draw_text2(0,8, ip, 1)
oled.draw_text2(0,16,rpi_board,1)
oled.draw_text2(0,24,rpi_rev,1)
oled.display()

if len(rpi_rev) > 20:
	i = 0
	while i < len(rpi_rev)-19:
		time.sleep(.3)
		oled.draw_text2(i,24,'                    ',1)
		time.sleep(.1)
		oled.draw_text2(i,24,rpi_rev[i:20+i],1)
		time.sleep(.2)
		oled.display()
		i += 1
time.sleep(2)
oled.draw_text2(i,24,'                    ',1)	# clear off old text
oled.draw_text2(0,24,rpi_rev,1)
time.sleep(.2)
oled.display()

# end
	