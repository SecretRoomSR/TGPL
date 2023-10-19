import pygame, font
from notifications import notify, notifications

try:
	from jnius import autoclass
	PythonActivity = autoclass("org.kivy.android.PythonActivity")
	InputMethodManager = autoclass("android.view.inputmethod.InputMethodManager")
	Context = autoclass("android.content.Context")
	activity = PythonActivity.mActivity
	service = activity.getSystemService(Context.INPUT_METHOD_SERVICE)
except:
	pass

def show_android_keyboard():
	try:
		global service
		service.toggleSoftInput(InputMethodManager.SHOW_FORCED, 0)
	except:
		pass
	
def hide_android_keyboard():
	try:
		global service
		service.hideSoftInputFromWindow(activity.getContentView().getWindowToken(), 0)
	except:
		pass

pygame.init()

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

e_keydown = None

clock = pygame.time.Clock()
running = True
while running:
	window.fill("black")
	
	if bool(e_keydown):
		window.blit(font.render("key: " + str(e_keydown.key), "white", 48), (0, 0))
		window.blit(font.render("unicode: " + str(e_keydown.unicode), "white", 48), (0, 58))
		window.blit(font.render("mod: " + str(e_keydown.mod), "white", 48), (0, 116))
	else:
		window.blit(font.render("type a key to show its details", "white", 18), (0, 0))
		window.blit(font.render("click the screen to show the keyboard", "white", 18), (0, 20))
	
	for i in notifications:
		window.blit(i[0], (i[1], i[2]))
		i[0].set_alpha(i[0].get_alpha() - 2)
		i[2] -= 2
		if i[0].get_alpha() == 0:
			notifications.remove(i) 
	
	pygame.display.flip()
	
	e = pygame.event.poll()
	if e.type == pygame.QUIT:
		running = False
	if e.type == pygame.MOUSEBUTTONDOWN:
		show_android_keyboard()
	if e.type == pygame.KEYDOWN:
		e_keydown = e
		notify("tap")