# TODO: Start filling out thte commands for the different
#  		context nodes


class PlayerCommands():
	def __init__(self, world, message, pid):
		self.world = world
		self.WORLD = self.world.WORLD
		self.player_id = pid
		self.message = message
		self.surface_nodes = SurfaceNode(self)
		self.inventory_nodes = InventoryNode(self)
		self.MenuTree = []

	def update(self):
		if not self.MenuTree:
			self.surface_nodes.look_at(self.world.get_location(self.player_id))
			self.MenuTree.append(self.surface_nodes.look_inventory(self.world.get_location(self.player_id)))
		top_node = self.MenuTree[-1]
		top_node.print_menu()
		
		user = input(":=======:>> ")
		self.do_surface(user)


	def do_surface(self, user):
		if user == "look":
			self.MenuTree.clear()
			self.surface_nodes.look_at(self.world.get_location(self.player_id))
			self.MenuTree.append(self.surface_nodes.look_inventory(self.world.get_location(self.player_id)))

		elif user == "inventory":
			self.MenuTree.append(self.surface_nodes.look_inventory(self.player_id))

		elif user in self.MenuTree[-1].options.keys():
			latest_node = self.MenuTree[-1]
			info = latest_node.options[user]
			action_type = info['type']

			if action_type == "back":
				self.MenuTree.pop()

			elif action_type == "interact":
				entity_id = info['data']["entity_id"]
				obj_type= self.world.get_object_type(entity_id)
				self.MenuTree.append(self.surface_nodes.interact(entity_id))

			elif action_type == "look":
				self.surface_nodes.look_at(info['data'])

			elif action_type == "drop":
				ent_id  = info['data']["entity_id"]
				message = {
					"type"   :"drop",
					"data":{"entity_id" : ent_id, "action_user" : self.player_id}
					}
				self.message.add_to_queue(message)
				self.MenuTree.pop() # Pops the interact Node
				self.MenuTree.pop() # Pops the Old container Node
				self.MenuTree.append(self.surface_nodes.look_inventory(self.world.get_location(info['data']["entity_id"]))) # Appends the updated node
				print("You drop "+self.WORLD['descriptor'][ent_id]['name']+". Down it goes!")

			elif action_type == "pick_up":
				ent_id  = info['data']["entity_id"]
				message = {
					"type"   :"pick_up",
					"data":{"entity_id" : ent_id, "action_user" : self.player_id}
					}
				self.message.add_to_queue(message)
				self.MenuTree.pop() # Pops the interact Node
				self.MenuTree.pop() # Pops the Old container Node
				self.MenuTree.append(self.surface_nodes.look_inventory(self.world.get_location(info['data']["entity_id"]))) # Appends the updated node
				print(self.WORLD['descriptor'][ent_id]['name'] + ' goes into your inventory.')

			elif action_type == "open":
				entity_id = info['data']["entity_id"]
				self.MenuTree.append(self.surface_nodes.look_inventory(entity_id))

			elif action_type == "go":
				next_room = self.WORLD['transition'][info['data']["entity_id"]]['target']
				message = {
					"type"   :"move",
					"data":{"room_target":next_room, "action_user":self.player_id}
				}
				self.MenuTree.clear()
				self.message.add_to_queue(message)

	
class SurfaceNode():
	def __init__(self, commands):
		self.commands   = commands
		self.world      = self.commands.world
		self.WORLD      = self.commands.world.WORLD
		self.player_id  = commands.player_id

	def interact(self, ent_id):
		new_node = MenuNode()
		new_node.set_context("surface")
		new_node.set_header("What do you want to do with "
			+ self.WORLD['descriptor'][ent_id]['name'] + "?")

		# Can be looked at?
		if self.world.is_object_type(ent_id, ["descriptor"]):
			print("DEBUG: Can be looked at.")
			new_node.add_new_option("look", "Look at", {"entity_id":ent_id})
		# Able to be picked up?
		if self.world.is_object_type(ent_id, ["item"]):
			print("DEBUG: Can be picked up.")
			new_node.add_new_option("pick_up", "Pick Up", {"entity_id":ent_id, "action_user":self.player_id})

		if self.world.is_object_type(ent_id, ["item"]) and self.world.in_container(ent_id, self.player_id):
			print("DEBUG: Is inside the players Inventory and thus, can be dropped.")
			new_node.add_new_option("drop", "Drop", {"entity_id":ent_id, "action_user":self.player_id})

		# Has something to identify?
		if self.world.is_object_type(ent_id, ["modifiers"]) or self.world.is_object_type(ent_id, ["buff_refill"]):
			print("DEBUG: Can be indentified.")
			new_node.add_new_option("identify", "Identify", {"entity_id":ent_id})

		# Is it a transition object? (AKA, a door or portal.. etc)
		if self.world.is_object_type(ent_id, ["transition"]):
			print("DEBUG: Can go through.")
			new_node.add_new_option("go", "Go Through", {"entity_id":ent_id})

		# Is an inventory?
		if self.world.is_object_type(ent_id, ["inventory"]):
			print("DEBUG: Is an Inventory.")
			new_node.add_new_option("open", "Open container", {"entity_id":ent_id})

		return new_node

	def look_at(self, ent_id):
		print("You look at the " + self.WORLD['descriptor'][ent_id]['name'])
		print(self.WORLD['descriptor'][ent_id]['desc'])

	def look_inventory(self, ent_id):
		look_node = MenuNode() 
		look_node.set_context("surface")
		if ent_id != self.player_id:
			look_node.set_header("You look through the " + self.WORLD['descriptor'][ent_id]['name'] + " and see...")
		else: 
			look_node.set_header("You look through your bags and see...")

		for things in self.WORLD['inventory'][ent_id]['items']:
			text = self.WORLD['descriptor'][things]['name']
			look_node.add_new_option("interact", text, {"entity_id":things})
		return look_node


class InventoryNode():
	def __init__(self, commands):
		self.commands   = commands
		self.world      = self.commands.world
		self.WORLD      = self.commands.world.WORLD
		self.player     = commands.player_id

	def look_weapon(self, ent_id):
		self.commands.look_at(ent_id)
		print("===============\nStatistics : ")
		self.commands.display_item_modifiers(ent_id)
		print("===============")

		choice_node = MenuNode()
		choice_node.set_header("What do you want to do with it?")
		choice_node.add_new_option("look", "Look", {"entity_id":ent_id})
		choice_node.add_new_option("equip","Equip",{"entity_id":ent_id})
		choice_node.add_new_option("drop", "Drop", {"entity_id":ent_id})

		return choice_node


class MenuNode():

	def __init__(self):
		self.current_options = 1
		self.context = ""
		self.header = ""
		self.options = {}  # Type, data, Text
		self.options[str(self.current_options)] = {
			"type": "back", "data": {}, "text": "Back"}

	def set_context(self, cont):
		self.context = cont

	def get_context(self):
		return self.context

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

	def add_new_option(self, option_type, text, data={}):
		self.options[str(self.current_options)] = {
			"type": option_type, "data": data, "text": text}
		self.current_options += 1

		# Moves Back option to back of menu list.
		try:
			del self.options[-2]
			self.options[str(self.current_options)] = {
				"type": "back", "data": {}, "text": "Back"}
		except KeyError:
			self.options[str(self.current_options)] = {
				"type": "back", "data": {}, "text": "Back"}

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
