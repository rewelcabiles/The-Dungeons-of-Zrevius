#/usr/bin/env python

from dungeon_creator import Dungeon_Generator as dun_gen
from game_commands import Command
import json
import random
# This is where we add functions that interface with the world object
# 
# 


class GameFunctions:

	def __init__(self):
		self.init_world()
		self.current_pos = random.choice(list(self.world.WORLD['isroom'].keys()))
		self.command = Command(self)
		print(self.current_pos)

	def game_loop(self):
		while(True):
			self.command.do()

	def init_world(self):
		dg = dun_gen()
		dg.create_dungeon(3)
		self.world = dg.get_world()

	def load_dungeon(self):
		pass

	def save_dungeon(self):
		with open('data/data.json', 'w') as save_file:
			json.dump(self.world.WORLD, save_file, indent=4, sort_keys=True)

	def create_dynamic_mask(self, component_list):
    	temp_mask = 0
    	for comps in component_list:
    		temp_mask |= self.world.COMPS[comps]
    	return temp_mask

    



test = GameFunctions()
test.game_loop()