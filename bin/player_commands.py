
class PlayerCommands():
	def __init__(self, world):
		self.world = world
		self.WORLD = self.world.WORLD





class MenuNode():

	def __init__(self):
		self.current_options = 1
		self.context = ""
		self.header = ""
		self.options = {}  # Type, Pointer, Text
		self.options[str(self.current_options)] = {
			"type": "back", "pointer": None, "text": "Back"}

	def set_context(self, cont):
		self.context = cont

	def set_header(self, head):
		self.header = head

	def print_menu(self):
		try:
			print(self.header + "\n")
			for index in self.options:
				item = self.options[index]
				print(index + " ) " + item['text'])
		except IndexError:
			print("This Menu Is Empty!")

	def add_new_option(self, option_type, text, pointer=None):
		self.options[str(self.current_options)] = {
			"type": option_type, "pointer": pointer, "text": text}
		self.current_options += 1

		# Moves Back option to back of menu list.
		try:
			del self.options[-2]
			self.options[str(self.current_options)] = {
				"type": "back", "pointer": None, "text": "Back"}
		except KeyError:
			self.options[str(self.current_options)] = {
				"type": "back", "pointer": None, "text": "Back"}

	def get_action(self, option_index):
		if self.is_an_option(option_index):
			return self.options[option_index][0]
		else:
			return None

	def is_an_option(self, option_index):
		if option_index in self.options.keys():
			return True
		else:
			return False
