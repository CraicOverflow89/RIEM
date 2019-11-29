from typing import Any
import enum

class DebugChannel(enum.Enum):
	RIEM = 0
	STATE = 1
	AUDIO = 2
	GRAPHICS = 3
	INPUT = 4
	
class Debug():

	# Constants
	debug_channels = {
		DebugChannel.RIEM: False,
		DebugChannel.STATE: False,
		DebugChannel.AUDIO: False,
		DebugChannel.GRAPHICS: False,
		DebugChannel.INPUT: False
	}

	def print(value: Any = "", channel: DebugChannel = DebugChannel.RIEM) -> None:

		# Channel Disabled
		if Debug.debug_channels[channel] is False:
			return

		# Print Logic
		def print_value(value: Any) -> None:
			if value == "": print("  |")
			else: print("%s | %s" % (channel.name[0], str(value)))

		# Unpack Lists
		if isinstance(value, list):
			for element in value:
				print_value(element)

		# Print Value
		else: print_value(value)