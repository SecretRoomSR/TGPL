import pygame
from values import tileSize

class Data:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def collideBlock(self, block):
		#return pygame.Rect(self.x, self.y, tileSize // 2, tileSize // 2).colliderect(pygame.Rect(block.x, block.y, tileSize, tileSize))
		return block.x == self.x - tileSize // 4 and block.y == self.y - tileSize // 4