from UniqueID import UniqueID
import numpy
from notifications import notify
from Data import Data
from values import tileSize
import values

class custom:
	pass

def start(block, id, blocks, datas):
	data0 = Data(block.x + tileSize / 4, block.y - (tileSize / 4) * 3)
	data1 = Data(block.x + tileSize / 4, block.y + (tileSize / 4) * 5)
	data2 = Data(block.x - (tileSize / 4) * 3, block.y + tileSize / 4)
	data3 = Data(block.x + (tileSize / 4) * 5, block.y + tileSize / 4)
	bc0 = False
	bc1 = False
	bc2 = False
	bc3 = False
	for block in blocks:
		if data0.collideBlock(block) and block.HasInput:
			bc0 = True
		if data1.collideBlock(block) and block.HasInput:
			bc1 = True
		if data2.collideBlock(block) and block.HasInput:
			bc2 = True
		if data3.collideBlock(block) and block.HasInput:
			bc3 = True
	if bc0:
		datas.append(data0)
	if bc1:
		datas.append(data1)
	if bc2:
		datas.append(data2)
	if bc3:
		datas.append(data3)

def signalLine(block, id, blocks, datas):
	for data in datas:
		if data.collideBlock(block):
			data.x += numpy.sin(numpy.radians(block.dir + 90)) * tileSize
			data.y += numpy.cos(numpy.radians(block.dir + 90)) * tileSize

def end(block, id, blocks, datas):
	for data in datas:
		if data.collideBlock(block):
			values.setStart(not values.start)

def notifyBlock(block, id, blocks, datas):
	for data in datas:
		if data.collideBlock(block):
			notify("hi")
			data.x += numpy.sin(numpy.radians(block.dir + 90)) * tileSize
			data.y += numpy.cos(numpy.radians(block.dir + 90)) * tileSize

def loop(block, id, blocks, datas):
	for data in datas:
		if data.collideBlock(block):
			block.values = {"on": True}
	try:
		if block.values["on"]:
			data0 = Data(block.x + tileSize / 4, block.y - (tileSize / 4) * 3)
			data1 = Data(block.x + tileSize / 4, block.y + (tileSize / 4) * 5)
			data2 = Data(block.x - (tileSize / 4) * 3, block.y + tileSize / 4)
			data3 = Data(block.x + (tileSize / 4) * 5, block.y + tileSize / 4)
			bc0 = False
			bc1 = False
			bc2 = False
			bc3 = False
			for block in blocks:
				if data0.collideBlock(block) and block.HasInput:
					bc0 = True
				if data1.collideBlock(block) and block.HasInput:
					bc1 = True
				if data2.collideBlock(block) and block.HasInput:
					bc2 = True
				if data3.collideBlock(block) and block.HasInput:
					bc3 = True
			if bc0:
				datas.append(data0)
			if bc1:
				datas.append(data1)
			if bc2:
				datas.append(data2)
			if bc3:
				datas.append(data3)
	except:
		pass

#$1: UniqueID("Name", "image.png", function, HasInput=False, HasOptions=False, (if HasOptions) Options, UpdateEveryFrame=True)
#Options {"Option Name": 0}
blockIds = {
0: UniqueID("Start", "start.png", start, UpdateEveryFrame=False, RunOnStart=True),
1: UniqueID("Signal Line", "signalLine.png", signalLine, True),
2: UniqueID("End", "end.png", end, True),
3: UniqueID("Notify", "string.png", notifyBlock, True, True, {"Text": "Text here"}),
4: UniqueID("Set Variable", "setVariable.png", None, True, True, {"Var Name": "", "Var Value": custom()}),
5: UniqueID("Loop", "loop.png", loop, True, True, {"Delay": 0})
}