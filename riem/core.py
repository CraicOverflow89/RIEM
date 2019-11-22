from abc import ABC, abstractmethod
from riem.graphics import Align, Graphics
from riem.input import Controller, Keyboard
from riem.library import ArrayList, Dimensions, Point
from riem.library import Point
from tkinter import Canvas, Tk
import importlib, inspect, os, re, sys, time

class Application:

	# Constants
	version = "0.0.1"
	tick_ms = 250

	def __init__(self, title, state_initial, state_directory, size = Dimensions(960, 720)):

		# State Logic
		def state_load(directory):

			# Directory Path
			directory_path = os.path.join(os.getcwd(), directory)

			# List Files
			file_list = ArrayList(os.listdir(directory_path)).reject(lambda it: it.startswith("_")).map(lambda it: it.split(".")[0])
			# NOTE: current reject is not going to ignore directories

			# Module Logic
			def load_module(module):

				# List Attributes
				result = ArrayList(list(module.__dict__.keys())).reject(lambda it: it == "State")

				# Map Classes
				result = result.map(lambda it: getattr(module, it)).map(lambda it: (it.get_name(), it))

				# Return States
				return result.filter(lambda _, v: inspect.isclass(v) and issubclass(v, State))

			# Return States
			result = {}
			for module in file_list.map(lambda it: load_module(importlib.import_module("%s.%s" % (directory.split("/")[-1], it)))):
				for name, state in module:
					result[name] = state
			return result

		# State Management
		self.state_active = None
		self.state_stored = None
		self.state_loaded = state_load(state_directory)
		self.state_bind = lambda: self.app.bind("<Key>", self.on_key_pressed)
		# NOTE: these shouldn't be public

		# Create Application
		self.app = Tk()
		self.app.title(title)
		self.app.geometry("%dx%d" % (self.size.width, self.size.height))
		self.app.resizable(False, False)

		# Create Canvas
		canvas = Canvas(self.app, bg = "black", width = self.size.width, height = self.size.height, highlightthickness = 0)
		canvas.pack()

		# Create Graphics
		gfx = Graphics(canvas)

		# Initial State
		self.state_update(state_initial)

		# Initialise Controller
		self.controller = Controller(self)

		# Application Status
		self.running = True

		# Create Loop
		def loop():

			# Not Running
			if self.running is not True:
				return

			# Timer Start
			loop_time = (time.time() * 1000)

			# Controller Actions
			self.controller.get_actions().each(lambda it: self.action(it))

			# Application Tick
			self.state_active.tick()
			self.state_active.tick_event()

			# Application Render
			gfx.draw_rect(Point(0, 0), self.size, "black", True)
			self.state_active.render(gfx)

			# Schedule Loop
			loop_time = (time.time() * 1000) - loop_time
			loop_wait = 0
			if loop_time < Application.tick_ms:
				loop_wait = Application.tick_ms - loop_time
			self.app.after(int(loop_wait), loop)

		# Invoke Loop
		loop()

		# Start Application
		self.app.mainloop()

	def action(self, action):
		self.state_active.on_action(action)

	def get_dimensions(self):
		return self.size

	def get_version(self):
		return Application.version

	def on_key_pressed(self, event):
		if event.keycode in Keyboard.action:
			self.action(Keyboard.action[event.keycode])

	def state_revert(self, data = None):

		# Nothing Stored
		if self.state_stored is None:
			raise Exception("No stored state to revert to!")

		# Terminate Existing
		self.state_active.on_terminate()

		# Revert State
		self.state_active = self.state_stored
		self.state_active.on_revert(data)
		self.state_stored = None

		# Bind Events
		self.state_bind()

	def state_update(self, state, store = False, data = None):

		# Existing State
		if self.state_active is not None:

			# Store Existing
			if store is True:
				self.state_active.on_store()
				self.state_stored = self.state_active

			# Terminate Existing
			else:
				self.state_active.on_terminate()

		# Initialise State
		self.state_active = self.state_loaded[state](self)
		# NOTE: put the above into a method to gracefully handle this
		self.state_active.on_start(data)

		# Bind Events
		self.state_bind()

	def terminate(self):

		# Already Terminating
		if self.running is False:
			return

		# Application Status
		self.running = False

		# Terminate Controller
		self.controller.terminate()

		# System Exit
		sys.exit()

class State(ABC):

	def __init__(self, app):
		self.app = app
		self.event = ArrayList()

	def add_event(self, time_ms, logic):
		self.event = self.event.add({
			"logic": logic,
			"timer": (time.time() * 1000) + time_ms
		})

	def on_action(self, action):
		pass

	def on_revert(self, data):
		pass

	def on_start(self, data):
		pass

	def on_store(self):
		pass

	def on_terminate(self):
		pass

	@abstractmethod
	def render(self, gfx):
		pass

	def render_hint(self, gfx, value):
		gfx.draw_text(value, Point(10, self.app.get_dimensions().height - 25), Align.LEFT, "Inconsolata 12")
		# NOTE: maybe make this game specific (move to a helper class or graphics library of styles?)

	def render_title(self, gfx, value):
		gfx.draw_text(value, Point(25, 25), Align.LEFT, "Inconsolata 22", "#E62959", "#801731")
		# NOTE: maybe make this game specific (move to a helper class or graphics library of styles?)

	@abstractmethod
	def tick(self):
		pass

	def tick_event(self):

		# Check Events
		time_ms = time.time() * 1000
		for event in self.event.filter(lambda it: time_ms >= it["timer"]):

			# Invoke Logic
			event["logic"]()

			# Remove Event
			self.event = self.event.remove(event)