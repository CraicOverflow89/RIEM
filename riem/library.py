import enum

class ArrayList():

	def __init__(self, *value):
		self.value = []
		self.iter_pos = 0
		if len(value) > 0:
			if len(value) == 1 and (isinstance(value[0], list) or isinstance(value[0], ArrayList)):
				value = value[0]
			for element in value:
				self.value.append(element)

	def __iter__(self):
		self.iter_pos = 0
		return self

	def __len__(self):
		return self.size()

	def __next__(self):
		if self.iter_pos == len(self.value):
			raise StopIteration
		result = self.value[self.iter_pos]
		self.iter_pos += 1
		return result

	def __str__(self):
		return "[" + ", ".join(map(lambda it: "'" + str(it) + "'", self.value)) + "]"

	def add(self, value):
		result = self.value
		result.append(value)
		return ArrayList(result)

	def add_all(self, *value):
		result = self.value
		if len(value) == 1 and (isinstance(value[0], list) or isinstance(value[0], ArrayList)):
			value = value[0]
		for element in value:
			result.append(element)
		return ArrayList(result)

	def all(self, logic):
		for element in self.value:
			if isinstance(element, tuple):
				if not logic(*element):
					return False
			else:
				if not logic(element):
					return False
		return True

	def any(self, logic):
		for element in self.value:
			if isinstance(element, tuple):
				if logic(*element):
					return True
			else:
				if logic(element):
					return True
		return False

	def contains(self, value):
		for element in self.value:
			if element == value:
				return True
		return False

	def copy(self):
		result = []
		for element in self.value:
			result.append(element)
		return ArrayList(result)

	def each(self, logic):
		for element in self.value:
			if isinstance(element, tuple):
				logic(*element)
			else:
				logic(element)
		return self

	def filter(self, logic):
		result = []
		for element in self.value:
			if isinstance(element, tuple):
				if logic(*element):
					result.append(element)
			else:
				if logic(element):
					result.append(element)
		return ArrayList(result)

	def first(self, logic = None):
		if logic is None: return self.value[0]
		for element in self.value:
			if isinstance(element, tuple):
				if logic(*element):
					return element
			else:
				if logic(element):
					return element
		return None

	def flatten(self):

		# Create Result
		result = []

		# Unpack Logic
		def unpack(value):

			# Unpack ArrayList
			if isinstance(value, ArrayList):
				for element in value.to_list():
					unpack(element)

			# Unpack List
			elif isinstance(value, list):
				for element in value:
					unpack(element)

			# Append Element
			else: result.append(value)

		# Append Value
		unpack(self.value)

		# Return Result
		return ArrayList(result)

	def get(self, position):
		return self.value[position]

	def is_empty(self):
		return len(self.value) > 0

	def map(self, logic):
		result = []
		for element in self.value:
			if isinstance(element, tuple):
				result.append(logic(*element))
			else:
				result.append(logic(element))
		return ArrayList(result)

	def none(self, logic):
		for element in self.value:
			if isinstance(element, tuple):
				if logic(*element):
					return False
			else:
				if logic(element):
					return False
		return True

	def reject(self, logic):
		result = []
		for element in self.value:
			if isinstance(element, tuple):
				if not logic(*element):
					result.append(element)
			else:
				if not logic(element):
					result.append(element)
		return ArrayList(result)

	def remove(self, value):
		result = []
		for element in self.value:
			if element != value:
				result.append(element)
		return ArrayList(result)

	def reverse(self):
		result = []
		x = len(self.value) - 1
		while x >= 0:
			result.append(self.value[x])
			x -= 1
		return ArrayList(result)

	def size(self):
		return len(self.value)

	def take(self, count):
		if len(self.value) < count:
			count = len(self.value)
		result = []
		for x in range(count):
			result.append(self.value[x])
		return ArrayList(result)

	def to_list(self):
		result = []
		for element in self.value:
			result.append(element)
		return result

	def to_map(self, logic):
		result = {}
		for element in self.value:
			if isinstance(element, tuple):
				key, value = logic(*element)
			else:
				key, value = logic(element)
			result[key] = value
		return result

	def to_string(self, delimiter = "", prefix = "", postfix = ""):
		return "".join([prefix, delimiter.join(self.map(lambda it: str(it)).to_list()), postfix])

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

class Direction(enum.Enum):
	EAST = 0
	NORTH = 1
	SOUTH = 2
	WEST = 3

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