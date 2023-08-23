import os, shutil, sys
from time import sleep

for x in "Please save every open file first.":
	print(x, end="")
	sys.stdout.flush()
	sleep(0.025)
os.system("clear")
input("Please save every open file first.")
print()

for x in "Exporting GLOX...":
	print(x, end="")
	sys.stdout.flush()
	sleep(0.025)
print()

try:
	shutil.rmtree("/storage/emulated/0/GLOX")
except:
	for x in "Old GLOX directory not found, creating new folder...":
		print(x, end="")
		sys.stdout.flush()
		sleep(0.025)
	print()

os.system("cp -r ~/GLOX /storage/emulated/0")

print()

for x in "GLOX Exported":
	print(x, end="")
	sys.stdout.flush()
	sleep(0.025)

while True:
	pass