# secretroom here
# WHAT U DOIN HERE >:((((60
# GRRRRRRRRRRRRRRRRR

import pygame
import numpy
import threading
import random
from values import tileSize, start
import values
from Block import Block
from blockIds import blockIds, custom
from loadImage import loadImage, loadAnim
from notifications import notifications, notify
from jnius import autoclass
import platform
import font as fontP

pygame.init()

devMode = True
secretMode = False
buildYear = 2023
version = 0
subVersion = 1
devBuild = "1a"

mute = False
muteDebug = False
show_hitbox = False

values.mute = mute
values.muteDebug = muteDebug

secretModeCaptions = [
"how u get here?",
"what da hail version",
"konami code ver",
"blocky scratch",
"total ripoff of scratch",
"snake ver",
"is dis e gaem?",
"cool secret mode",
"glox glox glox glox glox glox",
"xolg xolg xolg xolg xolg xolg",
";-;",
"UwU",
"OwO",
"import glox; glox.start()"
]

# Version Name: GLOX - {buildYear}.{version}.{subVersion} ( - Dev Build {devBuild})

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

values.width = window.get_width()
values.height = window.get_height()

if devMode:
	pygame.display.set_caption(f"GLOX - {buildYear}.{version}.{subVersion}" + " - Dev Build " + devBuild)
elif secretMode:
	pygame.display.set_caption("cooler glox - " + secretModeCap[random.randrange(0, len(secretModeCaptions) - 1)])
else:
	pygame.display.set_caption(f"GLOX {buildYear}.{version}.{subVersion}")

print("[GLOX] Starting: " + pygame.display.get_caption()[0])

if mute:
	print("[Notification Debug] Notification Manager Muted >:X")
if muteDebug:
	print("[Notification Debug] Notification Debug Muted ÷X")

PythonActivity = autoclass("org.kivy.android.PythonActivity")
InputMethodManager = autoclass("android.view.inputmethod.InputMethodManager")
Context = autoclass("android.content.Context")
activity = PythonActivity.mActivity
service = activity.getSystemService(Context.INPUT_METHOD_SERVICE)

def show_android_keyboard():
    global service
    service.toggleSoftInput(InputMethodManager.SHOW_FORCED, 0)
    
def hide_android_keyboard():
    global service
    service.hideSoftInputFromWindow(activity.getContentView().getWindowToken(), 0)

font = pygame.font.SysFont("Arial", 48)

# loadImage("ui.png", size)
# loadImage("ui.png", 0, width, height)
ui = [
loadImage("popup.png").convert_alpha(), loadImage("eraser.png").convert(), loadImage("eraserOn.png").convert(), loadImage("rotate.png").convert(), loadImage("play.png").convert(), loadImage("pause.png").convert(),
loadImage("options.png").convert(),
loadImage("import.png").convert(),
loadImage("textInput.png", 0, tileSize * 4, tileSize).convert(),
loadImage("cross.png").convert_alpha(),
loadAnim("selectOn.png", 16, 16, tileSize, tileSize)
]
popup = False

grid = window.copy()

def updateGrid():
	global grid, tileSize
	
	gridBuf = window.copy()
	
	gridBuf.fill((47, 47, 47))
	for x in range(gridBuf.get_width() // tileSize + 1):
		for i in range(tileSize // 8):
			pygame.draw.line(gridBuf, (66, 66, 66), (x * tileSize + i - tileSize // 16, 0), (x * tileSize + i - tileSize // 16, gridBuf.get_height()))
	for y in range(gridBuf.get_height() // tileSize + 1):
		for i in range(tileSize // 8):
			pygame.draw.line(gridBuf, (66, 66, 66), (0, y * tileSize + i - tileSize // 16), (gridBuf.get_width(), y * tileSize + i - tileSize // 16))
	for y in range(gridBuf.get_height() // tileSize + 1):
		for x in range(gridBuf.get_width() // tileSize + 1):
			pygame.draw.rect(gridBuf, (66, 66, 66), (tileSize // 16 + x * tileSize, tileSize // 16 + y * tileSize, tileSize // 16, tileSize // 16))
			pygame.draw.rect(gridBuf, (66, 66, 66), (tileSize // 16 + x * tileSize + (tileSize // 16 * 13), tileSize // 16 + y * tileSize, tileSize // 16, tileSize // 16))
			pygame.draw.rect(gridBuf, (66, 66, 66), (tileSize // 16 + x * tileSize, tileSize // 16 + y * tileSize + (tileSize // 16 * 13), tileSize // 16, tileSize // 16))
			pygame.draw.rect(gridBuf, (66, 66, 66), (tileSize // 16 + x * tileSize + (tileSize // 16 * 13), tileSize // 16 + y * tileSize + (tileSize // 16 * 13), tileSize // 16, tileSize // 16))
	gridBuf = gridBuf.convert()
	grid = gridBuf.copy()

updateGrid()

pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])

def mouseButtonDown(e):
	global popup, deleteMode, blocks, rects, window, Block, popupRotate, blockRotate, tileSize, eraserX, id, dir, textInput, blockIds, openOption
	done = False
	if pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize, tileSize, tileSize).collidepoint(e.pos):
		popupRotate += 180
		popupRotate %= 360
		eraserX -= tileSize
		if eraserX == -tileSize:
			eraserX = tileSize
		popup = not popup
		done = True
		
	if pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize * 2, tileSize, tileSize).collidepoint(e.pos) and popup:
		deleteMode = not deleteMode
		done = True
	
	if pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize * 3, tileSize, tileSize).collidepoint(e.pos) and popup:
		id += 1
		id %= len(blockIds)
		done = True
	if pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize * 4, tileSize, tileSize).collidepoint(e.pos) and popup:
		dir -= 90
		dir %= 360
		done = True
	
	if pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize * 5, tileSize, tileSize).collidepoint(e.pos) and popup:
		values.setStart(not values.start)
		if values.start:
			for i in blocks:
				idObj = i.idObj
				if idObj.RunOnStart:
					idObj.function(i, idObj, blocks, datas)
		else:
			for i in blocks:
				i.values = {}
		done = True
		
	if pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize * 6, tileSize, tileSize).collidepoint(e.pos) and popup and blockIds[id].HasOptions:
		textInput = not textInput
		done = True
	
	if pygame.Rect(window.get_width() - tileSize * 5, window.get_height() - tileSize * 6, tileSize * 4, tileSize).collidepoint(e.pos) and popup and textInput:
		show_android_keyboard()
		openOption = True
		done = True
		
	collide = pygame.Rect(e.pos, (1, 1)).collidelist(rects)
	
	if textInput and not pygame.Rect(window.get_width() - tileSize * 5, window.get_height() - tileSize * 6, tileSize * 5, tileSize).collidepoint(e.pos):
		textInput = False
		hide_android_keyboard()
		done = True
	
	if not done:
		if not deleteMode and collide == -1:
			blocks.append(Block(numpy.floor(e.pos[0] / tileSize) * tileSize, numpy.floor(e.pos[1] / tileSize) * tileSize, id, dir))
		if collide > -1 and deleteMode:
			blocks.remove(blocks[collide])
			clear = True
		if not deleteMode and collide > -1:
			pass

def draw_hitbox():
	global id, blockIds, popup, blocks, textInput
	for i in blocks:
		pygame.draw.rect(window, "green", pygame.Rect(i.x, i.y, tileSize, tileSize), tileSize // 16)
	pygame.draw.rect(window, "red", pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize, tileSize, tileSize), tileSize // 16)
	if popup:
		for i in range(4):
			pygame.draw.rect(window, "blue", pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize * (i + 2), tileSize, tileSize), tileSize // 16)
	if blockIds[id].HasOptions:
		pygame.draw.rect(window, "blue", pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize * 6, tileSize, tileSize), tileSize // 16)
		if textInput:
			for v, i in enumerate(blockIds[id].options):
				pos = (window.get_width() - tileSize * 5, window.get_height() - tileSize * (6 - v))
				pygame.draw.rect(window, "blue", pygame.Rect(pos, [tileSize * 4, tileSize]), tileSize // 16)
			pygame.draw.rect(window, "blue", pygame.Rect(window.get_width() - tileSize * 5, window.get_height() - tileSize * 6, tileSize * 4, tileSize), tileSize // 16)

clock = pygame.time.Clock()

running = True
blocks = []
datas = []
clear = True
deleteMode = False
textInput = False
dir = 0
rects = []
xy = {}
popupRotate = 180
pr = 180
blockRotate = 0
br = 0
eraserX = 0
ex = 0
id = 0
devLoad = pygame.transform.scale(loadImage("devMode.png", 256), (256, 64)).convert_alpha()
devLoad.set_colorkey((0, 0, 0))

lastSize = (0, 0)
winSize = (0, 0)

openOption = None

tick = 0
second = 0

while running:
	if tick == 60:
		tick = 0
		second += 1
		ui[10].frame += 1
		ui[10].frame %= 4
	window.fill((47, 47, 47))
	
	winSize = window.get_size()
	
	if winSize != lastSize:
		threading.Thread(target=updateGrid).start()
	
	br %= 360
	rects = []
	for block in blocks:
		rects.append(pygame.Rect(block.x, block.y, tileSize, tileSize))
	xy = {}
	for block in blocks:
		xy[(block.x, block.y)] = block
	clock.tick(60)
	window.blit(grid, (0, 0))
	if values.start:
		for data in datas:
			bc = False
			for block in blocks:
				if data.collideBlock(block) and block.HasInput:
					bc = True
					break
			if not bc:
				datas.remove(data)
		for block in blocks:
			block.update(blocks, datas)
	elif len(datas) > 0:
		datas = []
	for block in blocks:
		window.blit(pygame.transform.rotate(block.idObj.imgFile, block.dir), (block.x, block.y))
	if not bool(datas):
		values.setStart(False)
		
	if popupRotate > pr:
		pr += 20
	elif popupRotate < pr:
		pr -= 20
	
	if dir > br or dir < br:
		br -= 10
	
	if eraserX > ex:
		ex += tileSize / 8
	elif eraserX < ex:
		ex -= tileSize / 8
	window.blit(ui[2], (window.get_width() - ex, window.get_height() - tileSize * 2))
	
	idSurface = pygame.transform.rotate(blockIds[id].imgFile.convert_alpha(), br)
	idRect = idSurface.get_rect(center=(window.get_width() + tileSize / 2 - ex, window.get_height() - tileSize * 2.5))
	window.blit(idSurface, idRect)
	
	if deleteMode:
		window.blit(ui[2], (window.get_width() - ex, window.get_height() - tileSize * 2))
	else:
		window.blit(ui[1], (window.get_width() - ex, window.get_height() - tileSize * 2))
	popupSurface = pygame.transform.rotate(ui[0], pr)
	popupRect = popupSurface.get_rect(center=(window.get_width() - tileSize / 2, window.get_height() - tileSize / 2))
	window.blit(popupSurface, popupRect)
	
	window.blit(ui[3], (window.get_width() - ex, window.get_height() - tileSize * 4))
	
	if values.start:
		window.blit(ui[5], (window.get_width() - ex, window.get_height() - tileSize * 5))
	else:
		window.blit(ui[4], (window.get_width() - ex, window.get_height() - tileSize * 5))
	
	oPos = (window.get_width() - ex, window.get_height() - tileSize * 6) 
	window.blit(ui[6], oPos) 
	if blockIds[id].HasOptions:
		if textInput:
			options = blockIds[id].options
			for v, i in enumerate(options):
				pos = (window.get_width() - tileSize * 5, window.get_height() - tileSize * (6 - v))
				name = fontP.render(i, "white", tileSize // 2)
				value = pygame.Surface((0, 0))
				try:
					if type(options[i]) != custom:
						value = fontP.render(str(options[i]), (47, 47, 47), tileSize // 3)
				except:
					pass
				window.blit(name, [pos[0] - name.get_width() - tileSize // 4, pos[1] + tileSize // 4])
				window.blit(ui[8], pos)
				window.blit(value, [pos[0] + tileSize // 2, pos[1] + tileSize // 8 * 2.5])
	else:
		window.blit(ui[9], (window.get_width() - ex, window.get_height() - tileSize * 6))
	
	window.blit(ui[10].get_frame(), (window.get_width() - ex, window.get_height() - tileSize * 6))
	
	if devMode:
		window.blit(devLoad, (0, window.get_height() - devLoad.get_height()))
	
	fps = int(clock.get_fps())
	#fpsRender = font.render("FPS: " + str(fps), (max(255 - min(fps / 60 * 255, 255), 0), min(fps / 60 * 255, 255), 0), (max(255 - min(fps / 60 * 255, 255), 0), min(fps / 60 * 255, 255), 0))
	fpsRender = fontP.render("FPS: " + str(fps), "white", 48)
	window.blit(fpsRender, (0, 0))
	
	for i in notifications:
		window.blit(i[0], (i[1], i[2]))
		i[0].set_alpha(i[0].get_alpha() - 2)
		i[2] -= 2
		if i[0].get_alpha() == 0:
			notifications.remove(i)
	
	rects.append(pygame.Rect(window.get_width(), window.get_height() - tileSize * 3, 1, tileSize * 3))
	
	if show_hitbox:
		draw_hitbox()
	
	events = pygame.event.get()
	
	for e in events:
		if e.type == pygame.QUIT:
			if fps <= 10:
				print("[GLOX] Performance Issue Detected :O, if you think this isn't right or it insist, please report this problem in our issue tracker :)")
			print("\n[GLOX] === # Save Code # ===")
			saveCode = ""
			for i in blocks:
				# Save Format
				# id:x:y:dir;
				saveCode += f"{i.id}:{int(i.x // tileSize)}:{int(i.y // tileSize)}:{i.dir};"
			print("[GLOX] " + str(saveCode))
			print("[GLOX] ===================")
			print("\n[GLOX] Process exited")
			running = False
		if e.type == pygame.MOUSEBUTTONDOWN:
			mouseButtonDown(e)
		if e.type == pygame.KEYDOWN:
			pass
	pygame.display.flip()
	lastSize = winSize
	tick += 1