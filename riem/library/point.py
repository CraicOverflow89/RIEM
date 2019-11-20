class Point:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __mul__(self, other):
		return Point(self.x * other.x, self.y * other.y)

	def __neq__(self, other):
		return self.x != other.x or self.y != other.y

	def __str__(self):
		return "{x: %d, y: %d}" % (self.x, self.y)

	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y)

	def __truediv__(self, other):
		return Point(self.x / other.x, self.y / other.y)