
class Command:
	def __init__(self, functions):
		self.functions = functions
		self.WORLD = self.functions.world.WORLD
		self.MenuTree = []

	def get_object_type(self, ent_id):
		inv_mask = self.functions.interface.create_dynamic_mask(['inventory'])
		wep_mask = self.functions.interface.create_dynamic_mask(['weapon'])
		dor_mask = self.functions.interface.create_dynamic_mask(['transition'])
		if((self.WORLD['mask'][ent_id] & inv_mask) == inv_mask):
			return "is_inventory"
		if((self.WORLD['mask'][ent_id] & wep_mask) == wep_mask):
			return "is_weapon"
		if((self.WORLD['mask'][ent_id] & dor_mask) == dor_mask):
			return "is_door"

	def look_weapon(self, ent_id):
		if self.WORLD['item'][ent_id]['rarity'] == 'common':
			print("Its a "+self.WORLD['descriptor'][ent_id]['name'])

		elif self.WORLD['item'][ent_id]['rarity'] == 'unique':
			wep_type = self.WORLD['weapon'][ent_id]['type']
			print("A unique "+wep_type+", well known  as "+self.WORLD['descriptor'][ent_id]['name'])


	def look_inventory(self, ent_id):
		if not self.WORLD['inventory'][ent_id]['items']:
			print("You see no items in it.")
		else:
			temp_dict = {}
			iterator  = 0
			print("You see: ")
			for things in self.WORLD['inventory'][ent_id]['items']:
				iterator += 1
				text = str(iterator)+" ) "+ " a "+self.WORLD['descriptor'][things]['name']
				temp_dict[str(iterator)] = ["look", text, things]
				#print("BF "+ text)
			self.MenuTree.append(temp_dict)

	def display_menu(self):
		try:
			for items in self.MenuTree[-1]:
				print(self.MenuTree[-1][items][1])
		except IndexError:
			pass

	def do(self):
		self.display_menu()

		command = input("Health: >>")

		if command == "look":
			self.look_inventory(self.functions.current_pos)
					
		if command in self.MenuTree[-1].keys():
			info   = self.MenuTree[-1][command]
			action = info[0]
			if action == "look":
				item_id = info[2]
				obj_type = self.get_object_type(item_id)
				if obj_type   == "is_inventory":
					self.look_inventory(item_id)
				elif obj_type == "is_weapon":
					self.look_weapon(item_id)

