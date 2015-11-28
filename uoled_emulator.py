#!/usr/bin/python
# uoled_emulator.py

import os
import pygame
from pygame.locals import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)
BLACK = (0, 0, 0)
ROWHEIGHT = 20

class Screen():

	def __init__(self):
		x = 20
		y = 300
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
		pygame.init()
		pygame.display.set_mode((220, 80))
		pygame.display.set_caption('uoled emulator')
		self.screen = pygame.display.get_surface()
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill(BLACK)

	def writerow(self, rownumber, string):
		ypos = ROWHEIGHT / 2 + (rownumber - 1) * ROWHEIGHT
		font = pygame.font.Font(None, 24)
		text = font.render(string, 1, WHITE)
		textpos = text.get_rect(centery = ypos)
		self.background.blit(text, textpos)
		self.screen.blit(self.background, (0, 0))

	def display(self):
		pygame.display.flip()
		return(0)
		