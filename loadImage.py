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

class __GLOXSheet:
	def __init__(self, im, s, outSize):
		self.im = im
		self.size = s
		if (im.get_width() % s[0] != 0) or (im.get_height() % s[1] != 0):
			raise ValueError("Image size cant be perfectly divided by the output size")
		self.outSize = outSize
		self.sheetSize = im.get_width() // s[0], im.get_height() // s[1]
		size = s[0]
		self.sep = [
		im.subsurface((size, size, size, size)),
		im.subsurface((0, 0, size, size)),
		im.subsurface((size * 2, 0, size, size)),
		im.subsurface((0, size * 2, size, size)),
		im.subsurface((size * 2, size * 2, size, size)),
		im.subsurface((size, 0, size, size)),
		im.subsurface((0, size, size, size)),
		im.subsurface((size * 2, size, size, size)),
		im.subsurface((size, size * 2, size, size)),
		im.subsurface((size * 3, 0, size, size)),
		im.subsurface((0, size * 3, size, size)),
		im.subsurface((size * 2, size * 3, size, size)),
		im.subsurface((size * 3, size * 2, size, size)),
		im.subsurface((size * 3, size, size, size)),
		im.subsurface((size, size * 3, size, size)),
		im.subsurface((size * 3, size * 3, size, size))
		]
	def get_image_from_size(self, size):
		sizeD = int(size[0] // self.outSize[0]), int(size[1] // self.outSize[1])
		# 0 = Center
		# 1 = Top Left
		# 2 = Top Right
		# 3 = Bottom Left
		# 4 = Bottom Right
		# 5 = Top
		# 6 = Left
		# 7 = Right
		# 8 = Bottom
		# 9 = Up Only
		# 10 = Left Only
		# 11 = Right Only
		# 12 = Bottom Only
		# 13 = Up Down
		# 14 = Left Right
		# 15 = Singular
		try:
			sheet = [[0] * sizeD[0]] * sizeD[1]
			sur = pygame.Surface(size, pygame.SRCALPHA)
			if size[0] == self.outSize[0] and size[1] == self.outSize[1]:
				sheet = [[15]]
			elif size[0] == self.outSize[0]:
				sheet = [[13]] * sizeD[1]
				sheet[0] = [9]
				sheet[-1] = [12]
			elif size[1] == self.outSize[1]:
				sheet[0] = [14] * sizeD[0]
				sheet[0][0] = 10
				sheet[0][-1] = 11
			else:
				sheet[0] = [5] * sizeD[0]
				sheet[-1] = [8] * sizeD[0]
				for i in sheet:
					i[0] = 6
					i[-1] = 7
				sheet[0][0] = 1
				sheet[0][-1] = 2
				sheet[-1][0] = 3
				sheet[-1][-1] = 4
			for v, i in enumerate(sheet):
				for y, x in enumerate(i):
					sur.blit(pygame.transform.scale(self.sep[x], self.outSize), (y * self.outSize[0], v * self.outSize[1]))
		except:
			pass
		return sur

def loadAnim(sheet, w=0, h=0, outW=0, outH=0):
	return __GLOXAnimation(pygame.image.load("./assets/textures/" + sheet), (w, h), (outW, outH))

def loadSheet(sheet, w=0, h=0, outW=0, outH=0):
	image = pygame.image.load("./assets/textures/" + sheet)
	return __GLOXSheet(image, (w, h), (outW, outH))