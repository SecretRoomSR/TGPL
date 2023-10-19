import values
import font

notifications = []
def notify(string):
	if not values.mute:
		global notifications
		ren = font.render(str(string), "white", 32)
		notifications.append([ren, 0, values.height - ren.get_height()])
		if not values.muteDebug:
			print("\n[Notification Manager] " + str(string))

def devNotify(string):
	global notifications
	ren = font.render(str(string), "blue", 32)
	notifications.append([ren, 0, values.height - ren.get_height()])
	if not values.muteDebug:
		print("\n[Debug Notification Manager] " + str(string))