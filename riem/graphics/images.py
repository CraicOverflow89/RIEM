from PIL import Image, ImageTk

class ImageLoader:

	# Constants
	data = {}

	def load(image):

		# Store Image
		if image not in ImageLoader.data:
			ImageLoader.data[image] = ImageTk.PhotoImage(Image.open("resources/images/%s.png" % image))

		# Return Image
		return ImageLoader.data[image]