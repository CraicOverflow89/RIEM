from abc import ABC, abstractmethod
from PIL import Image, ImageTk
from riem.debug import Debug, DebugChannel
from riem.graphics import Align, Graphics, Menu
from riem.input import Action, Controller, Keyboard
from riem.library import ArrayList, Dimensions, Point
from riem.version import __version__
from tkinter import Canvas, Tk
from typing import Any, Callable, Dict
import importlib, inspect, os, re, sys, time

class Application:

	def __init__(self, title: str, state_initial: str, state_directory: str, default_text: Dict[str, str] = None, icon: str = None, size: Dimensions = Dimensions(960, 720), tick_ms: int = 250, **kwargs) -> None:

		# Parse Kwargs
		for k, v in kwargs.items():

			# Option: Debug
			if k == "debug": Application._debug_parse(v, title, size, tick_ms)

		# Public Properties
		self.size: Dimensions = size

		# State Logic
		def state_load(directory: str) -> Dict[str, State]:

			# Debug
			Debug.print("Loading states from directory %s" % directory, DebugChannel.STATE)

			# Directory Path
			directory_path = os.path.join(os.getcwd(), directory)

			# List Files
			file_list = ArrayList(os.listdir(directory_path)).reject(lambda it: it.startswith("_")).map(lambda it: it.split(".")[0])
			# NOTE: current reject is not going to ignore directories

			# Module Logic
			# def load_module(module: module) -> List[module]:
			# type is <class 'module'> but hasn't been imported
			def load_module(module):

				# List Attributes
				result = ArrayList(list(module.__dict__.keys())).reject(lambda it: it == "State")

				# Map Classes
				result = result.map(lambda it: (it, getattr(module, it)))

				# Return States
				return result.filter(lambda _, v: inspect.isclass(v) and issubclass(v, State))

			# Return States
			result = {}
			for module in file_list.map(lambda it: load_module(importlib.import_module("%s.%s" % (directory.split("/")[-1], it)))):
				for name, state in module:
					result[name] = state
					Debug.print(" - %s" % name, DebugChannel.STATE)
			return result

		# State Management
		self.state_active = None
		self.state_stored = None
		self.state_loaded = state_load(state_directory)
		self.state_bind = lambda: self.app.bind("<Key>", self.on_key_pressed)
		# NOTE: these shouldn't be public

		# Create Application
		Debug.print("Creating application", DebugChannel.RIEM)
		self.app = Tk()
		self.app.title(title)
		self.app.geometry("%dx%d" % (self.size.width, self.size.height))
		self.app.resizable(False, False)
		if icon is not None:
			Debug.print(" - locating custom icon %s" % icon, DebugChannel.RIEM)
			self.app.iconbitmap(r'%s' % os.path.join(os.getcwd(), "resources", "icons", "%s.ico" % icon))
		# NOTE: self.app shouldn't be public

		# Create Canvas
		canvas = Canvas(self.app, bg = "black", width = self.size.width, height = self.size.height, highlightthickness = 0)
		canvas.pack()

		# Create Graphics
		gfx: Graphics = Graphics(canvas, default_text)

		# Intro State
		self.state_active = StateIntro(self, state_initial)

		# Initialise Controller
		Debug.print("Initialising controller", DebugChannel.INPUT)
		self.controller = Controller(self)

		# Application Status
		self.running = True

		# Create Loop
		def loop() -> None:

			# Not Running
			if self.running is not True:
				return

			# Timer Start
			loop_time: int = (time.time() * 1000)

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
			loop_wait: int = 0
			if loop_time < tick_ms:
				loop_wait = tick_ms - loop_time
			self.app.after(int(loop_wait), loop)

		# Invoke Loop
		loop()

		# Start Application
		Debug.print("Initialising application loop", DebugChannel.RIEM)
		self.app.mainloop()

	def _debug_parse(value: str, title: str, size: Dimensions, tick_ms: int) -> None:

		# Invalid Value
		if not isinstance(value, str) or re.match(r"^[\+\-][A-Z]*$", value) is False:
			raise Exception("Invalid debug string!")

		# Disable Channels
		if value[0] == "-":

			# Disable All
			if len(value) == 1:
				return

			# Disable Specific
			if "R" not in value: Debug.debug_channels[DebugChannel.RIEM] = True
			if "S" not in value: Debug.debug_channels[DebugChannel.STATE] = True
			if "A" not in value: Debug.debug_channels[DebugChannel.AUDIO] = True
			if "G" not in value: Debug.debug_channels[DebugChannel.GRAPHICS] = True
			if "I" not in value: Debug.debug_channels[DebugChannel.INPUT] = True

		# Enable Channels
		if value[0] == "+":

			# Enable All
			if len(value) == 1:
				Debug.debug_channels = {
					DebugChannel.RIEM: True,
					DebugChannel.STATE: True,
					DebugChannel.AUDIO: True,
					DebugChannel.GRAPHICS: True,
					DebugChannel.INPUT: True
				}

			# Enable Specific
			if "R" in value: Debug.debug_channels[DebugChannel.RIEM] = True
			if "S" in value: Debug.debug_channels[DebugChannel.STATE] = True
			if "A" in value: Debug.debug_channels[DebugChannel.AUDIO] = True
			if "G" in value: Debug.debug_channels[DebugChannel.GRAPHICS] = True
			if "I" in value: Debug.debug_channels[DebugChannel.INPUT] = True

		# Print Info
		print("")
		Debug.print("Application Debug Mode")
		Debug.print("======================")
		Debug.print("Version: %s" % __version__)
		Debug.print("Project: %s" % title)
		Debug.print("Window:  %d x %d" % (size.width, size.height))
		Debug.print("Tick:    %d ms" % tick_ms)
		Debug.print()

	def action(self, action: Action) -> None:
		Debug.print(action, DebugChannel.STATE)
		self.state_active.on_action(action)

	def get_dimensions(self) -> Dimensions:
		return self.size

	def get_version(self) -> str:
		return __version__

	def on_key_pressed(self, event: Any) -> None:
		# NOTE: event should be specifically typed here
		if event.keycode in Keyboard.action:
			Debug.print(event, DebugChannel.INPUT)
			self.action(Keyboard.action[event.keycode])

	def state_revert(self, data: Dict = None) -> None:

		# Debug
		Debug.print("Reverting to stored state", DebugChannel.STATE)

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

	def state_update(self, state: str, store: bool = False, data: Dict = None) -> None:

		# Debug
		Debug.print("Updating to %s state" % state, DebugChannel.STATE)

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

	def terminate(self) -> None:

		# Already Terminating
		if self.running is False:
			return

		# Debug
		Debug.print("Terminating application")

		# Application Status
		self.running = False

		# Terminate Controller
		self.controller.terminate()

		# System Exit
		sys.exit()

class State(ABC):

	def __init__(self, app: Application) -> None:
		self.app = app
		self.event = ArrayList()

	def add_event(self, time_ms: int, logic: Callable) -> None:

		# Create Event
		event_new = {
			"logic": logic,
			"timer": (time.time() * 1000) + time_ms
		}

		# Debug
		Debug.print("Creating new event %d to fire in %d ms" % (id(event_new), time_ms), DebugChannel.STATE)

		# Append Event
		self.event = self.event.add(event_new)

	def on_action(self, action: Action) -> None:
		pass

	def on_revert(self, data: Dict) -> None:
		pass

	def on_start(self, data: Dict) -> None:
		pass

	def on_store(self) -> None:
		pass

	def on_terminate(self) -> None:
		pass

	@abstractmethod
	def render(self, gfx: Graphics) -> None:
		pass

	def render_hint(self, gfx: Graphics, value: str) -> None:
		gfx.draw_text(value, Point(10, self.app.get_dimensions().height - 25), Align.LEFT, "Inconsolata 12")
		# NOTE: maybe make this game specific (move to a helper class or graphics library of styles?)

	def render_title(self, gfx: Graphics, value: str) -> None:
		gfx.draw_text(value, Point(25, 25), Align.LEFT, "Inconsolata 22", "#E62959", "#801731")
		# NOTE: maybe make this game specific (move to a helper class or graphics library of styles?)

	@abstractmethod
	def tick(self) -> None:
		pass

	def tick_event(self) -> None:

		# Check Events
		time_ms: int = time.time() * 1000
		for event in self.event.filter(lambda it: time_ms >= it["timer"]):

			# Debug
			Debug.print("Invoking event %d" % id(event), DebugChannel.STATE)

			# Invoke Logic
			event["logic"]()

			# Remove Event
			self.event = self.event.remove(event)

class StateIntro(State):

	def __init__(self, app: Application, state_initial: str) -> None:
		super().__init__(app)

		# Create Event
		self.add_event(2000, lambda: self.app.state_update(state_initial))

	def render(self, gfx: Graphics) -> None:

		# Load Logo
		self.logo = ImageTk.PhotoImage(Image.open("resources/images/brand/riem_logo.png"))
		# NOTE: this is currently assuming the file exists in project
		#       change this later to use a predefined byte array

		# Render Logo
		gfx.draw_image(self.logo, Point(self.app.get_dimensions().width / 2, self.app.get_dimensions().height / 2), Align.CENTER)

		# Render Loading
		# NOTE: when resources are preloaded, there should be an object that fires off these tasks
		#       and provides a completion percentage to the a progress bar object that renders

	def tick(self) -> None:
		pass