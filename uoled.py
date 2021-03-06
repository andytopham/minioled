#!/usr/bin/python
# uoled.py
# My routines for writing to the micro oled.
# This calls on info from guyc at py-gaugette on github and raspi.tv.
# GPIO docs are here...
# https://pypi.python.org/pypi/RPi.GPIO
# http://raspi.tv/2015/rpi-gpio-new-feature-gpio-rpi_info-replaces-gpio-rpi_revision
# gaugette updates: https://github.com/guyc/py-gaugette

import gaugette.gpio
import gaugette.ssd1306
import time

# Setup which pins we are using to control the oled - these are wiring pi numbers.
# RESET_PIN = 15
# DC_PIN    = 16
# Now do it properly with real raspberry pi numbers
RESET_PIN = 14
DC_PIN    = 15
# Using a 5x8 font
ROW_HEIGHT = 8
ROW_LENGTH = 20
NO_OF_ROWS = 4


class Screen:
	''' Class to control the micro oled based on the gaugette routines.
		The row numbering starts at 1.
		Calling writerow does not display anything. Also need to call display.
		'''
	def __init__(self):
		gpio = gaugette.gpio.GPIO()
		spi = gsugette.spi.SPI(bus=0, device=0)
		self.MySsd = gaugette.ssd1306.SSD1306(gpio, spi, reset_pin=RESET_PIN, dc_pin=DC_PIN)
		self.MySsd.begin()
		self.MySsd.clear_display()
	
	def scroll_text(self,rownumber,text):
		''' So far just scrolls one row.'''
#		print 'Scrolling row number ',rownumber
		x = 0
		y = ROW_HEIGHT * rownumber-1
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
		self.MySsd.draw_text2(0,(rownumber)*ROW_HEIGHT,string,1)
		return(0)

	def draw_blob(self,x,y):
		self.MySsd.draw_pixel(x,y,True)
#		self.MySsd.draw_pixel(x+1,y,True)
#		self.MySsd.draw_pixel(x,y+1,True)
#		self.MySsd.draw_pixel(x+1,y+1,True)
		return(0)
		
	def delete_blob(self,x,y):
		self.MySsd.draw_pixel(x,y,False)
#		self.MySsd.draw_pixel(x+1,y,True)
#		self.MySsd.draw_pixel(x,y+1,True)
#		self.MySsd.draw_pixel(x+1,y+1,True)
		return(0)
		
	def display(self):
		self.MySsd.display()
		return(0)
	
	def test(self):
		self.writerow(1,'Test')
		self.display()
		return(0)
		
	def info(self):
		return(NO_OF_ROWS, ROW_LENGTH)
		
if __name__ == "__main__":
	print 'Uoled test'		
	MyScreen = Screen()
	MyScreen.test()