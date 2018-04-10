#/usr/bin/env python

from dungeon_creator import Dungeon_Generator as dun_gen
from player_commands import PlayerCommands
from Systems import Systems_Master, MessageBoard
import json
import random
# This is where we add functions that interface with the world object
#
#


class GameFunctions:

	def __init__(self):
		self.init_world()
		# Maybe move the player spawning to the command classes?
		self.player_id = self.world.factory.npc_factory.create_character('Human', "Quin", False) 
		spawn_room     = random.choice(list(self.world.WORLD['isroom'].keys()))
		self.world.set_entity_location(self.player_id, spawn_room)
		self.message_board   = MessageBoard()
		self.systems 		 = Systems_Master(self)
		self.command   		 = PlayerCommands(self.world, self.message_board, self.player_id)
		self.init_systems()

	def init_systems(self):
		self.message_board.register(self.command.notified)
		
	def game_loop(self):
		while(True):
			self.command.update()
			self.save_dungeon()

	def init_world(self):
		dg = dun_gen()
		dg.create_dungeon(3)
		self.world = dg.get_world()
		self.save_dungeon()

	def load_dungeon(self):
		pass

	def save_dungeon(self):
		with open('data/data.json', 'w') as save_file:
			json.dump(self.world.WORLD, save_file, indent=4, sort_keys=True)

game = GameFunctions()
game.game_loop()





