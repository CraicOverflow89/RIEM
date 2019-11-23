from riem.library import FileSystem
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
		cwd = os.getcwd()
		project_name_lowercase = project_name.lower()
		os.mkdir(os.path.join(cwd, project_name))
		os.mkdir(os.path.join(cwd, project_name, project_name_lowercase))
		os.mkdir(os.path.join(cwd, project_name, project_name_lowercase, "resources"))
		os.mkdir(os.path.join(cwd, project_name, project_name_lowercase, "resources", "images"))
		os.mkdir(os.path.join(cwd, project_name, project_name_lowercase, "resources", "sounds"))
		os.mkdir(os.path.join(cwd, project_name, project_name_lowercase, "states"))

		# App File
		content_app = "".join(FileSystem.read_file("%s/resources/skeleton/app" % "/".join(__file__.split("/")[:-2])))
		content_app = content_app.replace("[project_name]", project_name)
		content_app = content_app.replace("[project_name_lower]", project_name_lowercase)
		FileSystem.write_file(os.path.join(cwd, project_name, project_name_lowercase, "app.py"), content_app)

		# Done
		print("Created the % project!" % project_name)

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