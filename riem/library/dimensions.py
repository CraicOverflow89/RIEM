class Dimensions:

	def __init__(self, width, height):
		self.width = width
		self.height = height

	def __add__(self, value):
		return Dimensions(self.width + value, self.height + value)

	def __mul__(self, value):
		return Dimensions(self.width * value, self.height * value)

	def __str__(self):
		return "{width: %d, height: %d}" % (self.width, self.height)

	def __sub__(self, value):
		return Dimensions(self.width - value, self.height - value)

	def __truediv__(self, value):
		return Dimensions(self.width / value, self.height / value)

	def contains(self, point):
		return point.x >= 0 and point.x <= self.width and point.y >= 0 and point.y <= self.height