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
from RPi import GPIO
import uoled
import tft

LOGFILE = 'log/configinfo.log'
	
class Sysinfo():
	def __init__(self):
		uoled = False
		if uoled == True:
			self.MyUoled = uoled.uoled()	
		else:
			self.MyUoled = tft.Tft()
		self.collect_info()
		
		
	def get_ip_address(self, ifname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(
			s.fileno(),
			0x8915,  # SIOCGIFADDR
			struct.pack('256s', ifname[:15])
		)[20:24])

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
	#	pin=19		# board number
		pin=10		# gpio number
	#	GPIO.setmode(GPIO.BOARD)
		func = GPIO.gpio_function(pin)
		print func
		if func == GPIO.SPI:
			print 'SPI enabled'
			retstr += 'SPI '
		else:
			print 'Warning: SPI not enabled!'
	#	pin=3		# board number
		pin=2		# bcm number
		func = GPIO.gpio_function(pin)
		if func == GPIO.I2C:
			print 'I2C enabled'
			retstr += 'I2C '
		else:
			print 'Warning: I2C not enabled!'
		pin=8		# board number
		pin = 14		# bcm number
		func = GPIO.gpio_function(pin)
		if func == GPIO.SERIAL:
			print 'Serial enabled'
			retstr += 'Serial '
		else:
			print 'Warning: Serial not enabled!'
		pin=12		# board number
		pin = 18		# bcm number
		func = GPIO.gpio_function(pin)
		if func == GPIO.HARD_PWM:
			print 'PWM enabled'
			retstr += 'PWM '
		else:
			print 'Warning: PWM not enabled!'
		return(retstr)

	def collect_info(self):
		ip_string = '{:<30}'.format('IP addr:'+self.decode_ip_address())
		host_string = '{:<30}'.format('Hostname:'+os.uname()[1])
		rpi_board = '{:<30}'.format('RPi board rev:'+str(GPIO.RPI_INFO['P1_REVISION']))
		rpi_rev = self.decode_rpi_revision(GPIO.RPI_INFO['REVISION'])
		pi_type = GPIO.RPI_INFO['TYPE']			# only works well with rpi2.

		print GPIO.RPI_INFO
		gpio_func = self.rpi_gpio_chk_function()		# just prints pin function on console
		print gpio_func

		self.MyUoled.writerow(1,host_string)
		self.MyUoled.writerow(2,ip_string)
		self.MyUoled.writerow(3,rpi_board+' '+gpio_func)
		self.MyUoled.writerow(4,rpi_rev)
		self.MyUoled.display()
		return(0)

if __name__ == "__main__":
	print 'Config Info'
	myConfig = Sysinfo()
		
