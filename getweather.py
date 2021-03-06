#!/usr/bin/python
# getweather.py
# Designed to show weather on uoled.
# This calls on info from guyc at py-gaugette on github and raspi.tv.
# GPIO docs are here...
# https://pypi.python.org/pypi/RPi.GPIO
# http://raspi.tv/2015/rpi-gpio-new-feature-gpio-rpi_info-replaces-gpio-rpi_revision

import time
import os
import weather
import constants

RPi = False

if RPi == True:
	import uoled
	MyUoled = uoled.uoled()	
else:
	import uoled_emulator
	MyUoled = uoled_emulator.Uoled_Emulator()
	
MyWeather = weather.Weather()

print 'Fetching weather info'
MyUoled.writerow(1,'Weather for '+constants.locn)
temp,wind,winddir,obs = MyWeather.wunder(constants.key,constants.locn)
print 'Results',temp, wind, winddir, obs	
MyUoled.writerow(2,'Temperature:'+temp+' C')
MyUoled.writerow(3,'Wind:'+wind+'mph. Dirn:'+winddir)
MyUoled.writerow(4,'Observation:'+obs)
MyUoled.display()
#MyUoled.scroll_text(2,'Temperature:'+temp+' C'+' Wind:'+wind+' Dirn:'+winddir+' Observation:'+obs)
#MyUoled.display()
MyWeather.wunder_forecast(constants.key,constants.locn)

time.sleep(25)
