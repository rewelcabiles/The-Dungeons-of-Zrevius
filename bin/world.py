import json
import random
import factory




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
				
	def set_entity_location(self, ent_id, target_room):
		self.WORLD['location'][ent_id]['room_id'] = target_room

	def add_to_inventory(self, ent_id, target_inventory):
		self.WORLD['inventory'][target_inventory]['items'].append(ent_id)