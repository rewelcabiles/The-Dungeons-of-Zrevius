#/usr/bin/env python

from dungeon_creator import Dungeon_Generator as dun_gen
import json
import random
# This is where we add functions that interface with the world object
# 
# 


class GameFunctions:

	def __init__(self):
		self.init_world()
		self.interface = WorldInterface(self.world)
		self.current_pos = random.choice(list(self.world.WORLD['isroom'].keys()))
		print(self.current_pos)
		
	def game_loop(self):
		while(True):
			user = input("Health: >>").split(" ")

			if user[0] == "look":
				for lookables in self.interface.get_all_room_objects(self.current_pos):
					self.pretty_look(self.interface.get_descriptor(lookables))
			elif user == "break":
				break

	def pretty_look(self, descriptor):
		print(descriptor['name'])
		print(descriptor['desc'])

	def init_world(self):
		dg = dun_gen()
		dg.create_dungeon(3)
		self.world = dg.get_world()

	def load_dungeon(self):
		pass

	def save_dungeon(self):
		with open('data/data.json', 'w') as save_file:
			json.dump(self.world.WORLD, save_file, indent=4, sort_keys=True)

class WorldInterface():
    def __init__(self, world):
        self.world_class = world
        self.WORLD       = self.world_class.WORLD

    def create_dynamic_mask(self, component_list):
    	temp_mask = 0
    	for comps in component_list:
    		temp_mask |= self.world_class.COMPS[comps]
    	return temp_mask


    def get_all_room_objects(self, room_id):
    	descriptor_mask = self.create_dynamic_mask(['descriptor'])
    	temp = []
    	for ent_id in list(self.WORLD['inventory'][room_id]['items']):
    		if((self.WORLD['mask'][ent_id] & descriptor_mask) == descriptor_mask):
    			temp.append(ent_id)
    	return temp

    def get_area(self):
        return list(self.WORLD['area'].keys())

    def get_descriptor(self, ent_id):
    	return self.WORLD['descriptor'][ent_id]

    def get_rooms_in_area(self, area_id):
        return list(self.WORLD['area'][area_id]['rooms'].keys())

    def get_room_data(self, room_id):
        return list(self.WORLD['isroom'][room_id])
