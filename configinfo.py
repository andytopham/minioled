#!/usr/bin/python
# configinfo.py
# Designed to show hw and sw configuration at power on.
# This calls on info from guyc at py-gaugette on github and raspi.tv.
# GPIO docs are here...
# https://pypi.python.org/pypi/RPi.GPIO
# http://raspi.tv/2015/rpi-gpio-new-feature-gpio-rpi_info-replaces-gpio-rpi_revision

import RPi.GPIO as GPIO
import time
import os
import sys
import socket
import fcntl
import struct
#from RPi import GPIO
print dir()

class Configinfo:
	'''Print various information about the system we are running.'''
	def __init__(self):
		''' Setup hardware and libraries.'''
#		print sys.platform		# need to use this to select whether rpi is true
		GPIO.setmode(GPIO.BCM)
		print GPIO.RPI_INFO['TYPE']
		try:
			GPIO.RPI_INFO['TYPE']
			self.rpi = True
			print 'Board is raspberry pi.'
		except:
			self.rpi = False
			print 'Board is NOT raspberry pi.'
		if self.rpi == True:
			from RPi import GPIO
			import uoled
			self.myUoled = uoled.uoled()	
		else:
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
			print name
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
		return('RPi revision unknown:'+rev+' ')

	def rpi_gpio_chk_function(self):
		retstr = ''
		pin=19
		GPIO.setmode(GPIO.BOARD)
		func = GPIO.gpio_function(pin)
		print func
		if func == GPIO.SPI:
			print 'SPI enabled'
			retstr += 'SPI '
		else:
			print 'Warning: SPI not enabled!'
		pin=3
		func = GPIO.gpio_function(pin)
		if func == GPIO.I2C:
			print 'I2C enabled'
			retstr += 'I2C '
		else:
			print 'Warning: I2C not enabled!'
		pin=8
		func = GPIO.gpio_function(pin)
		if func == GPIO.SERIAL:
			print 'Serial enabled'
			retstr += 'Serial '
		else:
			print 'Warning: Serial not enabled!'
		pin=12
		func = GPIO.gpio_function(pin)
		if func == GPIO.HARD_PWM:
			print 'PWM enabled'
			retstr += 'PWM '
		else:
			print 'Warning: PWM not enabled!'
		return(retstr)

	def fetch_strings(self):
		self.host_string = 'Hostname:' + os.uname()[1]
		self.ip = 'IP addr:' + self.decode_ip_address()
		if self.rpi == True:
			self.rpi_board = 'RPi board rev:' + str(GPIO.RPI_INFO['P1_REVISION']) + ' ' + self.gpio_func
			self.rpi_rev = self.decode_rpi_revision(GPIO.RPI_INFO['REVISION'])
			pi_type = GPIO.RPI_INFO['TYPE']			# only works well with rpi2.
		else:
			self.rpi_board = 'No rpi board'
			self.rpi_rev = 'No rpi rev'
		return(0)
		
	def print_strings(self):
#		print GPIO.RPI_INFO
#		gpio_func = self.rpi_gpio_chk_function()		# just prints pin function on console
#		print gpio_func
		# now put stuff on the remote display
		self.myUoled.writerow(1,self.host_string)
		self.myUoled.writerow(2,self.ip)
		self.myUoled.writerow(3,self.rpi_board)
		self.myUoled.writerow(4,self.rpi_rev)
		self.myUoled.display()
		return(0)
		
if __name__ == "__main__":
	print 'Fetching system info'
	myConfiginfo = Configinfo()
	myConfiginfo.fetch_strings()
	myConfiginfo.print_strings()
	time.sleep(5)
	