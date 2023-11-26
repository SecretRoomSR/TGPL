import os, shutil, sys
from time import sleep

for x in "Please save every open file first.":
	print(x, end="")
	sys.stdout.flush()
	sleep(0.025)
input()
print()

for x in "Exporting GLOX...":
	print(x, end="")
	sys.stdout.flush()
	sleep(0.025)
print()

try:
	shutil.rmtree("/storage/emulated/0/TGPL")
except:
	for x in "Old GLOX directory not found, creating new folder...":
		print(x, end="")
		sys.stdout.flush()
		sleep(0.025)
	print()

os.system("cp -rv ~/GLOX /storage/emulated/0")
os.system("mv /storage/emulated/0/GLOX /storage/emulated/0/TGPL")

print()

for x in "GLOX Exported":
	print(x, end="")
	sys.stdout.flush()
	sleep(0.025)

while True:
	pass