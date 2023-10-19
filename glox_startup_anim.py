import pygame
import font
from loadImage import loadImage

pygame.init()

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA)

width, height = window.get_size()
wc, hc = width // 2, height // 2

size = 0
if width > height:
	size = height // 5
else:
	size = width // 5

gap = size // 5
totalW = gap * 3 + size * 4
gapLeft = (width - totalW) // 2

g = loadImage("icon.png", size)
l = font.render("L", "white", size)
o = loadImage("pause.png", size)
x = loadImage("cross.png", size + (size // 8))

g.set_alpha(0)
l.set_alpha(0)
o.set_alpha(0)
x.set_alpha(0)

speed = 12
tick = 0

clock = pygame.time.Clock()
running = True
while running:
	clock.tick(60)
	
	window.fill((0, 0, 0, 0))
	
	g.set_alpha(g.get_alpha() + speed)
	l.set_alpha(l.get_alpha() + speed) 
	o.set_alpha(o.get_alpha() + speed)
	x.set_alpha(x.get_alpha() + speed)
	
	window.blit(g, (gapLeft, hc - size // 2))
	window.blit(l, (gapLeft + gap + size, hc - size // 2))
	window.blit(o, (gapLeft + gap * 2 + size * 2, hc - size // 2))
	window.blit(x, (gapLeft + gap * 3 + size * 3 - (size // 8), hc - size // 2 - (size // 16)))
	
	if g.get_alpha() > 254 and tick >= 120:
		running = False
	if g.get_alpha() > 254:
		tick += 1
	
	pygame.display.flip()
	
	e = pygame.event.poll()
	if e.type == pygame.QUIT:
		running = False