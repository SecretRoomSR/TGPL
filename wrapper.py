#pygame.event.Event(
#pygame.KEYDOWN, 
#{
#"unicode": "\b",
#"key": pygame.K_BACKSPACE,
#"mod": 0,
#}
#)
#
# BACKSPACE FIX

import pygame, time
from loadImage import loadImage
import font
from time import sleep

import glox_startup_anim
del glox_startup_anim

while True:
	try:
		import main
	except Exception as e:
		if str(e) == "Quit":
			break
			continue
	
	window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SRCALPHA)
	
	sleep(1)
	window.blit(font.render("GLOX Crashed!", "red", 32), (0, 0))
	pygame.display.flip()
	sleep(2)
	window.blit(font.render("Restarting GLOX...", "white", 32), (0, 50))
	pygame.display.flip()
	sleep(3)
	window.blit(font.render("Restoring Save...", "white", 32), (0, 100))
	pygame.display.flip()
	sleep(4)
	window.fill("black")
	window.blit(font.render("Finished!", "green", 32), (0, 0))
	pygame.display.flip()
	sleep(1)