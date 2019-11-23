from setuptools import setup

# Load Version
exec(open("riem/version.py").read())

# Create Module
setup(
    author = "James Storer",
    author_email = "craic.overflow@hotmail.com",
    description = "Python framework for application development on Raspberry Pi.",
    keywords = ["RaspberryPi", "framework", "tkinter"],
    license = "MIT",
    packages = ["riem"],
    name = "riem",
    url = "https://github.com/CraicOverflow89/RIEM",
    version = __version__
)