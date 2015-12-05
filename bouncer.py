#!/usr/bin/python
# game.py
# Very simple game.
# A useful guide to using objects here....
# http://openbookproject.net/thinkcs/python/english3e/classes_and_objects_I.html
import time


class Bouncer:
	def __init__(self):
		rpi = 'tft'
		if rpi == 'tft':
			import tft
			self.myUoled = tft.Screen()
		elif rpi == 'uoled':
			import uoled
			self.myUoled = uoled.uoled()	
		else:		# linux console
			import uoled_emulator
			self.myUoled = uoled_emulator.Uoled_Emulator()
		x = 0
		y = 0
		self.maxx = 128
		self.maxy = 32
		self.minx = 0
		self.miny = 0
		self.movx = 1
		self.movy = 1

		self.obs = [[[20,20],[20,21],[21,20],[21,21],[22,20],[22,21]], 
				[[80,28],[80,29],[80,30],[80,31]],
				[[60,5],[60,6],[60,7],[60,8]]]
#		self.myUoled.draw_sprite(self.obs)
		self.main_loop(x,y)
		
	def crashed(self, x, y):
		for s in self.obs:
			for t in s:
				if (x in t) and (y in t):
					return(True)
		return(False)

	def main_loop(self, x, y):
		while True:
			self.myUoled.delete_blob(x,y)
			x += self.movx
			y += self.movy
			if x >= self.maxx:
				self.movx = -1
			if y >= self.maxy:
				self.movy = -1
			if x <= self.minx:
				self.movx = 1
			if y <= self.miny:
				self.movy = 1
			self.myUoled.draw_blob(x,y)
			if self.crashed(x, y):			# this needs improving to allow y bouncing
				self.movx = -self.movx
				self.myUoled.draw_sprite(self.obs)
			self.myUoled.display()
		
class Pt:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

class Block:
	def __init__(self, x=0, y=0):
		P = Pt()
		shape = [P(10,10), P(10,11)]
		
	def is_in(self, Q):
		if Q in shape:
			return(True)
		return(False)
		
	
if __name__ == "__main__":
	print 'Game in progress...'
	myGame = Bouncer()
	