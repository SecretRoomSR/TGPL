from loadImage import loadImage

class UniqueID:
	def __init__(self, name, texture, function, HasInput=False, HasOptions=False, options={}, UpdateEveryFrame=True, RunOnStart=False):
		self.name = name
		self.HasInput = HasInput
		self.HasOptions = HasOptions
		if function:
			self.function = function
		else:
			self.function = None
		self.options = options
		if not HasOptions:
			self.options = {}
		self.imgFile = loadImage(texture)
		self.UpdateEveryFrame = UpdateEveryFrame
		self.RunOnStart = RunOnStart