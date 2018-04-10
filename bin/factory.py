import random
import json
import copy

# Bridges the gap between the information in the json files, and the dungeon creator.
# Loads json files, and uses the data to create objects for the dungeon.


class Factory():

	def __init__(self, WORLD):
		with open('data/archetype.json') as data_file:
			self.archetypes = json.load(data_file)
		with open('data/components.json') as component_files:
			self.components = json.load(component_files)
		with open('data/descriptors.json') as descriptor_files:
			self.descriptors = json.load(descriptor_files)
		with open('data/entity_stats.json') as stat_files:
			self.stats = json.load(stat_files)
		self.world = WORLD
		self.WORLD = self.world.WORLD
		self.npc_factory = NPC_Factory(self)
		self.buff_factory= Buff_Factory(self)
		self.item_factory= Equipment_Factory(self)

	def create_from_archetype(self, ent_id, archetype_name):
		for component in list(self.archetypes[archetype_name].keys()):
			if self.archetypes[archetype_name][component] != None:
				self.WORLD[component][ent_id] = copy.deepcopy(
					self.archetypes[archetype_name][component])
			else:
				self.WORLD[component][ent_id] = copy.deepcopy(
					self.components[component])
			self.WORLD['mask'][ent_id] |= self.world.COMPS[component]

	def create_components(self, comp, ent_id):
		self.WORLD[comp][ent_id] = copy.deepcopy(self.components[comp])
		self.WORLD['mask'][ent_id] |= self.world.COMPS[comp]

	def remove_component(self, comp, ent_id):
		self.WORLD[comp].pop(ent_id)
		self.WORLD['mask'][ent_id] ^= self.world.COMPS[comp]		

	def lorify(self, ent_id):
		npc_mask = (self.world.COMPS['npc'])
		weapon_mask = (self.world.COMPS['weapon'])
		isroom_mask = (self.world.COMPS['isroom'])
		door_mask = (self.world.COMPS['transition'])
		inventory_mask = (self.world.COMPS['inventory'])
		refill_mask = (self.world.COMPS['buff_refill']
					   | self.world.COMPS['consumable'])

		if (self.WORLD['mask'][ent_id] & door_mask) == door_mask:
			desc = random.choice(self.descriptors['doors'])
			self.WORLD['descriptor'][ent_id]['name'] = desc['name']
			self.WORLD['descriptor'][ent_id]['desc'] = desc['desc']

		elif (self.WORLD['mask'][ent_id] & isroom_mask) == isroom_mask:
			desc = random.choice(self.descriptors['rooms'])
			self.WORLD['descriptor'][ent_id]['name'] = desc['name']
			self.WORLD['descriptor'][ent_id]['desc'] = desc['desc']

		elif (self.WORLD['mask'][ent_id] & npc_mask) == npc_mask:
			npc_type = self.WORLD['monster'][ent_id]['type']
			self.WORLD['descriptor'][ent_id]['name'] = random.choice(
				self.descriptors['names']['monsters'][npc_type])

		elif (self.WORLD['mask'][ent_id] & weapon_mask) == weapon_mask:
			weapon_type = self.WORLD['weapon'][ent_id]['type']
			if random.randrange(1, 100) <= 10:
				rarity = 'unique'
			else:
				rarity = 'common'
			self.WORLD['descriptor'][ent_id]['name'] = random.choice(
				self.descriptors['names']['objects'][weapon_type][rarity])
			self.WORLD['descriptor'][ent_id]['desc'] = "A " + \
				rarity + " " + weapon_type
			self.WORLD['item'][ent_id]['rarity'] = rarity

		elif (self.WORLD['mask'][ent_id] & inventory_mask) == inventory_mask:
			self.WORLD['descriptor'][ent_id] = random.choice(
				self.descriptors['containers'])

		elif (self.WORLD['mask'][ent_id] & refill_mask) == refill_mask:
			if self.WORLD['consumable'][ent_id]['size'] == "small":
				self.WORLD['descriptor'][ent_id] = random.choice(
					self.descriptors['small_food'])

	def room_creator(self, x, y):
		ent_id = self.world.assign_entity_id()
		self.create_from_archetype(ent_id, 'room')
		self.WORLD['position'][ent_id]['x'] = x
		self.WORLD['position'][ent_id]['y'] = y
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

	def create_consumable(self, c_type="refill", size="small"):
		ent_id = self.world.assign_entity_id()
		if c_type == 'refill':
			self.create_from_archetype(ent_id, 'consumable_refill')
			self.WORLD['buff_refill'][ent_id]['amount'] = self.stats['consumable_stats']['refill'][size]
			self.WORLD['consumable'][ent_id]['size'] = size
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
			self.WORLD['descriptor'][ent_id]['desc'] = "The stairs go " + direction
		else:
			self.WORLD['descriptor'][ent_id]['name'] = "Door"
			self.WORLD['descriptor'][ent_id]['desc'] = "The door goes " + direction
		self.lorify(ent_id)
		return ent_id


	

class Equipment_Factory:
	def __init__(self, factory):
		self.factory = factory
		self.world = self.factory.world
		self.WORLD = self.world.WORLD

	def create_weapon(self, weapon_type=None):
		ent_id = self.world.assign_entity_id()
		self.factory.create_from_archetype(ent_id, 'weapon')
		weapon_type = random.choice(list(self.factory.stats["weapon_info"].keys()))
		weapon_info = self.factory.stats["weapon_info"][weapon_type]
		self.WORLD['equippable'][ent_id]['slot'] = weapon_info['slot']
		self.WORLD['weapon'][ent_id]['damage_type'] = weapon_info['damage_type']
		self.WORLD['weapon'][ent_id]['main_modifier'] = weapon_info['main_modifier']
		self.WORLD['weapon'][ent_id]['weapon_type'] = weapon_type
		if weapon_info['damage_type'] == "ranged":
			self.factory.create_components('shoots_projectiles', ent_id)
			self.WORLD['shoots_projectiles'][ent_id]['projectile_type'] = weapon_info['projectile_type']
		rarity = random.choice(["Common", "Unique"])

		if rarity == "Common":
			name = random.choice(self.factory.descriptors["names"]["objects"][weapon_info['damage_type']]['common']) + " " + weapon_type
		elif rarity == "Unique":
			name = random.choice(self.factory.descriptors["names"]["objects"][weapon_info['damage_type']]['unique'])

		self.WORLD['item'][ent_id]['rarity'] = rarity

		self.WORLD['descriptor'][ent_id]['name'] = name

		if self.WORLD['equippable'][ent_id]['slot'] == "one_hand":
			self.WORLD['descriptor'][ent_id]['desc'] = "It is a "+rarity+" one-handed "+weapon_type
		else:
			self.WORLD['descriptor'][ent_id]['desc'] = "It is a "+rarity+" two-handed "+weapon_type

		self.randomly_create_stats(ent_id)
		return ent_id

	def randomly_create_stats(self, ent_id):
		power = random.randrange(2,10)
		if self.world.get_slot_type(ent_id) == 'one_hand':
			power /= 2
		self.WORLD['weapon'][ent_id]['damage_power'] = power

		possible_stat_modifiers = []
		possible_stat_modifiers.append("health")
		for stats in self.factory.stats['npc_stats']["Human"]:
			possible_stat_modifiers.append(stats)

		for stat in random.sample(possible_stat_modifiers, random.randrange(0, 4)):
			random_modifier_value = int(random.randrange(1, 6))
			new_mod = self.factory.buff_factory.create_modifier(
				ent_id,
				random_modifier_value,
				"additive",
				stat
				)
			self.WORLD['applies_modifiers'][ent_id].append(new_mod)

	def add_modifiers(self, ent_id):
		pass

class Buff_Factory:
	# Can be used for modifiers as well
	def __init__(self, factory):
		self.factory = factory
		self.world = self.factory.world
		self.WORLD = self.world.WORLD


	def create_modifier(self, source, amount, types, affects, name = None, duration = None):
		ent_id = self.world.assign_entity_id()
		self.factory.create_from_archetype(ent_id, "stat_modifier")

		self.WORLD['descriptor'][ent_id]['name']    = name
		self.WORLD['modifier'][ent_id]['source_id'] = source
		self.WORLD['modifier'][ent_id]['duration']  = duration
		self.WORLD['modifier'][ent_id]['key']       = affects
		self.WORLD['modifier'][ent_id]['value']  	= amount
		self.WORLD['modifier'][ent_id]['type']  	= types
		return ent_id

class NPC_Factory: # Not going to lie, we probably dont need this in a separate class.
	def __init__(self, factory):
		self.factory = factory
		self.world = self.factory.world
		self.WORLD = self.world.WORLD

	def _create_base_character(self):
		ent_id = self.world.assign_entity_id()
		self.factory.create_from_archetype(ent_id, 'character')
		return ent_id

	def create_character(self, species = None, name = None, is_npc = True):
		ent_id = self._create_base_character()
		if species == None or species not in self.factory.stats['npc_stats'].keys():
			if species not in self.factory.stats['npc_stats'].keys() and species != None:
				print("DEBUG: SPECIES NOT IN NPC_STATS")
			species = random.choice(list(self.factory.stats['npc_stats'].keys()))

		if name == None:
			name    = random.choice(self.factory.descriptors['names'][species])

		if is_npc:
			self.factory.create_components('npc', ent_id)
			self.factory.create_components('ai_aggressive', ent_id)
			self.factory.create_components('ai_retaliates', ent_id)
		else:
			self.factory.create_components('player', ent_id)

		self.WORLD['stats'][ent_id] 			 = self.factory.stats['npc_stats'][species]
		self.WORLD['descriptor'][ent_id]['name'] = name
		return ent_id

	def create_basic_hostile_npc(self, species = None, name = None):
		ent_id = self.world.assign_entity_id()
		self.factory.create_from_archetype(ent_id, 'character')
		self.factory.create_components('npc', ent_id)
		self.factory.create_components('ai_aggressive', ent_id)
		self.factory.create_components('ai_retaliates', ent_id)

		if species == None or species not in self.factory.stats['npc_stats'].keys():
			if species not in self.factory.stats['npc_stats'].keys() and species != None:
				print("DEBUG HIGH: SPECIES NOT IN NPC_STATS")
			species = random.choice(list(self.factory.stats['npc_stats'].keys()))
		if name == None:
			name    = random.choice(self.factory.descriptors['names'][species])

		self._apply_npc_base_stats(ent_id, species)
		self.WORLD['descriptor'][ent_id]['name'] = name
		
		return ent_id

	def create_special_hostile_npc(self, species = None, name = None, stat = None):
		ent_id = self.create_basic_hostile_npc(species, name)
		if stat == None:
			stat = random.choice(list(self.WORLD['stats'][ent_id].keys()))
		postfix = random.choice(self.factory.descriptors["names"]["Special Postfix"][stat])
		addition = int(self.WORLD['stats'][ent_id][stat] * 0.28)
		self.WORLD['stats'][ent_id][stat] += addition
		new_name = self.WORLD['descriptor'][ent_id]['name'] + " " + postfix
		self.WORLD['descriptor'][ent_id]['name'] = new_name
		return ent_id

	def _apply_npc_base_stats(self, ent_id, species):
		null_stats = self.WORLD['stats'][ent_id]
		null_health= self.WORLD['health'][ent_id]

		# Iterates through specific stats from entity_stats.json and applies it to 
		# the Entities individual stats
		for new_stat in self.factory.stats['npc_stats'][species]: 
			
			if new_stat == "health":
				null_health['current'] = self.factory.stats['npc_stats'][species][new_stat]
				null_health['max'] = self.factory.stats['npc_stats'][species][new_stat]
			else:
				null_stats[new_stat] = self.factory.stats['npc_stats'][species][new_stat]