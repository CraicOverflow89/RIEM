from riem.library import FileSystem
from riem.version import __version__
from typing import List, Dict
import os, requests, sys

# Script Logic
def invoke(args: List[str]) -> None:

	# Command: Create
	def create(args: List[str]) -> None:

		# Project Name
		if len(args) == 0:
			print("ERROR: Must specify a project name!")
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

	# Command: Help
	def help() -> None:
		print("Commands")
		print("=" * 8)
		print("$ create [project name]        creates a new project at the current location")
		print("$ help                         displays all commands")
		print("$ version                      displays the current version")

	# Command: Version
	def version(args: List[str]) -> None:

		# Print Logo
		FileSystem.read_file("%s/resources/shell/logo.txt" % "/".join(__file__.split("/")[:-2])).each(lambda it: print(it))
		print("")

		# Current Version
		print("Current Version      %s " % __version__)

		# Latest Version
		response: str = requests.get(url = "https://raw.githubusercontent.com/CraicOverflow89/RIEM/master/riem/version.py")
		print("Latest Version       %s " % response.text.split("\"")[1])

	# Command Map
	commands: Dict[str, Callable] = {
		"create" : create,
		"help" : help,
		"version" : version
	}

	# Spacing
	print("")

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
			print("ERROR: Command %s not recognised!" % args[0])
			print("")
			help()

# Invoke Script
invoke(sys.argv[1:])