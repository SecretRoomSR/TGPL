# secretroom here
# WHAT U DOIN HERE >:((((
# GRRRRRRRRRRRRRRRRR

import pygame
import numpy
import threading
import random
from values import tileSize, start
import values
from Block import Block
from blockIds import blockIds, custom
from loadImage import loadImage, loadAnim, loadSheet
from notifications import notifications, notify, devNotify
try:
	from jnius import autoclass
except:
	pass
import platform
import font as fontP
from time import sleep
import keyMod

pygame.init()

devMode = True
devModeDebug = False
devBuild = "1a"

secretMode = False

buildYear = 2023
version = 1
subVersion = 0

mute = False
muteDebug = False
show_hitbox = True

values.mute = mute
values.muteDebug = muteDebug

secretModeCaptions = [
"how u get here?",
"suscibe https://youtube.com/@secretroomdev",
"suscibe https://youtube.com/@secretroomsr",
"made in a 2017 phone",
"check my github",
"glox glox glox glox glox glox",
"xolg xolg xolg xolg xolg xolg",
":)",
"Also try scratch!",
"Also try blockly!",
"import glox; glox.start()",
"wow, that was really cool"
]

# Version Name: GLOX - {buildYear}.{version}.{subVersion} ( - Dev Build {devBuild})

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

values.width = window.get_width()
values.height = window.get_height()

if devMode:
	pygame.display.set_caption(f"GLOX - {buildYear}.{version}.{subVersion}" + " - Dev Build " + devBuild)
elif secretMode:
	pygame.display.set_caption(f"cooler glox - {buildYear}.{version}.{subVersion} - " + secretModeCaptions[random.randrange(0, len(secretModeCaptions))])
else:
	pygame.display.set_caption(f"GLOX {buildYear}.{version}.{subVersion}")

print("[GLOX] Starting: " + pygame.display.get_caption()[0])

if mute:
	print("[Notification Debug] Notification Manager Muted >:X")
if muteDebug:
	print("[Notification Debug] Notification Debug Muted ÷X")

try:
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

# Dev

def threadDevNotify(type):
	if type == "options":
		devNotify(selected)
		sleep(0.3)
		devNotify(bool(selected))
		sleep(0.3)
		if bool(selected):
			devNotify((selected[2], selected[3]))
		else:
			devNotify((0, 0))
		sleep(0.3)
		devNotify(tileSize)
		sleep(0.3)
		try:
			devNotify((selected[0] // tileSize, selected[1] // tileSize))
		except:
			devNotify((0, 0))
		sleep(0.3)
		for i in blocks.keys():
			devNotify(i)
			sleep(0.3)
		devNotify(blocks[(selected[0] // tileSize, selected[1] // tileSize)].idObj.HasOptions) 

def devModeNotify(type):
	if devMode and devModeDebug:
		threading.Thread(target=threadDevNotify, args=(type,)).start()

font = pygame.font.SysFont("Arial", 48)

# loadImage("ui.png", size)
# loadImage("ui.png", 0, width, height)
ui = [
loadImage("popup.png").convert_alpha(), loadImage("eraser.png").convert(), loadImage("eraserOn.png").convert(), loadImage("rotate.png").convert(), loadImage("play.png").convert(), loadImage("pause.png").convert(),
loadImage("options.png").convert(),
loadImage("import.png").convert(),
loadImage("textInput.png", 0, tileSize * 4, tileSize).convert(),
loadImage("cross.png").convert_alpha(),
loadImage("select.png").convert(),
loadAnim("selectOn.png", 16, 16, tileSize, tileSize),
loadSheet("selectSheet2.png", 16, 16, tileSize, tileSize),
loadImage("selectMove.png").convert(),
loadImage("selectCopy.png").convert(),
loadImage("selectTrash.png").convert()
]

ui[12].get_image_from_size((tileSize * 4, tileSize * 3))

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
	global popup, deleteMode, blocks, rects, window, Block, popupRotate, blockRotate, tileSize, eraserX, id, dir, textInput, blockIds, openOption, openOptionBlock, select, selectStart, selected, crashing
	done = False
	
	if devMode:
		if pygame.Rect((0, window.get_height() - devLoad.get_height()), devLoad.get_size()).collidepoint(e.pos):
			crashing = True
			done = True
	
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
			for i in blocks.values():
				idObj = i.idObj
				if idObj.RunOnStart:
					idObj.function(i, idObj, blocks.values(), datas)
		else:
			for i in blocks.values():
				i.values = {}
		done = True
		
	if pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize * 6, tileSize, tileSize).collidepoint(e.pos) and popup:
		devModeNotify("options")
		if bool(selected) and (selected[2], selected[3]) == (tileSize, tileSize) and (selected[0] // tileSize, selected[1] // tileSize) in blocks.keys() and blocks[(selected[0] // tileSize, selected[1] // tileSize)].idObj.HasOptions:
			textInput = not textInput
		done = True
	
	if bool(selected) and (selected[2], selected[3]) == (tileSize, tileSize) and (selected[0] // tileSize, selected[1] // tileSize) in blocks.keys():
		selectedOptionBlock = blocks[(selected[0] // tileSize, selected[1] // tileSize)]
		for v, i in enumerate(selectedOptionBlock.options.keys()):
			if pygame.Rect(window.get_width() - tileSize * 5, window.get_height() - tileSize * (6 - v), tileSize * 4, tileSize).collidepoint(e.pos) and popup and textInput:
				show_android_keyboard()
				openOption = i
				openOptionBlock = (selected[0] // tileSize, selected[1] // tileSize)
				done = True
	
	if pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize * 7, tileSize, tileSize).collidepoint(e.pos) and popup:
		select = not select
		done = True
		
	collide = pygame.Rect(e.pos, (1, 1)).collidelist(rects)
	
	if textInput and not pygame.Rect(window.get_width() - tileSize * 5, window.get_height() - tileSize * 6, tileSize * 5, tileSize * len(selectedOptionBlock.options)).collidepoint(e.pos):
		hide_android_keyboard()
		openOption = None
		openOptionBlock = None
		done = True
	
	selectCollide = False
	if bool(selected):
		selectCollide = pygame.Rect(selected).collidepoint(e.pos) or pygame.Rect(selected[0], selected[1] + selected[3], tileSize * 3, tileSize).collidepoint(e.pos)
	
	if not done and bool(selected) and not selectCollide:
		selected = ()
		done = True
	
	if not done and not select and not selected:
		placePos = (int(numpy.floor(e.pos[0] // tileSize)), int(numpy.floor(e.pos[1] // tileSize))) 
		if not deleteMode and collide == -1:
			blocks[placePos] = Block(numpy.floor(e.pos[0] / tileSize) * tileSize, numpy.floor(e.pos[1] / tileSize) * tileSize, id, dir)
		if collide > -1 and deleteMode:
			del blocks[placePos]
			clear = True
		if not deleteMode and collide > -1:
			pass
	if select and not done and not selectCollide:
		selectStart = [numpy.floor(e.pos[0] / tileSize) * tileSize, numpy.floor(e.pos[1] / tileSize) * tileSize]

def draw_hitbox():
	global id, blockIds, popup, blocks, textInput
	for i in blocks.values():
		pygame.draw.rect(window, "green", pygame.Rect(i.x, i.y, tileSize, tileSize), tileSize // 16)
	pygame.draw.rect(window, "blue", pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize, tileSize, tileSize), tileSize // 16)
	if popup:
		for i in range(4):
			pygame.draw.rect(window, "blue", pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize * (i + 2), tileSize, tileSize), tileSize // 16)
		if bool(selected) and (selected[2], selected[3]) == (tileSize, tileSize) and (selected[0] // tileSize, selected[1] // tileSize) in blocks.keys() and blocks[(selected[0] // tileSize, selected[1] // tileSize)].idObj.HasOptions:
			pygame.draw.rect(window, "blue", pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize * 6, tileSize, tileSize), tileSize // 16)
			if textInput:
				for v, i in enumerate(blockIds[id].options):
					pos = (window.get_width() - tileSize * 5, window.get_height() - tileSize * (6 - v))
					pygame.draw.rect(window, "blue", pygame.Rect(pos, [tileSize * 4, tileSize]), tileSize // 16)
				pygame.draw.rect(window, "blue", pygame.Rect(window.get_width() - tileSize * 5, window.get_height() - tileSize * 6, tileSize * 4, tileSize), tileSize // 16)
		pygame.draw.rect(window, "blue", pygame.Rect(window.get_width() - tileSize, window.get_height() - tileSize * 7, tileSize, tileSize), tileSize // 16)

clock = pygame.time.Clock()

running = True
#blocks = []
blocks = {}
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
select = False
devLoad = pygame.transform.scale(loadImage("devMode.png", 256), (256, 64)).convert_alpha()
devLoad.set_colorkey((0, 0, 0))
selectStart = None
selected = ()

lastSize = (0, 0)
winSize = (0, 0)

openOption = None
openOptionBlock = None

tick = 0
second = 0
events = ()
eventQueue = None

crashing = False
crashTick = 0

bgFade = pygame.Surface(window.get_size(), pygame.SRCALPHA).convert_alpha()
bgFade.fill("black")

while running:
	if tick == 60:
		tick = 0
		second += 1
		ui[11].frame += 1
		ui[11].frame %= 4
	window.fill((47, 47, 47))
	
	if crashing:
		crashTick += 1
	
	if crashTick % 60 == 1:
		counter = 3 - int(numpy.floor(crashTick / 60))
		if counter == 0:
			class DevModeCrash(Exception):
				pass
			class Quit(Exception):
				pass
			raise DevModeCrash("Crashed")
		notify(f"Crashing in {counter}")
	
	winSize = window.get_size()
	
	if winSize != lastSize:
		threading.Thread(target=updateGrid).start()
	
	br %= 360
	rects = []
	for block in blocks.values():
		rects.append(pygame.Rect(block.x, block.y, tileSize, tileSize))
	xy = {}
	for block in blocks.values():
		xy[(block.x, block.y)] = block
	clock.tick(60)
	window.blit(grid, (0, 0))
	if values.start:
		for data in datas:
			bc = False
			for block in blocks.values():
				if data.collideBlock(block) and block.HasInput:
					bc = True
					break
			if not bc:
				datas.remove(data)
		for block in blocks.values():
			block.update(blocks, datas)
	elif len(datas) > 0:
		datas = []
	for block in blocks.values():
		window.blit(pygame.transform.rotate(block.idObj.imgFile, block.dir), (block.x, block.y))
	if not bool(datas):
		values.setStart(False)
	
	if selectStart:
		pos = pygame.mouse.get_pos()
		pos = [numpy.floor((pos[0] + tileSize) / tileSize) * tileSize, numpy.floor((pos[1] + tileSize) / tileSize) * tileSize]
		pX, pY = selectStart
		sX = pos[0] - selectStart[0]
		sY = pos[1] - selectStart[1]
		if sX < 0:
			pX += sX
			sX -= tileSize
		if sY < 0:
			pY += sY
			sY -= tileSize
		sX = int(abs(sX))
		sY = int(abs(sY))
		if sX == 0:
			sX = tileSize
		if sY == 0:
			sY = tileSize
		window.blit(ui[12].get_image_from_size((sX, sY)).convert_alpha(), (pX, pY))
	if bool(selected):
		window.blit(ui[12].get_image_from_size((selected[2], selected[3])).convert_alpha(), (selected[0::1]))
		window.blit(ui[13], (selected[0], selected[1] + selected[3]))
		window.blit(ui[14], (selected[0] + tileSize, selected[1] + selected[3]))
		window.blit(ui[15], (selected[0] + tileSize * 2, selected[1] + selected[3]))
	
	if bool(openOption):
		#window.blit(tSur, (0, 0))
		cEdit = fontP.render(f"Editing \"{openOption}\"", "white", 32).convert_alpha()
		window.blit(cEdit, (0, 58))
		pygame.draw.line(window, "white", (0, 100), (cEdit.get_width() + 30, 100), tileSize // 16)
	
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
	if bool(selected) and (selected[2], selected[3]) == (tileSize, tileSize) and (selected[0] // tileSize, selected[1] // tileSize) in blocks.keys() and blocks[(selected[0] // tileSize, selected[1] // tileSize)].idObj.HasOptions:
		if textInput:
			options = blocks[(selected[0] // tileSize, selected[1] // tileSize)].options
			for v, i in enumerate(options):
				pos = (window.get_width() - tileSize * 5, window.get_height() - tileSize * (6 - v))
				name = fontP.render(i, "white", tileSize // 2)
				value = pygame.Surface((0, 0))
				try:
					if type(options[i]) != custom:
						value = fontP.render(str(options[i]), (47, 47, 47), tileSize // 3)
					elif type(options[i]) == str:
						value = fontP.render(options[i], (47, 47, 47), tileSize // 3)
				except:
					pass
				window.blit(name, [pos[0] - name.get_width() - tileSize // 4, pos[1] + tileSize // 4])
				window.blit(ui[8], pos)
				window.blit(value, [pos[0] + tileSize // 2, pos[1] + tileSize // 8 * 2.5])
	else:
		window.blit(ui[9], (window.get_width() - ex, window.get_height() - tileSize * 6))
	
	if select:
		window.blit(ui[11].get_frame().convert(), (window.get_width() - ex, window.get_height() - tileSize * 7))
	else:
		window.blit(ui[10].convert(), (window.get_width() - ex, window.get_height() - tileSize * 7)) 
	
	if devMode:
		window.blit(devLoad, (0, window.get_height() - devLoad.get_height()))
	
	fps = int(clock.get_fps())
	#fpsRender = font.render("FPS: " + str(fps), (max(255 - min(fps / 60 * 255, 255), 0), min(fps / 60 * 255, 255), 0), (max(255 - min(fps / 60 * 255, 255), 0), min(fps / 60 * 255, 255), 0))
	fpsRender = fontP.render("FPS: " + str(fps), (max(255 - min(fps / 60 * 255, 255), 0), min(fps / 60 * 255, 255), 0), 48)
	window.blit(fpsRender, (0, 0))
	
	for i in notifications:
		window.blit(i[0], (i[1], i[2]))
		i[0].set_alpha(i[0].get_alpha() - 2)
		i[2] -= 2
		if i[0].get_alpha() == 0:
			notifications.remove(i)
	
	rects.append(pygame.Rect(window.get_width(), window.get_height() - tileSize * 3, 1, tileSize * 3))
	
	if bgFade:
		window.blit(bgFade, (0, 0))
		bgFade.set_alpha(bgFade.get_alpha() - 60)
		if bgFade.get_alpha() < 1:
			bgFade = False
	
	if show_hitbox:
		draw_hitbox()
	
	events = pygame.event.get()
	
	if bool(eventQueue):
		events.append(eventQueue)
	
	for e in events:
		if e.type == pygame.QUIT:
			if fps <= 10:
				print("[GLOX] Performance Issue Detected :O, if you think this isn't right or it insist, please report this problem in our issue tracker :)")
			print("\n[GLOX] === # Save Code # ===")
			saveCode = ""
			for i in blocks.values():
				# Save Format
				# id:x:y:dir;
				saveCode += f"{i.id}:{int(i.x // tileSize)}:{int(i.y // tileSize)}:{int(i.dir // 90)};"
			print("[GLOX] " + str(saveCode))
			print("[GLOX] ===================")
			print("\n[GLOX] Process exited")
			running = False
			raise Quit("Quit")
		if e.type == pygame.MOUSEBUTTONDOWN:
			mouseButtonDown(e)
		if e.type == pygame.KEYDOWN:
			try:
				if e.mod == 1:
					e.unicode = keyMod.mod_to_str(e.unicode)
				if bool(openOption) and len(str(e.key)) < 4:
					option = blocks[openOptionBlock].options[openOption]
					if isinstance(option, str):
						if e.unicode == "\b":
							blocks[openOptionBlock].options[openOption] = blocks[openOptionBlock].options[openOption][:-1]
						elif e.key == pygame.K_RETURN:
							openOption = None
							hide_android_keyboard()
						else:
							blocks[openOptionBlock].options[openOption] += e.unicode
							print(blocks[openOptionBlock].options)
					if isinstance(option, int) and e.unicode in "1234567890":
						blocks[openOptionBlock].options[openOption] = int(str(option) + e.unicode)
					print(f"[Options] {blocks[openOptionBlock]} [{openOption}] = {blocks[openOptionBlock].options[openOption]}")
			except:
				pass
		if e.type == pygame.MOUSEBUTTONUP:
			if bool(selectStart):
				selectStart = None 
				selected = (int(pX), int(pY), sX, sY)
			crashing = False
			crashTick = 0
	
	pygame.display.flip()
	lastSize = winSize
	tick += 1