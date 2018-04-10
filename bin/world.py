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
		self.entity_id_max = 2500
		self.factory = factory.Factory(self)
		self.modifiers = Modifier_Helper(self)

	def assign_entity_id(self):
		while True:
			entity_id = random.randint(1, self.entity_id_max)
			if entity_id not in list(self.WORLD['mask'].keys()):
				self.WORLD['mask'][entity_id] = self.COMPS['none']
				return entity_id

	def create_dynamic_mask(self, component_list):
		temp_mask = 0
		for comps in component_list:
			temp_mask |= self.COMPS[comps]
		return temp_mask		

	def has_components(self, ent_id, component_list):
		temp_mask = self.create_dynamic_mask(component_list)
		if((self.WORLD['mask'][ent_id] & temp_mask) == temp_mask):
			return True

	def destroy_entity(self, entity_id):
		for components in self.WORLD.keys():
			if entity_id in self.WORLD[components].keys():
				del self.WORLD[components][entity_id]

	def set_entity_location(self, ent_id, target_room):
		self.WORLD['location'][ent_id]['container_id'] = target_room
		self.WORLD['inventory'][target_room]['items'].append(ent_id)

	def del_from_inventory(self, ent_id, target_inventory):
		self.WORLD['inventory'][target_inventory]['items'].remove(ent_id)

	def add_to_inventory(self, ent_id, target_inventory):
		self.WORLD['inventory'][target_inventory]['items'].append(ent_id)
		self.WORLD['location'][ent_id]['container_id'] = target_inventory
		
	def move_to_inventory(self, ent_id, new_inv):
		old_inv = self.WORLD['location'][ent_id]['container_id']
		self.WORLD['inventory'][new_inv]['items'].append(ent_id)
		self.WORLD['inventory'][old_inv]['items'].remove(ent_id)
		self.WORLD['location' ][ent_id ]['container_id'] = new_inv

	def get_location(self, ent_id):
		return self.WORLD['location'][ent_id]['container_id']

	def in_container(self, ent_id, container):
		return container == self.WORLD['location'][ent_id]['container_id']

	def get_equipment_slot(self, entity, slot):
		return self.WORLD['equipment'][entity][slot]

	def get_slot_type(self, ent_id):
		return self.WORLD['equippable'][ent_id]['slot']

	def equipped_by(self, ent_id):
		try:
			return self.WORLD['equippable'][ent_id]['equipped_by']
		except:
			return False

class Modifier_Helper:
	def __init__(self, world):
		self.world 		   = world
		self.WORLD		   = world.WORLD

	def get_modified_stat(self, ent_id, stat):
		stat_value = self.WORLD['stats'][ent_id][stat]
		base = self.get_base_modifiers(ent_id)
		add = self.get_add_modifiers(ent_id)
		mult = self.get_mult_modifiers(ent_id)
		
		# Apply Base Multiplicative Modifiers
		percent_amount = 0
		for mod_ids in base:
			mod = self.WORLD['modifier'][mod_ids]
			if mod['key'] != stat:
				continue
			percent_amount += mod['value']
		percentage = percent_amount / 100
		new_value  = stat_value * percentage
		stat_value += new_value

		# Add Additive Modifiers
		for mod_ids in add:
			mod = self.WORLD['modifier'][mod_ids]
			if mod['key'] != stat:
				continue
					
			stat_value += mod['value']

		# Add Total Multiplicative Modifiers:
		percent_amount = 0
		for mod_ids in mult:
			mod = self.WORLD['modifier'][mod_ids]
			if mod['key'] != stat:
				continue
			print("Mult_Modifiers Found")				
			percent_amount += mod['value']

		percentage = percent_amount / 100
		new_value  = stat_value * percentage
		stat_value += new_value
	
		return stat_value

	def get_modified_amount(self, ent_id, stat):
		final_amount  = self.get_modified_stat(ent_id, stat)
		current_amount= self.WORLD['stats'][ent_id][stat]
		return final_amount - current_amount

	def get_base_modifiers(self, ent_id):
		base_mods = []
		for mod_id in self.WORLD['has_modifiers'][ent_id]:
			if self.WORLD['modifier'][mod_id]['type'] == "base":
				base_mods.append(mod_id)
		return base_mods

	def get_mult_modifiers(self, ent_id):
		mult_mods = []
		for mod_id in self.WORLD['has_modifiers'][ent_id]:
			if self.WORLD['modifier'][mod_id]['type'] == "multiplicative":
				mult_mods.append(mod_id)
		return mult_mods

	def get_add_modifiers(self, ent_id):
		add_mods = []
		for mod_id in self.WORLD['has_modifiers'][ent_id]:
			if self.WORLD['modifier'][mod_id]['type'] == "additive":
				add_mods.append(mod_id)
		return add_mods