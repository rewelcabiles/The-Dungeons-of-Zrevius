
class Command:
	def __init__(self, functions):
		self.functions = functions
		self.WORLD = self.functions.world.WORLD
		self.menu = {}

	def advanced_look(self, ent_id):
		inv_mask = self.functions.interface.create_dynamic_mask(['inventory'])
		# Has an inventory
		if((self.WORLD['mask'][ent_id] & inv_mask) == inv_mask): 
			self.look_in_inventory(ent_id)
		# Doesnt have an inventory.
		else:
			print("Its a "+self.WORLD['descriptor'][ent_id]['name'])
			print(self.WORLD['descriptor'][ent_id]['desc'])


	def look_in_inventory(self, ent_id):
		if not self.WORLD['inventory'][ent_id]['items']:
			print("You see no items in it.")
		else:
			temp_list = []
			iterator  = 0
			print("You see: ")
			for things in self.WORLD['inventory'][ent_id]['items']:
				iterator += 1
				self.menu[str(iterator)] = things
				print(str(iterator)+" ) "+ " a "+self.WORLD['descriptor'][things]['name'])


	def do(self, command):

		if command == "look":
			found = False
			self.look_in_inventory(self.functions.current_pos)
					
		if command in self.menu.keys():
			self.advanced_look(self.menu[command])
