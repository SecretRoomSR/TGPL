import pygame, font

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

toCheck = "@#$&_-()=%\"*':/!?+~[]{}<>^`;\|"

keys = {}
for i in toCheck:
	keys.update({i:""})

currentKey = 0

clock = pygame.time.Clock()
running = True
while running:
	window.fill("black")
	
	window.blit(font.render(list(keys.keys())[currentKey], "white", 36), (0, 0))
	
	pygame.display.flip()
	
	e = pygame.event.poll()
	if e.type == pygame.QUIT:
		running = False
		print(keys)
	if e.type == pygame.KEYDOWN:
		if currentKey < len(toCheck) and len(str(e.key)) < 4:
			keys[toCheck[currentKey]] = e.unicode
			currentKey += 1
			if currentKey >= len(toCheck):
				with open("./assets/mod/modDict", "w") as file:
					for i in keys.keys():
						if i != keys[i]:
							file.write(f"{i}: {keys[i]}\n")
				break
	if e.type == pygame.MOUSEBUTTONDOWN:
		show_android_keyboard()