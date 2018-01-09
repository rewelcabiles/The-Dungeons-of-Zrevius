import random

# TODO: Make it so that as you travel between rooms, you get a chance of being ambushed
# TODO: @Important Work in user commands like: View stats, Inventory Etc.
# Will use wisdom to discern.
# TODO: Combat mechanics now pls

class Command:
	def __init__(self, functions):
		self.functions = functions
		self.world     = self.functions.world
		self.WORLD = self.world.WORLD
		self.player = self.functions.player_id
		self.player_pos = self.WORLD['location'][self.player]['container_id']
		self.MenuTree = []

	def look_at(self, ent_id):
		print("You look at the " + self.WORLD['descriptor'][ent_id]['name'])
		print(self.WORLD['descriptor'][ent_id]['desc'])
	
	def look_weapon(self, ent_id):
		print("You look at " + self.WORLD['descriptor'][ent_id]['name'])
		print(self.WORLD['descriptor'][ent_id]['desc'])
		print("===============\nStatistics : ")
		self.display_item_modifiers(ent_id)
		print("===============")

		new_node = MenuNode()
		new_node.set_header("What do you want to do with it? ")
		new_node.add_new_option("pick_up", "Pick Up", ent_id)

		self.MenuTree.append(new_node)

	def look_door(self, ent_id):
		new_node = MenuNode()
		new_node.set_header("Go through the " +
							self.WORLD['descriptor'][ent_id]['name'] + "?")
		new_node.add_new_option("go", "Go through", ent_id)
		self.MenuTree.append(new_node)

	# TODO: Create an Inventory component Maybe
	# TODO: Depending on wisdom modifier, make it so that the stats hown
	# Are only accurate if the wisdom check is high enough.

	def display_ent_stats(self, ent_id):
		ent_stats = self.WORLD['stats'][ent_id]
		if ent_stats:
			for stat in ent_stats.keys():
				if stat != 'exp': # Theres no need to show exp
					text = stat.capitalize() + " : " + str(ent_stats[stat])
					print(text)

	def display_item_modifiers(self, ent_id):
		ent_mod  = self.WORLD['modifiers'][ent_id]
		if ent_mod:
			for mods in ent_mod.keys():
				text = mods.capitalize() + " : " + str(ent_mod[mods])
				print(text)

	def look_inventory(self, ent_id):
		new_node = MenuNode()
		container_type = self.WORLD['descriptor'][ent_id]['name']
		if not self.WORLD['inventory'][ent_id]['items']:
			if ent_id != self.player:																				## TODO: This feels hacky. Fix in future
				new_node.set_header("You look through the " + container_type + " and see nothing of use.")			##
			else:																									##
				new_node.set_header("You look through the your bags and see nothing.")	
		else:
			new_node.set_context(self.world.get_object_type(ent_id))
			if ent_id != self.player:
				new_node.set_header("You look through the " + container_type + " and see...")
			else:
				new_node.set_header("You look through the your bags and see...")

			for things in self.WORLD['inventory'][ent_id]['items']:
				if self.world.get_object_type(things) == "is_door":
					text = self.WORLD['descriptor'][things]['name'] + " " + str(self.WORLD['transition'][things]['target'])
				else:
					text = self.WORLD['descriptor'][things]['name']
				new_node.add_new_option("look", text, things)

		self.MenuTree.append(new_node)


	# TODO: separate the logic to another class? idk
	def do(self):
		if self.MenuTree:
			self.MenuTree[-1].print_menu()

		command = input("============: >> ")

		if command == "look":
			self.MenuTree.clear()
			self.look_at(self.player_pos)
			self.look_inventory(self.player_pos)

		elif command == "inventory":
			self.look_inventory(self.player)

		elif command == "stats":
			print("===============\nStatistics : ")
			self.display_ent_stats(self.player)
			print("===============")

		elif self.MenuTree: # Checks if MenuTree is empty. If not: 
			if command in self.MenuTree[-1].options.keys():
				latest_node = self.MenuTree[-1]
				info = latest_node.options[command]
				action = info['type']

				print(action)

				if action == "back":  # Go Back a Menu
					self.MenuTree.pop()

				elif action == "go":   # Use A Door / Transition Object
					next_room = info['pointer']
					self.player_pos = self.WORLD['transition'][next_room]['target']
					print("You head through the " + self.WORLD['descriptor'][next_room]['name'] +
						  " and into a " + self.WORLD['descriptor'][self.player_pos]['name'])
					self.MenuTree.clear()

				elif action == "pick_up":
					item_id = info['pointer']
					
					print("You add the "
						+ self.WORLD['descriptor'][item_id]['name']
						+ ' to your inventory.'
						)
					self.world.move_to_inventory(item_id, self.player)
					self.MenuTree.clear()

				elif action == "look":  # Look at / interact with something
					item_id = info['pointer']
					obj_type = self.world.get_object_type(item_id)
					if obj_type == "is_inventory":
						self.look_at(item_id)
						self.look_inventory(item_id)
					elif obj_type == "is_weapon":
						self.look_weapon(item_id)
					elif obj_type == "is_door":
						self.look_at(item_id)
						self.look_door(item_id)
					else:
						self.look_at(item_id)
				else:
					print("You stand confused as to what you want to do.")
			else: 
				print("You stand confused as to what you want to do.")

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
