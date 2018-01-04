
class Command:
	def __init__(self, functions):
		self.functions = functions
		self.WORLD = self.functions.world.WORLD
		self.MenuTree = []

	def get_object_type(self, ent_id):
		inv_mask = self.functions.interface.create_dynamic_mask(['inventory'])
		wep_mask = self.functions.interface.create_dynamic_mask(['weapon'])
		dor_mask = self.functions.interface.create_dynamic_mask(['transition'])
		isr_mask = self.functions.interface.create_dynamic_mask(['isroom'])
		if((self.WORLD['mask'][ent_id] & inv_mask) == inv_mask):
			return "is_inventory"
		if((self.WORLD['mask'][ent_id] & wep_mask) == wep_mask):
			return "is_weapon"
		if((self.WORLD['mask'][ent_id] & dor_mask) == dor_mask):
			return "is_door"
		if((self.WORLD['mask'][ent_id] & isr_mask) == isr_mask):
			return "is_room"			

	def look_weapon(self, ent_id):
		if self.WORLD['item'][ent_id]['rarity'] == 'common':
			print("Its a "+self.WORLD['descriptor'][ent_id]['name'])

		elif self.WORLD['item'][ent_id]['rarity'] == 'unique':
			wep_type = self.WORLD['weapon'][ent_id]['type']
			print("A unique "+wep_type+", well known  as "+self.WORLD['descriptor'][ent_id]['name'])


	def look_inventory(self, ent_id):
		print("You look around the "+self.WORLD['descriptor'][ent_id]['name'])
		print(self.WORLD['descriptor'][ent_id]['desc'])
		container_type = self.WORLD['descriptor'][ent_id]['name']
		if not self.WORLD['inventory'][ent_id]['items']:
			print("You look through the "+container_type+" and see nothing of use.")
		else:
			new_node  = MenuNode()
			print("You look through the "+container_type+" and see...")
			for things in self.WORLD['inventory'][ent_id]['items']:
				text = self.WORLD['descriptor'][things]['name']
				new_node.add_new_option("look", text, things)
			self.MenuTree.append(new_node)

	def display_menu(self):
		try:
			for items in self.MenuTree[-1]:
				print(self.MenuTree[-1][items][1])
		except IndexError:
			pass

	def do(self):
		# self.display_menu()
		try:
			self.MenuTree[-1].print_menu()
		except IndexError:
			pass

		command = input("Health: >> ")

		if command == "look":
			self.look_inventory(self.functions.current_pos)
		
		try:
			if command in self.MenuTree[-1].options.keys():
				latest_node = self.MenuTree[-1]
				info   = latest_node.options[command]
				action = info['type']
				if action == "back":
					self.MenuTree.pop()

				if action == "look":
					item_id = info['pointer']
					obj_type = self.get_object_type(item_id)
					if obj_type   == "is_inventory":
						self.look_inventory(item_id)
					elif obj_type == "is_weapon":
						self.look_weapon(item_id)
					elif obj_type == "is_room":
						pass
		except IndexError:
			pass


class MenuNode():

	def __init__(self):
		self.current_options = 1
		self.options         = {} # Type, Pointer, Text
		#self.add_new_option("back", "Back")

	def print_menu(self):
		try:
			for index in self.options:
				item = self.options[index]
				print(index+" ) "+item['text'])
		except IndexError:
			print("This Menu Is Empty!")

	def add_new_option(self,option_type, text, pointer = None):
		self.options[str(self.current_options)] = {"type": option_type, "pointer": pointer, "text": text}
		self.current_options += 1

		# Moves Back option to back of menu list.
		try:
			del self.options[-2]
			self.options[str(self.current_options)] = {"type": "back", "pointer": None, "text": "Back"}
		except KeyError:
			self.options[str(self.current_options)] = {"type": "back", "pointer": None, "text": "Back"}

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


class MenuTree():
	
	def __init__(self):
		self.Tree = []

	def create_current_node(self):
		self.new_node = {}

	def add_options(self):
		pass