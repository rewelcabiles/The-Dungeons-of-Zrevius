
class PlayerCommands():
	def __init__(self, world, message):
		self.world = world
		self.WORLD = self.world.WORLD
		self.message = message
		self.MenuTree = []
	
	def set_player_id(self, pid):
		self.player_id = pid
		self.surface_nodes = SurfaceNode(self)
		self.inventory_nodes = InventoryNode(self)

	def do(self):
		if self.MenuTree:
			self.MenuTree[-1].print_menu()
		user = input("============: >> ")

		if user == "look":
			self.MenuTree.clear()
			self.look_at(self.player_pos)
			self.look_inventory(self.player_pos)

		elif command == "inventory":
			self.MenuTree.append(self.InventoryNode.look_inventory(self.player))

	def look_at(self, ent_id):
		print("You look at the " + self.WORLD['descriptor'][ent_id]['name'])
		print(self.WORLD['descriptor'][ent_id]['desc'])


class SurfaceNode():
	def __init__(self, commands):
		self.commands = commands
		self.player   = commands.player_id

	def look_door(self, ent_id):
		door_node = MenuNode()
		door_node.set_header(
			"Go through the "
			+ self.WORLD['descriptor'][ent_id]['name'] 
			+ "?"
			)
		door_node.add_new_option("go", "Go through", ent_id)
		return door_node

	def look_inventory(self, ent_id):
		look_node = MenuNode() 
		look_node.set_context("surface")
		look_node.set_header(
			"You look through the " 
			+ self.WORLD['descriptor'][ent_id]['name'] 
			+ " and see..."
			)
		for things in self.WORLD['inventory'][ent_id]['items']:
			text = self.WORLD['descriptor'][things]['name']
			look_node.add_new_option("look", text, things)
		return look_node

class InventoryNode():
	def __init__(self, commands):
		self.commands = commands
		self.player   = commands.player_id
	
	def pick_up(self, ent_id):
		print(self.commands.WORLD['descriptor'][ent_id]['name'] + ' goes into your inventory.')
		self.commands.world.move_to_inventory(ent_id, self.player)

	def drop(self, ent_id):
		print("You drop "+self.commands.WORLD['descriptor'][ent_id]['name']+". Down it goes!")
		player_loc = self.commands.WORLD['location'][self.player]['container_id']
		self.commands.world.move_to_inventory(ent_id, player_loc)

	def look_inventory(self, ent_id):
		look_node = MenuNode()
		look_node.set_context("inventory")
		look_node.set_header("You look through your bags and see...")
		for item in self.commands.WORLD['inventory'][ent_id]['items']:
			text = self.commands.WORLD['descriptor'][item]['name']
			look_node.add_new_option("look", text, item)
		return look_node


	def look_weapon(self, ent_id):
		self.commands.look_at(ent_id)
		print("===============\nStatistics : ")
		self.commands.display_item_modifiers(ent_id)
		print("===============")

		choice_node = MenuNode()
		choice_node.set_header("What do you want to do with it?")
		choice_node.add_new_option("look", "Look", ent_id)
		choice_node.add_new_option("equip","Equip",ent_id)
		choice_node.add_new_option("drop", "Drop", ent_id)

		return choice_node


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
