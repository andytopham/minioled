#!/usr/bin/python
''' Fetch weather information from wunder.'''
import requests
from bs4 import BeautifulSoup
import urllib2
import json
import logging
import datetime

class Weather:
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		temperature = 0

	def gettemperature(self,bbckey):
		self.logger.debug("Fetching temperature")
		try:
			string = 'http://open.live.bbc.co.uk/weather/feeds/en/'+bbckey+'/observations.rss'
			soup = BeautifulSoup(requests.get(string).text)
		except HTTPError, e:
			self.logger.error('Failed to fetch temperature')
			temperature = 0
		except URLError, e:
			self.logger.error('Failed to reach temperature website')
			temperature = 1
		except:
			self.logger.error('Unknown error fetching temperature')
			temperature = 99	
		try:
			g = unicode(soup.item.description)
			found = re.search(": [0-9]*.*C",g)
			ggg = re.search("[0-9][0-9]|[0-9]",found.group())
			temperature=ggg.group()
			#this example shows how to get the temperatures from the forecast...
			#temperatures=[str(tem.contents[0]) for tem in table.find_all("span",class_="units-value temperature-value temperature-value-unit-c")]
		except:
			self.logger.error('Failed to convert temperature.')
			temperature=0
		self.logger.info('Temperature='+str(temperature))
		return(temperature)

	def wunder(self,key,locn):
		self.logger.debug("Fetching wunder temperature")
		f = urllib2.urlopen('http://api.wunderground.com/api/'+key+'/conditions/q/'+locn+'.json')
		json_string = f.read()
		parsed_json = json.loads(json_string)
		print parsed_json
		#location = parsed_json['location']['city']
		temp_c = parsed_json['current_observation']['temp_c']
		wind_mph = parsed_json['current_observation']['wind_mph']
		wind_dir = parsed_json['current_observation']['wind_dir']
		weathertype = parsed_json['current_observation']['weather']
		print 'wind',wind_mph
		print 'wind dir ',wind_dir
		print 'Weather:',weathertype
		self.logger.info("Current temperature is: %s" % (temp_c))
		f.close()
		return(str(temp_c),str(wind_mph),str(wind_dir),str(weathertype))
	
	def wunder_forecast(self,key,locn):
		self.logger.debug("Fetching wunder forecast temperature")
		f = urllib2.urlopen('http://api.wunderground.com/api/'+key+'/forecast/q/'+locn+'.json')
		json_string = f.read()
		parsed_json = json.loads(json_string)
#		print parsed_json
		#location = parsed_json['location']['city']
		days = parsed_json['forecast']['txt_forecast']['forecastday']
		print
		for day in days:
			print day['title'], ': ',day['fcttext_metric']

		f.close()
		return(0)
		
if __name__ == "__main__":
	logging.basicConfig(filename='log/weather.log',
						filemode='w',
						level=logging.WARNING)	#filemode means that we do not append anymore
#	Default level is warning, level=logging.INFO log lots, level=logging.DEBUG log everything
	logging.warning(datetime.datetime.now().strftime('%d %b %H:%M')+
					". Running weather class as a standalone app")

	print "Fetching weather info"
	myWeather = weather()
	myWeather.wunder()
	