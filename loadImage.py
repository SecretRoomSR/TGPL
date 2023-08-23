import pygame
from values import tileSize

def loadImage(texture, size=tileSize, w=0, h=0):
	if w == 0:
		w = size
	if h == 0:
		h = size
	return pygame.transform.scale(pygame.image.load("./assets/textures/" + texture), (w, h))

class __GLOXAnimation:
	def __init__(self, im, size, outSize):
		self.im = im
		self.size = size
		self.outSize = outSize
		self.frame = 0
	def get_frame(self):
		frame = round(self.frame)
		rect = ((0, frame * self.size[1]), self.size)
		subsurface = self.im.subsurface((0, frame * self.size[0], self.size[0], self.size[1]))
		return pygame.transform.scale(subsurface, self.outSize)

def loadAnim(sheet, w=0, h=0, outW=0, outH=0):
	return __GLOXAnimation(pygame.image.load("./assets/textures/" + sheet), (w, h), (outW, outH))