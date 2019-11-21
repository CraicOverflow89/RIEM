import enum
from PIL import Image, ImageTk
from riem.input import Action
from riem.library import ArrayList
from riem.library import Point
import tkinter as tk

class Align(enum.Enum):
	CENTER = 0
	LEFT = 1
	MIDDLE = 2
	RIGHT = 3

class Graphics:

	# Constants
	text_default = {
		"font": "Inconsolata 14",
		"colour": "white"
	}
	anchor = {
		Align.CENTER: tk.CENTER,
		Align.LEFT: tk.NW,
		Align.MIDDLE: tk.N,
		Align.RIGHT: tk.NE
	}

	def __init__(self, canvas, offset = Point(0, 0)):
		self.canvas = canvas
		self.offset = offset

	def draw_image(self, image, position, align = Align.LEFT):

		# Apply Offset
		position = position + self.offset

		# Render Image
		self.canvas.create_image(position.x, position.y, image = image, anchor = Graphics.anchor[align])

	def draw_rect(self, position, size, colour, fill):

		# Apply Offset
		position = position + self.offset

		# Render Solid
		if fill is True:
			self.canvas.create_rectangle(position.x, position.y, position.x + size.width, position.y + size.height, fill = colour)

		# Render Outline
		else:
			self.canvas.create_rectangle(position.x, position.y, position.x + size.width, position.y + size.height, outline = colour)

	def draw_text(self, text, position, align = Align.LEFT, font = None, colour = None, shadow = None):

		# Apply Offset
		position = position + self.offset

		# Default Font
		if font is None: font = Graphics.text_default["font"]

		# Default Colour
		if colour is None: colour = Graphics.text_default["colour"]

		# Render Shadow
		if shadow is not None:
			self.canvas.create_text(position.x + 1, position.y + 1, text = text, font = font, fill = shadow, anchor = Graphics.anchor[align])

		# Render Text
		self.canvas.create_text(position.x, position.y, text = text, font = font, fill = colour, anchor = Graphics.anchor[align])

	def offset_graphics(self, offset):
		return Graphics(self.canvas, self.offset + offset)

class ImageLoader:

	# Constants
	data = {}

	def load(image):

		# Store Image
		if image not in ImageLoader.data:
			ImageLoader.data[image] = ImageTk.PhotoImage(Image.open("resources/images/%s.png" % image))

		# Return Image
		return ImageLoader.data[image]

class Menu:

	def __init__(self, offset = Point(-30, 0)):
		self.option = ArrayList()
		self.active = 0
		self.offset = offset

	def add_option(self, label, position, logic):
		self.option = self.option.add(MenuItem(self, label, position, logic))

	def get_offset(self):
		return self.offset

	def on_action(self, action):

		# Invoke Option
		if action == Action.ACTION:
			self.option.get(self.active).invoke()
			return

		# Cursor Up
		if action == Action.UP:
			if self.active > 0: self.active -= 1
			return

		# Cursor Down
		if action == Action.DOWN:
			if self.active < self.option.size() - 1: self.active += 1
			return

	def render(self, gfx):

		# Render Text
		self.option.each(lambda it: it.render_label(gfx))

		# Render Cursor
		self.option.get(self.active).render_cursor(gfx)

	def set_cursor(self, position = 0):
		if position >= self.option.size(): position = 0
		self.active = position

class MenuItem:

	def __init__(self, menu, label, position, logic):
		self.menu = menu
		self.label = label
		self.position = position
		self.logic = logic

	def invoke(self):
		self.logic()

	def render_cursor(self, gfx):
		gfx.draw_text("->", self.position + self.menu.get_offset())

	def render_label(self, gfx):
		gfx.draw_text(self.label, self.position)