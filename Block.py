import pygame
import copy
from blockIds import blockIds
from values import tileSize

class Block:
	global window
	def __init__(self, x, y, id, dir):
		self.x = x
		self.y = y
		self.dir = dir
		self.id = id
		self.HasInput = blockIds[id].HasInput
		self.idObj = blockIds[id]
		self.options = copy.deepcopy(self.idObj.options)
		self.values = {}
	def update(self, blocks, datas):
		if self.idObj.function and self.idObj.UpdateEveryFrame:
			self.idObj.function(self, self.idObj, blocks, datas)
	def __repr__(self):
		return f"[{self.idObj.name}, {self.x / tileSize}, {self.y / tileSize}]"