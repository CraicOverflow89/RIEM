from library.list import ArrayList
from threading import Thread
from playsound import playsound

class SoundLoader:

	def play(sound):

		# Thread Logic
		def execute(sound, _):
			playsound("resources/sounds/%s.mp3" % sound)

		# Spawn Thread
		Thread(target = execute, args = (sound, None), daemon = False).start()