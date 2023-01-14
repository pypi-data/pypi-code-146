import pygame as pg
from random import choice, randint

_red = [(8, 0, 0), (16, 0, 0), (32, 0, 0), (64, 0, 0), (128, 0, 0), (255, 0, 0), (255, 64, 0), (255, 128, 0), (255, 200, 0), (255, 255, 0)]
_blue = [(0, 0, 8), (0, 0, 16), (0, 0, 32), (0, 0, 64), (0, 0, 128), (0, 0, 255), (0, 64, 255), (0, 128, 255), (0, 200, 255), (0, 255, 255)]
_green = [(0, 8, 0), (0, 16, 0), (0, 32, 0), (0, 64, 0), (0, 128, 0), (0, 255, 0), (0, 255, 64), (0, 255, 128), (0, 255, 200), (0, 255, 255)]

class Flame:
	def __init__(self, size, pallete=_red, boxSize=8, randomSources=True, zeroOnIndexError=False, flipColors=False):
		self.scr = pg.Surface(size)
		self.pallete = pallete
		if(flipColors):
			self.pallete = self.pallete[::-1]
		self.boxSize = boxSize
		self.maxBoxes = int(size[0]/boxSize), int(size[1]/boxSize)
		self.screen = [[0 for _ in range(self.maxBoxes[1])] for _ in range(self.maxBoxes[0])]
		self.nums = [i+1 for i in range(10)]
		self.zeroOnIndexError = zeroOnIndexError
		self.randomSources = randomSources
		
	def _drawBox(self, x, y, color):
		x *= self.boxSize
		y *= self.boxSize
		pg.draw.rect(self.scr, color, (x, y, self.boxSize, self.boxSize))
		
	def _randomizeSources(self):
		for x in range(self.maxBoxes[0]):
			self.screen[x][-1] = choice(self.nums) if randint(1, 2) == 1 else 0

	def drawScreen(self):
		for x in range(self.maxBoxes[0]):
			for y in range(self.maxBoxes[1]):
				if(self.screen[x][y] != 0):
					self._drawBox(x, y, self.pallete[self.screen[x][y]-1])
				else:
					self._drawBox(x, y, (0, 0, 0))
	
	def updateScreen(self):
		for x in range(self.maxBoxes[0]):
			for y in range(self.maxBoxes[1]):
				try:
					if(self.screen[x][y] == self.screen[x][y+1]) and (self.screen[x][y] == self.screen[x][y+2]): self.screen[x][y] = 0
					else: self.screen[x][y] = round((self.screen[x-1][y+1]+self.screen[x][y+1]+self.screen[x+1][y+1]+self.screen[x][y])/4)
				except IndexError:
					if(self.zeroOnIndexError):
						self.screen[x][y] = 0
					
	def update(self):
		if(self.randomSources):
			self._randomizeSources()
		self.updateScreen()
		self.drawScreen()
