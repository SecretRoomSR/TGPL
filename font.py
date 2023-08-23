import pygame
from loadImage import loadImage

pygame.init()

def read_sheet():
	d = {}
	with open("./assets/font/sheet") as sheet:
		for i in sheet.read().split("\n"):
			if i != "":
				key = i[0]
				val = i[2:].split(", ")
				valueX = int(val[0].replace("(", ""))
				valueY = int(val[1].replace(")", ""))
				if valueX == -5:
					valueX = 45
					valueY -= 5
				value = [valueX, valueY]
				d.update({key: value})
		return d

sheet = read_sheet()

def render(text, color, size):
	minoff = 0
	font = pygame.image.load("assets/font/font.png")
	sur = pygame.Surface((5 * len(text) + len(text) - 1, 5), pygame.SRCALPHA)
	color = pygame.Color(color)
	for v, i in enumerate(text):
		for x in range(5):
			for y in range(5):
				if i != " ":
					if i in sheet.keys():
						pos = sheet[i]
					else:
						pos = sheet["×"]
					if i in ["i", " "]:
						minoff = 2
					get = font.get_at((x + pos[0], y + pos[1]))
					if get[3] > 0:
						get = color
					sur.set_at((x + v * 5 + v - minoff, y), get)
	sur = pygame.transform.scale(sur, (size * len(text), size))
	return sur