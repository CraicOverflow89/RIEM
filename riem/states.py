from abc import ABC, abstractmethod
from riem.graphics import Align
from riem.library import ArrayList
from riem.library import Point
import time

class State(ABC):

	def __init__(self, app, name):
		self.app = app
		self.name = name
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

	def render_title(self, gfx, value):
		gfx.draw_text(value, Point(25, 25), Align.LEFT, "Inconsolata 22", "#E62959", "#801731")

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