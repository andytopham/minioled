#!/usr/bin/python
# uoled.py
# My routines for writing to the micro oled.
# This calls on info from guyc at py-gaugette on github and raspi.tv.
# GPIO docs are here...
# https://pypi.python.org/pypi/RPi.GPIO
# http://raspi.tv/2015/rpi-gpio-new-feature-gpio-rpi_info-replaces-gpio-rpi_revision

import gaugette.ssd1306
import time

# Setup which pins we are using to control the oled
RESET_PIN = 15
DC_PIN    = 16
# Using a 5x8 font
ROW_HEIGHT = 8
ROW_LENGTH = 20

class uoled:
	''' Class to control the micro oled based on the gaugette routines.'''
	def __init__(self):
		self.MySsd = gaugette.ssd1306.SSD1306(reset_pin=RESET_PIN, dc_pin=DC_PIN)
		self.MySsd.begin()
		self.MySsd.clear_display()
	
	def scroll_text(self,text):
		''' So far just scrolls the bottom row.'''
		x = 0
		y = ROW_HEIGHT * 3
		i = 0
		time.sleep(1)
		while i < len(text)-ROW_LENGTH:
			todraw = '{: <20}'.format(text[i:])
			self.MySsd.draw_text2(x,y,todraw,1)
			self.MySsd.display()
			i += 1
		time.sleep(1)
		return(0)
	
	def writerow(self,rownumber,string):
		self.MySsd.draw_text2(0,(rownumber-1)*ROW_HEIGHT,string,1)
		return(0)

	def display(self):
		self.MySsd.display()
		return(0)
		