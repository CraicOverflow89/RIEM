import sys

# Script Logic
def invoke(args):

	# Command: Help
	def help():
		print("Help")
		# NOTE: list commands and args
		#       commands.each {get metadata/annotations of it}

	# Command: Create
	def create(args):
		print("App Skeleton")
		# NOTE: create dirs and files at cwd

	# Command Map
	commands = {
		"create" : create,
		"help" : help
	}

	# No Command
	if len(args) == 0:
		help()

	# Parse Command
	else:

		# Valid Command
		if args[0] in commands.keys():
			commands[args[0]](args[1:])

		# Invalid Command
		else:
			print("Command %s not recognised!" % args[0])
			help()

# Invoke Script
invoke(sys.argv[1:])