#!/usr/bin/python
# Using forecastio for the weather forecast

import forecastio
import datetime
import forecastkey

api_key = forecastkey.key

#lat = -31.967819
#lng = 115.87718
# Stroud
lat = 51.727499
lng = -2.241022
current_time = datetime.datetime(2015, 11, 20, 9, 0, 0)
forecast = forecastio.load_forecast(api_key, lat, lng, time=current_time)
byHour = forecast.hourly()
print forecast.currently()
print byHour.summary

for hourly_data_point in byHour.data:
	print hourly_data_point

