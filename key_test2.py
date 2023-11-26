import pygame, font

def show_android_keyboard():
	pygame.key.start_text_input()
	
def hide_android_keyboard():
	pygame.key.stop_text_input()

pygame.init()

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

e_keydown = None

clock = pygame.time.Clock()
running = True
while running:
	window.fill("black")
	
	if bool(e_keydown):
		window.blit(font.render("key: " + str(ord(e_keydown.text)), "white", 48), (0, 0))
		window.blit(font.render("unicode: " + str(e_keydown.text), "white", 48), (0, 58))
	else:
		window.blit(font.render("type a key to show its details", "white", 18), (0, 0))
		window.blit(font.render("click the screen to show the keyboard", "white", 18), (0, 20))
	
	pygame.display.flip()
	
	e = pygame.event.poll()
	if e.type == pygame.QUIT:
		running = False
	if e.type == pygame.MOUSEBUTTONDOWN:
		show_android_keyboard()
	if e.type == pygame.TEXTINPUT:
		e_keydown = e