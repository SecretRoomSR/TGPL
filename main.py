# secretroom here
# WHAT U DOIN HERE >:((((
# GRRRRRRRRRRRRRRRRR

import pygame
try:
	import numpy
except:
	import math as numpy
import threading
import random
from values import tileSize, start
import values
from Block import Block
from blockIds import blockIds, custom
from loadImage import loadImage, loadAnim, loadSheet
from notifications import notifications, notify
import platform
import font as fontP
from time import sleep
import keyMod

class App:
	def __init__(self, buildYear, version, subversion, devBuild, devMode, mute=False, muteDebug=False):
		pygame.init()
		
		self.devMode = devMode
		self.devBuild = devBuild
		
		self.secretMode = False
		
		self.buildYear = buildYear
		self.version = version
		self.subVersion = subversion
		
		values.mute = mute
		values.muteDebug = muteDebug
		
		self.secretModeCaptions = [
		"how u get here?",
		"glox glox glox glox glox glox",
		"xolg xolg xolg xolg xolg xolg",
		":)",
		"wow, that was really cool"
		]
		
		# Version Name: GLOX - {buildYear}.{version}.{subVersion} ( - Dev Build {devBuild})
		
		self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
		
		values.width = self.window.get_width()
		values.height = self.window.get_height()
		
		if self.devMode:
			pygame.display.set_caption(f"GLOX - {self.buildYear}.{self.version}.{self.subVersion}" + " - Dev Build " + self.devBuild)
		elif self.secretMode:
			pygame.display.set_caption(f"cooler glox - {self.buildYear}.{self.version}.{self.subVersion} - " + self.secretModeCaptions[random.randrange(0, len(self.secretModeCaptions))])
		else:
			pygame.display.set_caption(f"GLOX {self.buildYear}.{self.version}.{self.subVersion}")
		
		print("[GLOX] Starting: " + pygame.display.get_caption()[0])
		
		if mute:
			print("[Notification Debug] Notification Manager Muted >:X")
		if muteDebug:
			print("[Notification Debug] Notification Debug Muted ÷X")
		
		self.font = pygame.font.SysFont("Arial", 48)
		
		# loadImage("ui.png", size)
		# loadImage("ui.png", 0, width, height)
		self.ui = [
		loadImage("popup.png").convert_alpha(),
		loadImage("eraser.png").convert(),
		loadImage("eraserOn.png").convert(),
		loadImage("rotate.png").convert(),
		loadImage("play.png").convert(),
		loadImage("pause.png").convert(),
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
		
		self.popup = False
		
		self.grid = self.window.copy()
		
		self.updateGrid()
		
		#pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.KEYUP]) 
		
		self.clock = pygame.time.Clock()

		self.running = True
		#blocks = []
		self.blocks = {}
		self.datas = []
		self.clear = True
		self.deleteMode = False
		self.textInput = False
		self.dir = 0
		self.rects = []
		self.xy = {}
		self.popupRotate = 180
		self.pr = 180
		self.blockRotate = 0
		self.br = 0
		self.eraserX = 0
		self.ex = 0
		self.id = 0
		self.select = False
		self.devLoad = pygame.transform.scale(loadImage("devMode.png", 256), (256, 64)).convert_alpha()
		self.devLoad.set_colorkey((0, 0, 0))
		self.selectStart = None
		self.selected = ()
			
		self.lastSize = (0, 0)
		self.winSize = (0, 0)

		self.openOption = None
		self.openOptionBlock = None

		self.tick = 0
		self.second = 0

		self.crashing = False
		self.crashTick = 0
		
		self.bgFade = pygame.Surface(self.window.get_size(), pygame.SRCALPHA).convert_alpha()
		self.bgFade.fill("black")

	def show_android_keyboard(self):
		pygame.key.start_text_input()
	
	def hide_android_keyboard(self):
		pygame.key.stop_text_input()

	def updateGrid(self):
		self.gridBuf = self.window.copy()
	
		self.gridBuf.fill((47, 47, 47))
		for x in range(self.gridBuf.get_width() // tileSize + 1):
			for i in range(tileSize // 8):
				pygame.draw.line(self.gridBuf, (66, 66, 66), (x * tileSize + i - tileSize // 16, 0), (x * tileSize + i - tileSize // 16, self.gridBuf.get_height()))
		for y in range(self.gridBuf.get_height() // tileSize + 1):
			for i in range(tileSize // 8):
				pygame.draw.line(self.gridBuf, (66, 66, 66), (0, y * tileSize + i - tileSize // 16), (self.gridBuf.get_width(), y * tileSize + i - tileSize // 16))
		for y in range(self.gridBuf.get_height() // tileSize + 1):
			for x in range(self.gridBuf.get_width() // tileSize + 1):
				pygame.draw.rect(self.gridBuf, (66, 66, 66), (tileSize // 16 + x * tileSize, tileSize // 16 + y * tileSize, tileSize // 16, tileSize // 16))
				pygame.draw.rect(self.gridBuf, (66, 66, 66), (tileSize // 16 + x * tileSize + (tileSize // 16 * 13), tileSize // 16 + y * tileSize, tileSize // 16, tileSize // 16))
				pygame.draw.rect(self.gridBuf, (66, 66, 66), (tileSize // 16 + x * tileSize, tileSize // 16 + y * tileSize + (tileSize // 16 * 13), tileSize // 16, tileSize // 16))
				pygame.draw.rect(self.gridBuf, (66, 66, 66), (tileSize // 16 + x * tileSize + (tileSize // 16 * 13), tileSize // 16 + y * tileSize + (tileSize // 16 * 13), tileSize // 16, tileSize // 16))
		self.gridBuf = self.gridBuf.convert()
		self.grid = self.gridBuf.copy()
	
	def mouseButtonDown(self, e):
		done = False
		
		if self.devMode:
			if pygame.Rect((0, self.window.get_height() - self.devLoad.get_height()), self.devLoad.get_size()).collidepoint(e.pos):
				self.crashing = True
				done = True
		
		if pygame.Rect(self.window.get_width() - tileSize, self.window.get_height() - tileSize, tileSize, tileSize).collidepoint(e.pos):
			self.popupRotate += 180
			self.popupRotate %= 360
			self.eraserX -= tileSize
			if self.eraserX == -tileSize:
				self.eraserX = tileSize
			self.popup = not self.popup
			done = True
			
		if pygame.Rect(self.window.get_width() - tileSize, self.window.get_height() - tileSize * 2, tileSize, tileSize).collidepoint(e.pos) and self.popup:
			self.deleteMode = not self.deleteMode
			done = True
		
		if pygame.Rect(self.window.get_width() - tileSize, self.window.get_height() - tileSize * 3, tileSize, tileSize).collidepoint(e.pos) and self.popup:
			self.id += 1
			self.id %= len(blockIds)
			done = True
		
		if pygame.Rect(self.window.get_width() - tileSize, self.window.get_height() - tileSize * 4, tileSize, tileSize).collidepoint(e.pos) and self.popup:
			self.dir -= 90
			self.dir %= 360
			done = True
		
		if pygame.Rect(self.window.get_width() - tileSize, self.window.get_height() - tileSize * 5, tileSize, tileSize).collidepoint(e.pos) and self.popup:
			values.setStart(not values.start)
			if values.start:
				for i in self.blocks.values():
					idObj = i.idObj
					if idObj.RunOnStart:
						idObj.function(i, idObj, self.blocks.values(), self.datas)
			else:
				for i in self.blocks.values():
					i.values = {}
			done = True
			
		if pygame.Rect(self.window.get_width() - tileSize, self.window.get_height() - tileSize * 6, tileSize, tileSize).collidepoint(e.pos) and self.popup:
			if bool(self.selected) and (self.selected[2], self.selected[3]) == (tileSize, tileSize) and (self.selected[0] // tileSize, self.selected[1] // tileSize) in self.blocks.keys() and self.blocks[(self.selected[0] // tileSize, self.selected[1] // tileSize)].idObj.HasOptions:
				self.textInput = not self.textInput
			done = True
	
		if bool(self.selected) and (self.selected[2], self.selected[3]) == (tileSize, tileSize) and (self.selected[0] // tileSize, self.selected[1] // tileSize) in self.blocks.keys():
			selectedOptionBlock = self.blocks[(self.selected[0] // tileSize, self.selected[1] // tileSize)]
			for v, i in enumerate(selectedOptionBlock.options.keys()):
				if pygame.Rect(self.window.get_width() - tileSize * 5, self.window.get_height() - tileSize * (6 - v), tileSize * 4, tileSize).collidepoint(e.pos) and self.popup and self.textInput:
					self.show_android_keyboard()
					self.openOption = i
					self.openOptionBlock = (self.selected[0] // tileSize, self.selected[1] // tileSize)
					done = True
		
		if pygame.Rect(self.window.get_width() - tileSize, self.window.get_height() - tileSize * 7, tileSize, tileSize).collidepoint(e.pos) and self.popup:
			self.select = not self.select
			done = True
			
		collide = pygame.Rect(e.pos, (1, 1)).collidelist(self.rects)
		
		if self.textInput and not pygame.Rect(self.window.get_width() - tileSize * 5, self.window.get_height() - tileSize * 6, tileSize * 5, tileSize * len(selectedOptionBlock.options)).collidepoint(e.pos):
			self.hide_android_keyboard()
			self.openOption = None
			self.openOptionBlock = None
			done = True
			
		selectCollide = False	
		if bool(self.selected):
			selectCollide = pygame.Rect(self.selected).collidepoint(e.pos) or pygame.Rect(self.selected[0], self.selected[1] + self.selected[3], tileSize * 3, tileSize).collidepoint(e.pos)
	
		if not done and bool(self.selected) and not selectCollide:
			self.selected = ()
			done = True
		
		if not done and not self.select and not self.selected:
			placePos = (int(numpy.floor(e.pos[0] // tileSize)), int(numpy.floor(e.pos[1] // tileSize))) 
			if not self.deleteMode and collide == -1:
				self.blocks[placePos] = Block(numpy.floor(e.pos[0] / tileSize) * tileSize, numpy.floor(e.pos[1] / tileSize) * tileSize, self.id, self.dir)
			if collide > -1 and self.deleteMode:
				del self.blocks[placePos]
				clear = True
			if not self.deleteMode and collide > -1:
				pass
		if self.select and not done and not selectCollide:
			self.selectStart = [numpy.floor(e.pos[0] / tileSize) * tileSize, numpy.floor(e.pos[1] / tileSize) * tileSize]

	def main(self, eventQueue=[]):
		if self.tick == 60:
			self.tick = 0
			self.second += 1
			self.ui[11].frame += 1
			self.ui[11].frame %= 4
		self.window.fill((47, 47, 47))
		
		if self.crashing:
			self.crashTick += 1
		
		if self.crashTick % 60 == 1:
			counter = 3 - int(numpy.floor(self.crashTick / 60))
			if counter == 0:
				class DevModeCrash(Exception):
					pass
				class Quit(Exception):
					pass
				raise DevModeCrash("Crashed")
			notify(f"Crashing in {counter}")
	
		winSize = self.window.get_size()
	
		if winSize != self.lastSize:
			threading.Thread(target=self.updateGrid).start()
	
		self.br %= 360
		self.rects = []
		for block in self.blocks.values():
			self.rects.append(pygame.Rect(block.x, block.y, tileSize, tileSize))
		self.xy = {}
		for block in self.blocks.values():
			self.xy[(block.x, block.y)] = block
		
		
		self.clock.tick(60)
		
		
		self.window.blit(self.grid, (0, 0))
		if values.start:
			for data in self.datas:
				bc = False
				for block in self.blocks.values():
					if data.collideBlock(block) and block.HasInput:
						bc = True
						break
				if not bc:
					self.datas.remove(data)
			for block in self.blocks.values():
				block.update(self.blocks, self.datas)
		elif len(self.datas) > 0:
			self.datas = []
		for block in self.blocks.values():
			self.window.blit(pygame.transform.rotate(block.idObj.imgFile, block.dir), (block.x, block.y))
		if not bool(self.datas):
			values.setStart(False)
	
		if self.selectStart:
			pos = pygame.mouse.get_pos()
			pos = [numpy.floor((pos[0] + tileSize) / tileSize) * tileSize, numpy.floor((pos[1] + tileSize) / tileSize) * tileSize]
			pX, pY = self.selectStart
			sX = pos[0] - self.selectStart[0]
			sY = pos[1] - self.selectStart[1]
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
			self.window.blit(self.ui[12].get_image_from_size((sX, sY)).convert_alpha(), (pX, pY))
		if bool(self.selected):
			self.window.blit(self.ui[12].get_image_from_size((self.selected[2], self.selected[3])).convert_alpha(), (self.selected[0::1]))
			self.window.blit(self.ui[13], (self.selected[0], self.selected[1] + self.selected[3]))
			self.window.blit(self.ui[14], (self.selected[0] + tileSize, self.selected[1] + self.selected[3]))
			self.window.blit(self.ui[15], (self.selected[0] + tileSize * 2, self.selected[1] + self.selected[3]))
	
		if bool(self.openOption):
			#self.window.blit(tSur, (0, 0))
			cEdit = fontP.render(f"Editing \"{self.openOption}\"", "white", 32).convert_alpha()
			self.window.blit(cEdit, (0, 58))
			pygame.draw.line(self.window, "white", (0, 100), (cEdit.get_width() + 30, 100), tileSize // 16)
	
		if self.popupRotate > self.pr:
			self.pr += 20
		elif self.popupRotate < self.pr:
			self.pr -= 20
	
		if self.dir > self.br or self.dir < self.br:
			self.br -= 10
	
		if self.eraserX > self.ex:
			self.ex += tileSize / 8
		elif self.eraserX < self.ex:
			self.ex -= tileSize / 8
		self.window.blit(self.ui[2], (self.window.get_width() - self.ex, self.window.get_height() - tileSize * 2))
	
		idSurface = pygame.transform.rotate(blockIds[self.id].imgFile.convert_alpha(), self.br)
		idRect = idSurface.get_rect(center=(self.window.get_width() + tileSize / 2 - self.ex, self.window.get_height() - tileSize * 2.5))
		self.window.blit(idSurface, idRect)
	
		if self.deleteMode:
			self.window.blit(self.ui[2], (self.window.get_width() - self.ex, self.window.get_height() - tileSize * 2))
		else:
			self.window.blit(self.ui[1], (self.window.get_width() - self.ex, self.window.get_height() - tileSize * 2))
		popupSurface = pygame.transform.rotate(self.ui[0], self.pr)
		popupRect = popupSurface.get_rect(center=(self.window.get_width() - tileSize / 2, self.window.get_height() - tileSize / 2))
		self.window.blit(popupSurface, popupRect)
	
		self.window.blit(self.ui[3], (self.window.get_width() - self.ex, self.window.get_height() - tileSize * 4))
	
		if values.start:
			self.window.blit(self.ui[5], (self.window.get_width() - self.ex, self.window.get_height() - tileSize * 5))
		else:
			self.window.blit(self.ui[4], (self.window.get_width() - self.ex, self.window.get_height() - tileSize * 5))
	
		oPos = (self.window.get_width() - self.ex, self.window.get_height() - tileSize * 6) 
		self.window.blit(self.ui[6], oPos) 
		if bool(self.selected) and (self.selected[2], self.selected[3]) == (tileSize, tileSize) and (self.selected[0] // tileSize, self.selected[1] // tileSize) in self.blocks.keys() and self.blocks[(self.selected[0] // tileSize, self.selected[1] // tileSize)].idObj.HasOptions:
			if self.textInput:
				options = self.blocks[(self.selected[0] // tileSize, self.selected[1] // tileSize)].options
				for v, i in enumerate(options):
					pos = (self.window.get_width() - tileSize * 5, self.window.get_height() - tileSize * (6 - v))
					name = fontP.render(i, "white", tileSize // 2)
					value = pygame.Surface((0, 0))
					try:
						if type(options[i]) != custom:
							value = fontP.render(str(options[i]), (47, 47, 47), tileSize // 3)
						elif type(options[i]) == str:
							value = fontP.render(options[i], (47, 47, 47), tileSize // 3)
					except:
						pass
					self.window.blit(name, [pos[0] - name.get_width() - tileSize // 4, pos[1] + tileSize // 4])
					self.window.blit(self.ui[8], pos)
					self.window.blit(value, [pos[0] + tileSize // 2, pos[1] + tileSize // 8 * 2.5])
		else:
			self.window.blit(self.ui[9], (self.window.get_width() - self.ex, self.window.get_height() - tileSize * 6))
	
		if self.select:
			self.window.blit(self.ui[11].get_frame().convert(), (self.window.get_width() - self.ex, self.window.get_height() - tileSize * 7))
		else:
			self.window.blit(self.ui[10].convert(), (self.window.get_width() - self.ex, self.window.get_height() - tileSize * 7)) 
	
		if self.devMode:
			self.window.blit(self.devLoad, (0, self.window.get_height() - self.devLoad.get_height()))
	
		fps = int(self.clock.get_fps())
		#fpsRender = font.render("FPS: " + str(fps), (max(255 - min(fps / 60 * 255, 255), 0), min(fps / 60 * 255, 255), 0), (max(255 - min(fps / 60 * 255, 255), 0), min(fps / 60 * 255, 255), 0))
		fpsRender = fontP.render("FPS: " + str(fps), (max(255 - min(fps / 60 * 255, 255), 0), min(fps / 60 * 255, 255), 0), 48)
		self.window.blit(fpsRender, (0, 0))
	
		for i in notifications:
			self.window.blit(i[0], (i[1], i[2]))
			alpha = i[0].get_alpha()
			i[0].set_alpha(alpha - 2)
			i[2] -= 2
			if i[0].get_alpha() < 1:
				notifications.remove(i)
	
		self.rects.append(pygame.Rect(self.window.get_width(), self.window.get_height() - tileSize * 3, 1, tileSize * 3))
	
		if self.bgFade:
			self.window.blit(self.bgFade, (0, 0))
			self.bgFade.set_alpha(self.bgFade.get_alpha() - 60)
			if self.bgFade.get_alpha() < 1:
				self.bgFade = False
	
		events = list(pygame.event.get())
	
		if bool(eventQueue):
			for i in eventQueue:
				events.append(i)
	
		for e in events:
			if e.type == pygame.QUIT:
				if fps <= 10:
					print("[GLOX] Performance Issue Detected :O, if you think this isn't right or it insist, please report this problem in our issue tracker :)")
				print("\n[GLOX] === # Save Code # ===")
				saveCode = ""
				for i in self.blocks.values():
					# Save Format
					# id:x:y:dir;
					saveCode += f"{i.id}:{int(i.x // tileSize)}:{int(i.y // tileSize)}:{int(i.dir // 90)};"
				print("[GLOX] " + str(saveCode))
				print("[GLOX] ===================")
				print("\n[GLOX] Process exited")
				self.running = False
				class Quit(Exception):
					pass
				raise Quit("Quit")
			if e.type == pygame.MOUSEBUTTONDOWN:
				self.mouseButtonDown(e)
			if e.type == pygame.KEYDOWN:
				try:
					if e.mod == 1:
						e.unicode = keyMod.mod_to_str(e.unicode)
					if bool(self.openOption) and len(str(e.key)) < 4:
						option = self.blocks[self.openOptionBlock].options[self.openOption]
						if isinstance(option, str):
							if e.unicode == "\b":
								self.blocks[self.openOptionBlock].options[self.openOption] = self.blocks[self.openOptionBlock].options[self.openOption][:-1]
							elif e.key == pygame.K_RETURN:
								self.openOption = None
								self.hide_android_keyboard()
							else:
								self.blocks[self.openOptionBlock].options[self.openOption] += e.unicode
						if isinstance(option, int) and e.unicode in "1234567890":
							self.blocks[openOptionBlock].options[self.openOption] = int(str(option) + e.unicode)
						if not values.muteDebug:
							print(f"[Options] {self.blocks[self.openOptionBlock]} [{self.openOption}] = {self.blocks[self.openOptionBlock].options[self.openOption]}")
				except:
					pass
			if e.type == pygame.MOUSEBUTTONUP:
				if bool(self.selectStart):
					self.selectStart = None 
					self.selected = (int(pX), int(pY), sX, sY)
				self.crashing = False
				self.crashTick = 0
		pygame.event.pump()
		pygame.display.flip()
		self.lastSize = winSize
		self.tick += 1