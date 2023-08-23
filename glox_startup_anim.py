import pygame
from loadImage import loadImage

pygame.init()

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

width, height = window.get_size()

size = 0
if width > height:
	size = height // 2
else:
	size = width // 2

icon = loadImage("iconEmpty.png", size)
iconDone = loadImage("icon.png", size)

iconPos = (width // 2 - size // 2, height // 2 - size // 2)
mid = pygame.Surface((size // 8 * 3, size // 16), pygame.SRCALPHA)
mid.fill("white")
midSize = 0
midRot = -90
leftSize = 0
bottom = pygame.Surface((size // 8, size // 8 * 6), pygame.SRCALPHA)
bottom.fill("white")
bottomRot = 0
bottomY = 0
rightBigSize = 0
rightSize = 0
topSize = 0

done = False

clock = pygame.time.Clock()
running = True
while running:
	window.fill("black")
	
	window.blit(icon, iconPos)
	
	if not done:
		if midSize >= size // 8 * 3:
			if midRot != 0:
				midRot += 5
		else:
			midSize += size // 64
		if leftSize >= size // 8 * 6:
			leftSize = size // 8 * 6
			window.blit(pygame.transform.rotate(bottom, bottomRot), (iconPos[0] + size // 8, iconPos[1] + size // 8 + bottomY))
			if bottomRot != -90:
				bottomRot -= 5
				bottomY += size / 8 * 6 / 22
			else:
				bottomY = size / 8 * 5
				if rightBigSize < size // 8 * 3:
					rightBigSize += size // 48
				else:
					rightBigSize = size // 8 * 3
					done = True
				if rightSize < size // 8 * 2.5:
					rightSize += size // 48
				else:
					rightSize = size // 8 * 2.5
			if topSize < size // 8 * 6:
				topSize += size / 32
		else:
			leftSize += size // 32
	
	clock.tick(60)
	
	if not done:
		# Right
		pygame.draw.rect(window, "white", pygame.Rect(iconPos[0] + size // 8 * 6, iconPos[1] + size // 8 * 3.5 - rightSize, size // 8, rightSize))
		pygame.draw.rect(window, "white", pygame.Rect(iconPos[0] + size // 8 * 6, iconPos[1] + size // 8 * 4, size // 8, rightBigSize))
	
		# Left
		pygame.draw.rect(window, "white", pygame.Rect(iconPos[0] + size // 8, iconPos[1] + size // 8, size // 8, leftSize))
	
		# Top And Bottom
		pygame.draw.rect(window, "white", pygame.Rect(iconPos[0] + size // 8, iconPos[1] + size // 8, topSize, size // 8))
	
		# Middle
		if midSize >= size // 8 * 3:
			window.blit(pygame.transform.rotate(mid, midRot), (iconPos[0] + size // 2, iconPos[1] + size // 8 * 4))
		else:
			pygame.draw.rect(window, "white", pygame.Rect(iconPos[0] + size // 2, iconPos[1] + size // 8 * 4, size // 16, midSize))
	else:
		window.blit(iconDone, iconPos)
	
	pygame.display.flip()
	
	e = pygame.event.poll()
	if e.type == pygame.QUIT:
		running = False