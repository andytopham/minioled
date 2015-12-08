#!/usr/bin/python
# configinfo.py
# Designed to show hw and sw configuration at power on.
# This calls on info from guyc at py-gaugette on github and raspi.tv.
# GPIO docs are here...
# https://pypi.python.org/pypi/RPi.GPIO
# http://raspi.tv/2015/rpi-gpio-new-feature-gpio-rpi_info-replaces-gpio-rpi_revision

import time
import os
import sys
import socket
import fcntl
import struct
import argparse
#from RPi import GPIO
#print dir()
#print dir(GPIO)
#import RPi.GPIO as GPIO
import RPi.GPIO as GPIO
#? why is error for local variable if GPIO is the variable, but global name if tmp is name?

class Config_info():
	'''Print various information about the system we are running.'''
	def __init__(self, board = 'tft'):
		GPIO.setmode(GPIO.BCM)
		try:
			GPIO.RPI_INFO['TYPE']
			self.rpi = True
		except:
			self.rpi = False
		if board == 'uoled':
			print 'Board = uoled'
			import uoled
			self.myUoled = uoled.Screen()
		elif board == 'tft':
			print 'Board = tft'
			import tft
			self.myUoled = tft.Screen()			
		else:
			print 'Board = emulator'
			import uoled_emulator
			self.myUoled = uoled_emulator.Display()
			
	def get_ip_address(self, ifname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		if self.rpi == True:
			return socket.inet_ntoa(fcntl.ioctl(
				s.fileno(),
				0x8915,  # SIOCGIFADDR
				struct.pack('256s', ifname[:15])
			)[20:24])
		else:
			s.connect(("gmail.com",80))
			name = s.getsockname()
			s.close()
#			s.connect(('8.8.8.8', 80))
#			s.getsockname()[0]
#			s.close() 
#			for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
			return(name[0])

	def decode_ip_address(self):
		retstr = ''
		try:
			retstr = self.get_ip_address('wlan0')
		except IOError:
			try:
				retstr = self.get_ip_address('eth0')
			except IOError:
				retstr = ('No ip connection')
		return(retstr)

	def decode_rpi_revision(self, rev):
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
		if rev == '0010':
			return('Model B+ Revision 1.0 512MB')
		if rev == '0011':
			return('Compute module Revision 1.0 512MB')
		if rev == '0012':
			return('Model A+ Revision 1.0 256MB')
		if rev == '0013':
			return('Model B+ Revision 1.2 512MB')
		if rev == 'a01041':
			return('Pi2 Model B Revision 1.1 1GB (Sony)')
		if rev == 'a21041':
			return('Pi2 Model B Revision 1.1 1GB (China)')
		return('RPi revision unknown:'+rev+' ')

	def rpi_gpio_chk_function(self):
		retstr = ''
		pin=10
		func = GPIO.gpio_function(pin)
		if func == GPIO.SPI:
			retstr += 'SPI '
			pin=2
		func = GPIO.gpio_function(pin)
		if func == GPIO.I2C:
			retstr += 'I2C '
		pin=14
		func = GPIO.gpio_function(pin)
		if func == GPIO.SERIAL:
			retstr += 'Serial '
		pin=18
		func = GPIO.gpio_function(pin)
		if func == GPIO.HARD_PWM:
			retstr += 'PWM '
		return(retstr)

	def fetch_strings(self):
		no_of_rows, rowlength = self.myUoled.info()
		print 'Display rows ',no_of_rows, ' Length ', rowlength
		retstr = [' ' for i in range(no_of_rows)]
		retstr[0] = 'Name:' + os.uname()[1]
		retstr[1] = 'IP:' + self.decode_ip_address()
		if self.rpi == True:
			retstr[2] = 'RPi board rev:' + str(GPIO.RPI_INFO['P1_REVISION']) 
			retstr[3] = self.decode_rpi_revision(GPIO.RPI_INFO['REVISION'])[0:rowlength]
			if no_of_rows > 4:
				retstr[4] = self.decode_rpi_revision(GPIO.RPI_INFO['REVISION'])[rowlength:rowlength*2]
				retstr[5] = self.decode_rpi_revision(GPIO.RPI_INFO['REVISION'])[rowlength*2:rowlength*3]
				retstr[6] = GPIO.RPI_INFO['TYPE']			# only works well with rpi2.
		else:
			retstr[2] = 'No rpi board'
			retstr[3] = 'No rpi rev'
		retstr[no_of_rows-1] = time.strftime("%H:%M", time.gmtime())
		ifstring = self.rpi_gpio_chk_function()
		if no_of_rows > 4:
			retstr[8] = ('I/F: '+ifstring)[0:rowlength]
			retstr[9] = ('I/F: '+ifstring)[rowlength:rowlength*2]
			retstr[10] = ('I/F: '+ifstring)[rowlength*2:rowlength*3]
		self.print_strings(retstr, no_of_rows)
		return(retstr)
		
	def print_strings(self, strings, no_of_rows=4):
		for i in range(no_of_rows):
			print strings[i]
			self.myUoled.writerow(i,strings[i])
		self.myUoled.display()
		return(0)
		
if __name__ == "__main__":
	print 'Fetching system info'
	parser = argparse.ArgumentParser(description='configinfo')
	parser.add_argument("-H", "--HAT", help="select hat, default tft", action="store")
	args = parser.parse_args()
	if args.HAT:
		hat = 'uoled'
	else:
		hat = 'tft'
	# options for display are 'tft' or 'uoled'
	print 'HAT =', hat
	myConfiginfo = Config_info(hat)
	myConfiginfo.fetch_strings()
	