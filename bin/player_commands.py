# TODO 
#
#
# !   If you're feeling bored. Separate out the input logic from the display logic :P 
#
# !!! Make player characters invisible from room look.
# TODO: Make it so that as you travel between rooms, you get a chance of being ambushed
# TODO: @Important Work in user commands like: View stats, Inventory Etc.
# Will use wisdom to discern.
# TODO: Combat mechanics now pls

class PlayerCommands():
	def __init__(self, world, message, pid):
		self.world = world
		self.WORLD = self.world.WORLD
		self.player_id = pid
		self.message = message
		self.surface_nodes = SurfaceNode(self)
		self.MenuTree = []

	def notified(self, message):
		pass

	def update(self):
		if not self.MenuTree:
			self.surface_nodes.look_at(self.world.get_location(self.player_id))
			self.MenuTree.append(self.surface_nodes.look_inventory(self.world.get_location(self.player_id)))
		self.MenuTree[-1].print_menu()
		user = input(":=======:>> ")
		self.do_surface(user)


	def do_surface(self, user):
		if user == "look":
			self.MenuTree.clear()
			self.surface_nodes.look_at(self.world.get_location(self.player_id))
			self.MenuTree.append(self.surface_nodes.look_inventory(self.world.get_location(self.player_id)))

		elif user == "inventory":
			self.MenuTree.append(self.surface_nodes.look_inventory(self.player_id))

		elif user == "equipment":
			self.MenuTree.append(self.surface_nodes.look_equipment(self.player_id))

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
				self.surface_nodes.look_at(info['data']['entity_id'])

			elif action_type == "drop":
				ent_id  = info['data']["entity_id"]
				message = {
					"type"   :"drop",
					"data":{"entity_id" : ent_id, "action_user" : self.player_id}
					}
				self.message.add_to_queue(message)
				self.MenuTree.clear() # Pops the interact Node
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

			elif action_type == "equip":
				requested_slot  = self.WORLD['equippable'][info['data']["entity_id"]]['slot']
				slot = info['data']['slot']

				if requested_slot == "dual_wield":
					slot = "dual_wield"

				elif requested_slot == "one_hand" and info['data']['slot'] == None:
					self.MenuTree.append(self.surface_nodes.one_hand_equip(info['data']["entity_id"]))
				
				if slot != None:
					message = {
						"type"   :"equip",
						"data":{"entity_id":info['data']["entity_id"], 
							"action_user":self.player_id,
							"slot": slot
						}
					}
					self.message.add_to_queue(message)
					self.MenuTree.clear()
					
			elif action_type == "unequip":
				message = {
					"type"   :"unequip",
					"data":{"entity_id":info['data']["entity_id"]}
				}
				self.message.add_to_queue(message)
				self.MenuTree.clear()
				self.MenuTree.append(self.surface_nodes.look_equipment(self.player_id))
	
class SurfaceNode():
	def __init__(self, commands):
		self.commands   = commands
		self.world      = self.commands.world
		self.WORLD      = self.commands.world.WORLD
		self.player_id  = commands.player_id

	def one_hand_equip(self, ent_id):
		new_node = MenuNode()
		new_node.set_header("Which slot do you want to equip it in?")
		new_node.add_new_option("equip", "Left Hand", {"entity_id":ent_id, "slot": "left_hand", "action_user":self.player_id})
		new_node.add_new_option("equip", "Right Hand", {"entity_id":ent_id, "slot": "right_hand", "action_user":self.player_id})
		return new_node

	def interact(self, ent_id):
		new_node = MenuNode()
		new_node.set_header("What do you want to do with "+ self.WORLD['descriptor'][ent_id]['name'] + "?")
		# Can be looked at?
		if self.world.has_components(ent_id, ["descriptor"]):
			new_node.add_new_option("look", "Look at", {"entity_id":ent_id})
		# Able to be picked up?
		if self.world.has_components(ent_id, ["item"]) and not self.world.in_container(ent_id, self.player_id):
			new_node.add_new_option("pick_up", "Pick Up", {"entity_id":ent_id, "action_user":self.player_id})
		#  Is inside the players Inventory and thus, can be dropped.
		if self.world.has_components(ent_id, ["item"]) and ent_id in self.WORLD['inventory'][self.player_id]['items']:
			new_node.add_new_option("drop", "Drop", {"entity_id":ent_id, "action_user":self.player_id})

		# Is Equipable, and is in player inventory
		if self.world.has_components(ent_id, ["equippable"]) and ent_id in self.WORLD['inventory'][self.player_id]['items']:
			new_node.add_new_option("equip", "Equip", {"entity_id":ent_id, "slot":None,"action_user":self.player_id})

		# Has something to identify?
		if self.world.has_components(ent_id, ["modifiers"]) or self.world.has_components(ent_id, ["buff_refill"]):
			new_node.add_new_option("identify", "Identify", {"entity_id":ent_id})

		# Is it a transition object? (AKA, a door or portal.. etc)
		if self.world.has_components(ent_id, ["transition"]):
			new_node.add_new_option("go", "Go Through", {"entity_id":ent_id})

		# Is a container?
		if self.world.has_components(ent_id, ["container"]):
			new_node.add_new_option("open", "Open container", {"entity_id":ent_id})

		# Is currently equipped?
		print(self.world.equipped_by(ent_id))
		print(self.player_id)
		if self.world.has_components(ent_id, ["equippable"]) and self.world.equipped_by(ent_id) == self.player_id:
			new_node.add_new_option("unequip", "Unequip", {"entity_id":ent_id, "action_user": self.player_id})

		return new_node

	def look_at(self, ent_id):
		print("You look at the " + self.WORLD['descriptor'][ent_id]['name'])
		print(self.WORLD['descriptor'][ent_id]['desc'])

	def look_inventory(self, ent_id):
		look_node = MenuNode() 
		if ent_id != self.player_id:
			look_node.set_header("You look through the " + self.WORLD['descriptor'][ent_id]['name'] + " and see...")
		else: 
			look_node.set_header("You look through your bags and see...")

		for things in self.WORLD['inventory'][ent_id]['items']:
			if things != self.player_id:
				text = self.WORLD['descriptor'][things]['name']
				look_node.add_new_option("interact", text, {"entity_id":things})
		return look_node

	def look_equipment(self, ent_id):
		equipment_node = MenuNode()
		if ent_id != self.player_id:
			pass
		else:
			equipment_node.set_header("You check your equipment.")

		equipment = self.WORLD['equipment'][ent_id]

		for slots in equipment:
			
			if equipment[slots] != None:
				text = slots + '    ->     ' + self.WORLD['descriptor'][equipment[slots]]['name']
				equipment_node.add_new_option("interact", text, {"entity_id":equipment[slots]})
			else:
				text = slots + '    ->      None' 
				equipment_node.add_new_option("interact", text, {"entity_id":equipment[slots]})

		return equipment_node

class MenuNode():
	def __init__(self):
		self.current_options = 1
		self.header = ""
		self.options = {}  # Type, data, Text
		self.options[str(self.current_options)] = {
			"type": "back", "data": {}, "text": "Back"}

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
