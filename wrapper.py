import pygame
import time
from loadImage import loadImage
import font
from time import sleep
from threading import Thread

retryMax = 5

buildYear = 2023
version = 1
subversion = 0
devBuild = "1a"

devMode = True

mute = False
muteDebug = True

bsEvent = pygame.event.Event(
pygame.KEYDOWN, 
{
"unicode": "\b",
"key": pygame.K_BACKSPACE,
"mod": 0,
}
) 
eventQueue = []

if not devMode:
	import glox_startup_anim
	del glox_startup_anim

def keyget():
	eventQueue.append(bsEvent)
	#pass

def waitPress():
	while True:
		if pygame.event.poll().type == pygame.MOUSEBUTTONDOWN:
			break

errorCount = 1
exc = ""

while True:
	try:
		import main
		app = main.App(buildYear, version, subversion, devBuild, devMode, mute, muteDebug)
		while True:
			eventQueue = []
			t = Thread(target=keyget)
			if bool(eventQueue):
				print("EVENT QUEUE")
				print(eventQueue)
			app.main(eventQueue)
			del t
	except Exception as e:
		exception = e
		if str(e) == "Quit":
			break
			continue
	
	window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SRCALPHA)
	
	if errorCount > retryMax:
		window.blit(font.render("GLOX Quit with", "red", 32), (0, 0))
		window.blit(font.render("exception", "red", 32), (0, 50))
		window.blit(font.render(str(exception), "red", 10), (0, 100))
		window.blit(font.render("Click to quit...", "white", 32), (0, window.get_height() - 32))
		pygame.display.flip()
		waitPress()
		exit(1)
	
	if errorCount > retryMax - 1:
		window.blit(font.render("Last try!", "red", 32), (0, 200 + offset))
		exc = "!!!!" 
	window.blit(font.render("error:", "red", 32), (0, 0))
	
	#38.4
	window.blit(font.render(str(exception), "red", 10), (0, 50))
	offset = 50
	
	window.blit(font.render("retry: " + str(errorCount) + f" / {retryMax}" + exc, "red", 32), (0, 50 + offset))
	
	window.blit(font.render("GLOX Crashed!", "red", 32), (0, 100 + offset))
	window.blit(font.render("Restarting GLOX...", "white", 32), (0, 150 + offset))
	
	window.blit(font.render("Click to continue...", "white", 32), (0, window.get_height() - 32))
	
	pygame.display.flip() 
	waitPress()
	errorCount += 1