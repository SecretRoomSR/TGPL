keys = {}

with open("./assets/mod/modDict", "r") as file:
	for i in file.read().split("\n"):
		if len(i) > 3:
			a, b = i.split(": ")
			keys.update({a: b})

def mod_to_str(char):
	if char in keys.values():
		valList = list(keys.values()) 
		return list(keys.keys())[valList.index(char)]
	return ""