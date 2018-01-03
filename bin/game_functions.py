#/usr/bin/env python

from dungeon_creator import Dungeon_Generator as dun_gen
import json

# This is where we add functions that interface with the world object
# 
# 

class Interface:

	def __init__(self):
		self.init_world()

	def init_world(self):
		dg = dun_gen()
		dg.create_dungeon(3)
		self.world = dg.get_world()

	def load_dungeon(self):
		pass

	def save_dungeon(self):
		with open('data/data.json', 'w') as save_file:
			json.dump(self.world.WORLD, save_file, indent=4, sort_keys=True)

	def move_ent(self, eid): # eid will refer to the entity ID of entities.
		pass


	def get_ent_pos(self, eid):
		pass


	def get_ent_stats(self, eid):
		pass

