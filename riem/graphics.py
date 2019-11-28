import enum
from PIL import Image, ImageTk
from riem.input import Action
from riem.library import ArrayList, Dimensions, Point
from typing import Any, Callable, Dict
import tkinter as tk

class Align(enum.Enum):
	CENTER = 0
	LEFT = 1
	MIDDLE = 2
	RIGHT = 3

class Graphics:

	# Constants
	text_default: Dict[str, str] = {
		"font": "Inconsolata 14",
		"colour": "white"
	}
	anchor: Dict[Align, int] = {
		Align.CENTER: tk.CENTER,
		Align.LEFT: tk.NW,
		Align.MIDDLE: tk.N,
		Align.RIGHT: tk.NE
	}

	def __init__(self, canvas: Any, default_text: Dict[str, str] = None, offset: Point = Point(0, 0)) -> None:
		# NOTE: canvas should have specific type here

		# Public Properties
		self.canvas = canvas
		self.offset = offset

		# Custom Defaults
		if default_text is not None:
			for key in default_text:

				# Invalid Key
				if key not in Graphics.text_default.keys():
					raise Exception("%s is not a valid default text option!" % key)

				# Update Value
				Graphics.text_default[key] = default_text[key]

	def draw_image(self, image: Any, position: Point, align: Align = Align.LEFT) -> None:
		# NOTE: image should have specific type here

		# Apply Offset
		position = position + self.offset

		# Render Image
		self.canvas.create_image(position.x, position.y, image = image, anchor = Graphics.anchor[align])

	def draw_rect(self, position: Point, size: Dimensions, colour: str, fill: bool) -> None:

		# Apply Offset
		position = position + self.offset

		# Render Solid
		if fill is True:
			self.canvas.create_rectangle(position.x, position.y, position.x + size.width, position.y + size.height, fill = colour)

		# Render Outline
		else:
			self.canvas.create_rectangle(position.x, position.y, position.x + size.width, position.y + size.height, outline = colour)

	def draw_text(self, text: str, position: Point, align: Align = Align.LEFT, font: str = None, colour: str = None, shadow: str = None)  -> None:

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

	def offset_graphics(self, offset: Point): # -> Graphics
		return Graphics(self.canvas, None, self.offset + offset)

class ImageLoader:

	# Constants
	data: Dict[str, ImageTk.PhotoImage] = {}

	def _store(image: str, size: Dimensions = None) -> None:
		ImageLoader.data[image] = {"image": ImageTk.PhotoImage(Image.open("resources/images/%s.png" % image)), "size": size}
		# NOTE: images disappear when trying to move the ImageTk.PhotImage to value in ImageLoader.data issues occur

	def load(image: str, size: Dimensions = None) -> ImageTk.PhotoImage:
		# NOTE: this can defer to the load_at method (with default values)

		# Store Image
		if image not in ImageLoader.data:
			ImageLoader._store(image, size)

		# Return Image
		return ImageLoader.data[image]["image"]

	def load_at(image: str, size: Dimensions, point: Point) -> ImageTk.PhotoImage:

		# Store Image
		if image not in ImageLoader.data:
			ImageLoader._store(image, size)

		# Return Image
		return ImageLoader.data[image]["image"]
		# NOTE: will be calling the crop method on the above value

class Menu:

	def __init__(self, offset: Point = Point(-30, 0)) -> None:
		self.option = ArrayList()
		self.active = 0
		self.offset = offset

	def add_option(self, label: str, position: Point, logic: Callable) -> None:
		self.option = self.option.add(MenuItem(self, label, position, logic))

	def get_offset(self) -> Point:
		return self.offset

	def on_action(self, action: Action) -> None:

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

	def render(self, gfx: Graphics) -> None:

		# Render Text
		self.option.each(lambda it: it.render_label(gfx))

		# Render Cursor
		self.option.get(self.active).render_cursor(gfx)

	def set_cursor(self, position: int = 0) -> None:
		if position >= self.option.size(): position = 0
		self.active = position

class MenuItem:

	def __init__(self, menu: Menu, label: str, position: Point, logic: Callable) -> None:
		self.menu = menu
		self.label = label
		self.position = position
		self.logic = logic

	def invoke(self) -> None:
		self.logic()

	def render_cursor(self, gfx: Graphics) -> None:
		gfx.draw_text("->", self.position + self.menu.get_offset())

	def render_label(self, gfx: Graphics) -> None:
		gfx.draw_text(self.label, self.position)