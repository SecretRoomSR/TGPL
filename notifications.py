import pygame
import values
import font

pygame.font.init()

notifications = []
def notify(string):
	if not values.mute:
		global notifications
		ren = font.render(string, "white", 48)
		notifications.append([ren, 0, values.height - ren.get_height()])
		if not values.muteDebug:
			print("\n[Notification Manager] " + string)