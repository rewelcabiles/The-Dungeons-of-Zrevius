import json
import random
import factory

# TODO: equip_item(self, ent_id, player_id)

class World():

	def __init__(self):
		#Loads the files that contains all components
		with open ('data/components.json') as component_files:
		   components = json.load(component_files)
		self.WORLD = {}
		self.COMPS = {}
		self.COMPS['none'] = 1 << 0
		iterator = 1
		for key in components:
			self.WORLD[key] = {}
			self.COMPS[key] = 1 << iterator
			iterator += 1
		self.entity_id_max = 1500
		self.factory = factory.Factory(self)

	def assign_entity_id(self):
		while True:
			entity_id = random.randint(1, self.entity_id_max)
			if entity_id not in list(self.WORLD['mask'].keys()):
				self.WORLD['mask'][entity_id] = self.COMPS['none']
				return entity_id


	def destroy_entity(self, entity_id):
		for components in self.WORLD.keys():
			if ent_id in self.WORLD[components].keys():
				del self.WORLD[components][ent_id]

	def equip_item(self, equipment_id, character_id, slot):
		equipment_slot = self.WORLD['equippable'][equipment_id]['slot']
		if slot == "dual_hand":
			self.WORLD['equipment'][character_id]['left_hand'] = equipment_id
			self.WORLD['equipment'][character_id]['right_hand'] = equipment_id

		elif slot == "left_hand":
			self.WORLD['equipment'][character_id]['left_hand'] = equipment_id

		elif slot == "right_hand":
			self.WORLD['equipment'][character_id]['right_hand'] = equipment_id

		elif slot == "helmet_armor":
			self.WORLD['equipment'][character_id]['helmet_armor'] = equipment_id

		elif slot == "chest_armor":
			self.WORLD['equipment'][character_id]['chest_armor'] = equipment_id

		elif slot == "legs_armour":
			self.WORLD['equipment'][character_id]['legs_armour'] = equipment_id		

		elif slot == "ring01":
			self.WORLD['equipment'][character_id]['ring01'] = equipment_id		

		elif slot == "ring02":
			self.WORLD['equipment'][character_id]['ring02'] = equipment_id		
			
	def set_entity_location(self, ent_id, target_room):
		self.WORLD['location'][ent_id]['container_id'] = target_room

	def del_from_inventory(self, ent_id, target_inventory):
		del self.WORLD['inventory'][target_inventory]['items'][ent_id]

	def add_to_inventory(self, ent_id, target_inventory):
		self.WORLD['inventory'][target_inventory]['items'].append(ent_id)

	def move_to_inventory(self, ent_id, old_inv, new_inv):
		self.WORLD['inventory'][new_inv]['items'].append(ent_id)
		del self.WORLD['inventory'][old_inv]['items'][ent_id]