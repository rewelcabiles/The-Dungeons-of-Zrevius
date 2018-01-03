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

	def game_loop(self):
		while(True):
			user = input("Health: >>")
			if user == "look":
				print(self.interface.get_descriptor(self.current_pos)['name']+'\n')
				print(self.interface.get_descriptor(self.current_pos)['desc'])
			elif user == "break":
				break


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

    def get_area(self):
        return list(self.WORLD['area'].keys())

    def get_descriptor(self, ent_id):
    	return self.WORLD['descriptor'][ent_id]

    def get_rooms_in_area(self, area_id):
        return list(self.WORLD['area'][area_id]['rooms'].keys())

    def get_room_data(self, room_id):
        return list(self.WORLD['isroom'][room_id])
