import os, sys

# Script Logic
def invoke(args):

	# Command: Help
	def help():
		print("Help")
		# NOTE: list commands and args
		#       commands.each {get metadata/annotations of it}

	# Command: Create
	def create(args):

		# Project Name
		if len(args) == 0:
			print("Please specify a project name!")
			sys.exit(-1)
		else:
			project_name = args[0]

		# Create Directories
		os.mkdir(os.path.join(os.getcwd(), project_name))
		os.mkdir(os.path.join(os.getcwd(), project_name, "resources"))
		os.mkdir(os.path.join(os.getcwd(), project_name, "resources", "images"))
		os.mkdir(os.path.join(os.getcwd(), project_name, "resources", "sounds"))
		os.mkdir(os.path.join(os.getcwd(), project_name, "states"))

		# Create Files
		fs = open(os.path.join(os.getcwd(), project_name, "app.py"), "x")
		fs.write("from riem.core import Application 1")
		fs.write("")
		fs.write("from riem.core import Application 2")
		fs.close()

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