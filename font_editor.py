from PIL import Image
import numpy

img = Image.open("./assets/font/font.png")
img = img.convert("RGB")

offset = [0, 0]
asd = ""
asdo = ""
autoscroll = False
while True:
	pixels = []
	for y in range(5):
		currentX = []
		for x in range(5):
			r, g, b = img.getpixel((x + offset[0], y + offset[1]))
			currentX.append([r, g, b])
		pixels.append(currentX)
	
	for array in pixels:
		for pix in array:
			if pix[0] == 255:
				print("#", end="")
			else:
				print(" ", end="")
		print()
	if autoscroll:
		dir = "as"
		offset[0] += 5
		if offset[0] == 50:
			offset[0] = 0
			offset[1] += 5
		if offset[1] == 50:
			offset = [0, 0]
			autoscroll = False
	else:
		dir = input("dir: ")
	if dir == "w":
		offset[1] -= 5
	if dir == "a":
		offset[0] -= 5
	if dir == "s":
		offset[1] += 5
	if dir == "d":
		offset[0] += 5
	if dir == "as":
		asg = input("assign: ")
		if asg == "autoscroll":
			autoscroll = not autoscroll
		else:
			asd += asg[0] + "\n"
			asdo += f"({offset[0] - 5}, {offset[1]})\n"
	if dir == "view":
		asdos = asdo.split("\n")
		for i, o in enumerate(asd.split()):
			print(o, asdos[i])
	if dir == "exit":
		toBeSaved = ""
		with open("./assets/font/sheet", "w") as f:
			asdos = asdo.split("\n")
			for i, o in enumerate(asd.split()):
				toBeSaved += f"{o}, {asdos[i]}\n"
			f.write(toBeSaved)
		break
	offset[0] %= 50
	offset[1] %= 50
	if offset[0] == -5:
		offset[0] = 45
	if offset[1] == -5:
		offset[1] = 45