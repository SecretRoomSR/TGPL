import values
import font

notifications = []
def notify(string):
	if not values.mute:
		global notifications
		ren = font.render(str(string), "white", 32).convert_alpha()
		notifications.append([ren, 0, values.height - ren.get_height()])
		if not values.muteDebug:
			print("\n[Notification Manager] " + str(string))