#!/usr/bin/python
# bounce.py
# Very simple implementation of bouncing ball.

import time

RPi = True
if RPi == True:
	import uoled
	MyUoled = uoled.uoled()	
else:
	import uoled_emulator
	MyUoled = uoled_emulator.Uoled_Emulator()

print 'Starting bounce...'

x = 0
y = 0
maxx = 128
maxy = 32
minx = 0
miny = 0
movx = 1
movy = 1

while True:
	MyUoled.delete_blob(x,y)
	x += movx
	y += movy
	if x >= maxx:
		movx = -1
	if y >= maxy:
		movy = -1
	if x <= minx:
		movx = 1
	if y <= miny:
		movy = 1
#	print x,y
	MyUoled.draw_blob(x,y)
	MyUoled.display()
#	time.sleep(.1)
