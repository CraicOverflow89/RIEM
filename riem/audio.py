from riem.debug import Debug, DebugChannel
from riem.library import ArrayList
from threading import Thread
from playsound import playsound

class SoundLoader:

	def play(sound: str) -> None:

		# Debug
		Debug.print("Playing sound %s" % sound, DebugChannel.AUDIO)

		# Thread Logic
		def execute(sound: str, _) -> None:
			playsound("resources/sounds/%s.mp3" % sound)

		# Spawn Thread
		Thread(target = execute, args = (sound, None), daemon = False).start()