import random
import json
import copy

# Bridges the gap between the information in the json files, and the dungeon creator.
# Loads json files, and uses the data to create objects for the dungeon.

class Factory():

	def __init__(self,WORLD):
		self.world = WORLD
		self.WORLD = self.world.WORLD
		with open('data/archetype.json') as data_file:
			self.archetypes  = json.load(data_file)
		with open('data/components.json') as component_files:
			self.components  = json.load(component_files)
		with open('data/descriptors.json') as descriptor_files:
			self.descriptors = json.load(descriptor_files)
		with open('data/entity_stats.json') as stat_files:
			self.stats = json.load(stat_files)

	def create_from_archetype(self,ent_id, archetype_name):
		for component in list(self.archetypes[archetype_name].keys()):
			if self.archetypes[archetype_name][component] != "None":
				self.WORLD[component][ent_id] = copy.deepcopy(self.archetypes[archetype_name][component])
			else:
				self.WORLD[component][ent_id] = copy.deepcopy(self.components[component])
			self.WORLD['mask'][ent_id] |= self.world.COMPS[component]


	def create_components(self, comp, ent_id):
		self.WORLD[comp][ent_id] = copy.deepcopy(self.components[comp])
		self.WORLD['mask'][ent_id] |= self.world.COMPS[comp]


	def lorify(self, ent_id):
		monster_mask   = (self.world.COMPS['monster'])
		weapon_mask    = (self.world.COMPS['weapon'])
		isroom_mask    = (self.world.COMPS['isroom'])
		door_mask  	   = (self.world.COMPS['transition'])
		inventory_mask = (self.world.COMPS['inventory'])
		refill_mask    = (self.world.COMPS['buff_refill'] | self.world.COMPS['consumable'])

		if (self.WORLD['mask'][ent_id] & door_mask) == door_mask:
			desc = random.choice(self.descriptors['doors'])
			self.WORLD['descriptor'][ent_id]['name'] = desc['name']
			self.WORLD['descriptor'][ent_id]['desc'] = desc['desc']

		elif (self.WORLD['mask'][ent_id] & isroom_mask) == isroom_mask:
			desc = random.choice(self.descriptors['rooms'])
			self.WORLD['descriptor'][ent_id]['name'] = desc['name']
			self.WORLD['descriptor'][ent_id]['desc'] = desc['desc']

		elif (self.WORLD['mask'][ent_id] & monster_mask) == monster_mask:
			monster_type = self.WORLD['monster'][ent_id]['type']
			self.WORLD['descriptor'][ent_id]['name'] = random.choice(self.descriptors['names']['monsters'][monster_type])

		elif (self.WORLD['mask'][ent_id] & weapon_mask) == weapon_mask:
			weapon_type = self.WORLD['weapon'][ent_id]['type']
			if random.randrange(1,100) <= 10:
				rarity = 'unique'
			else:
				rarity = 'common'
			self.WORLD['descriptor'][ent_id]['name'] = random.choice(self.descriptors['names']['objects'][weapon_type][rarity])
			self.WORLD['descriptor'][ent_id]['desc'] = "A "+rarity+" "+ weapon_type
			self.WORLD['item'][ent_id]['rarity']     = rarity

		elif (self.WORLD['mask'][ent_id] & inventory_mask) == inventory_mask:
			self.WORLD['descriptor'][ent_id] = random.choice(self.descriptors['containers'])

		elif (self.WORLD['mask'][ent_id] & refill_mask) == refill_mask:
			if self.WORLD['consumable'][ent_id]['size'] == "small":
				self.WORLD['descriptor'][ent_id] = random.choice(self.descriptors['small_food'])

	def room_creator(self,x ,y):
		ent_id = self.world.assign_entity_id()
		self.create_from_archetype(ent_id, 'room')
		self.WORLD['position'][ent_id]['x'] = x
		self.WORLD['position'][ent_id]['y'] = y
		self.lorify(ent_id)
		return ent_id


	def monster_creator(self, monster_type = 'random'):
		ent_id = self.world.assign_entity_id()
		if monster_type == 'random':
			monster_type = random.choice(list(self.descriptors['names']['monsters'].keys()))

		for component in list(self.archetypes['monster'].keys()):
			self.create_components(component, ent_id)

		self.WORLD['monster'][ent_id]['type'] = monster_type
		self.lorify(ent_id)
		return ent_id


	def area_creator(self):
		ent_id = self.world.assign_entity_id()
		for component in list(self.archetypes['area'].keys()):
			self.create_components(component, ent_id)
		return ent_id

	def container_creator(self):
		ent_id = self.world.assign_entity_id()
		self.create_from_archetype(ent_id, 'container')
		self.lorify(ent_id)
		return ent_id
	
	def create_consumbale(self, c_type = "refill", size = "small"):
		ent_id = self.world.assign_entity_id()
		if c_type == 'refill':
			self.create_from_archetype(ent_id, 'consumable_refill')
			self.WORLD['buff_refill'][ent_id]['amount'] = self.stats['consumable_stats']['refill'][size]
			self.WORLD['consumable'][ent_id]['size']    = size
		# Add more types here
		self.lorify(ent_id)
		return ent_id

	def pair_doors(self, door1, door2):
		desc = random.choice(self.descriptors['doors'])
		self.WORLD['descriptor'][door1]['name'] = desc['name']
		self.WORLD['descriptor'][door1]['desc'] = desc['desc']

		self.WORLD['descriptor'][door2]['name'] = desc['name']
		self.WORLD['descriptor'][door2]['desc'] = desc['desc']

	def door_creator(self, targets, direction):
		ent_id = self.world.assign_entity_id()
		self.create_from_archetype(ent_id, 'door')
		self.WORLD['transition'][ent_id]['target'] = targets
		if direction == "Upwards" or direction == "Downwards":
			self.WORLD['descriptor'][ent_id]['name'] = "Staircase"
			self.WORLD['descriptor'][ent_id]['desc'] = "The stairs go "+ direction
		else:
			self.WORLD['descriptor'][ent_id]['name'] = "Door"
			self.WORLD['descriptor'][ent_id]['desc'] = "The door goes "+ direction
		self.lorify(ent_id)
		return ent_id


	def weapon_creator(self, weapon_type = "random"):
		ent_id = self.world.assign_entity_id()
		if weapon_type == 'random':
			weapon_type = random.choice(list(self.descriptors['names']['objects'].keys()))

		#Same as monster_creator
		self.create_from_archetype(ent_id, weapon_type)

		self.WORLD['weapon'][ent_id] =  self.archetypes[weapon_type]['weapon'].copy()
		self.lorify(ent_id)
		return ent_id


