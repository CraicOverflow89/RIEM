import enum
from riem.library import ArrayList
from threading import Event, Thread
import pygame

class Action(enum.Enum):
	ACTION = 0
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4

class Controller:

	def __init__(self, app):
		self.app = app
		self.joystick_active = False

		# Action Queue
		self.action_queue = ArrayList()

		# Detect Controller
		pygame.init()
		pygame.joystick.init()
		if pygame.joystick.get_count() == 1:

			# Create Listener
			pygame.joystick.Joystick(0).init()
			self.joystick_active = True
			self.listener_halt = Event()
			self.listener_thread = Thread(target = self.listener, args = (self.listener_halt, self.action_queue), daemon = False)
			self.listener_thread.start()

	def add_action(self, action):
		self.action_queue = self.action_queue.add(action)

	def get_actions(self):

		# Create Result
		result = self.action_queue.copy()

		# Empty Queue
		self.action_queue = ArrayList()

		# Return Actions
		return result

	def listener(self, halt, queue):
		while True:
			if halt.is_set():
				break
			for event in pygame.event.get():
				if event.type == pygame.JOYBUTTONDOWN and (event.button == 0 or event.button == 1):
					self.add_action(Action.ACTION)
				elif event.type == pygame.JOYAXISMOTION and (event.axis == 0 or event.axis == 1):
					if event.axis == 0:
						if event.value >= 0.8:
							self.add_action(Action.RIGHT)
						elif event.value <= -0.8:
							self.add_action(Action.LEFT)
					elif event.axis == 1:
						if event.value >= 0.8:
							self.add_action(Action.DOWN)
						elif event.value <= -0.8:
							self.add_action(Action.UP)

	def terminate(self):
		if self.joystick_active is True:
			self.listener_halt.set()
			self.listener_thread.join()
		pygame.quit()

class Keyboard:

	action = {
		13: Action.ACTION,
		36: Action.ACTION,
		37: Action.LEFT,
		38: Action.UP,
		39: Action.RIGHT,
		40: Action.DOWN,
		111: Action.UP,
		113: Action.LEFT,
		114: Action.RIGHT,
		116: Action.DOWN
	}