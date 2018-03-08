#!/usr/bin/env python
import random
from world import *
from factory import *

# This file puts the pieces together and creates the dungeon itself.

# TODO: Document this monstrosity of a class.
#       Possibly make this class create dungeon FLOORS instead of the whole dungeon.
#       And then create another class that calls this one if it needs more floors.
# TODO: Make a function that ONLY creates floors, separate it from the generation as a whole.

class Dungeon_Generator():
	def __init__(self):
		self.world = World()

	def set_world(self, world):
		self.world = world

	def get_world(self):
		return self.world

	def create_dungeon(self, floors):
		complexity = 4
		floors = 1
		self.d_xsize = complexity 
		self.d_ysize = complexity 
		d_map = {}
		for floor in range(floors):
			self.d_xsize = complexity
			self.d_ysize = complexity
			self.f_map = {}
			self.unvisited = []
			self.generation_inits()
			self.randomize_maze()
			d_map[floor] = self.f_map
			complexity += 1

		self.connect_floors(d_map)
		Dungeon_Spicer(self.world, d_map)

	# Creates empty maps, creates unvisited list... etc.
	def generation_inits(self):
		area_id = self.world.factory.area_creator()
		for x in range(self.d_xsize):
			for y in range(self.d_ysize):
				ent_id = self.world.factory.room_creator(x, y)
				self.world.WORLD['area'][area_id]['rooms'].append(ent_id)
				self.unvisited.append(ent_id)
				self.f_map[x, y] = ent_id

	def randomize_maze(self):
		WORLD = self.world.WORLD
		dfs_x = random.randint(0, self.d_xsize - 1)
		dfs_y = random.randint(0, self.d_ysize - 1)
		current = self.f_map[dfs_x, dfs_y]
		self.unvisited.remove(current)
		place_stack = []
		while len(self.unvisited) > 0:

			if self.has_unvisited_neighbor(current) == True:
				place_stack.append(current)
				tmp = self.get_random_unvisited_neighbor(current)
				temp_current = self.f_map[tmp[1]]

				if tmp[0] == "up":
					WORLD['isroom'][temp_current]['exits'][2] = current
					WORLD['isroom'][current]['exits'][0] = temp_current
					self.connect_rooms(current, temp_current, "forward")

				elif tmp[0] == "right":
					WORLD['isroom'][temp_current]['exits'][3] = current
					WORLD['isroom'][current]['exits'][1] = temp_current
					self.connect_rooms(current, temp_current, "right")

				elif tmp[0] == "down":
					WORLD['isroom'][temp_current]['exits'][0] = current
					WORLD['isroom'][current]['exits'][2] = temp_current
					self.connect_rooms(current, temp_current, "back")

				elif tmp[0] == "left":
					WORLD['isroom'][temp_current]['exits'][1] = current
					WORLD['isroom'][current]['exits'][3] = temp_current
					self.connect_rooms(current, temp_current, "left")

				current = temp_current
				self.unvisited.remove(current)
			else:                                          
				if len(place_stack) != 0:
					current = place_stack.pop()

	def connect_floors(self, d_map):
		temp_dict = {}
		for floor in d_map:
			start = random.choice(list(d_map[floor].values()))
			end = random.choice(list(d_map[floor].values()))
			if start != end:
				temp_dict[floor] = [start, end]

		for floor in temp_dict:
			if floor != list(temp_dict.keys())[-1]:
				self.connect_rooms(
					temp_dict[floor][1], temp_dict[floor + 1][0], "down")

	def connect_rooms(self, current_room, temp_room, direction):
		if direction == "forward":
			dir_1 = "forward"
			dir_2 = "backward"

		elif direction == "right":
			dir_1 = "right"
			dir_2 = "left"

		elif direction == "back":
			dir_1 = "backward"
			dir_2 = "forward"

		elif direction == "left":
			dir_1 = "left"
			dir_2 = "right"

		elif direction == "up":
			dir_1 = "Upwards"
			dir_2 = "Downwards"

		elif direction == "down":
			dir_1 = "Downwards"
			dir_2 = "Upwards"
		door1_id = self.world.factory.door_creator(temp_room, dir_1)
		door2_id = self.world.factory.door_creator(current_room, dir_2)
		self.world.add_to_inventory(door1_id, current_room)
		self.world.add_to_inventory(door2_id, temp_room)
		self.world.factory.pair_doors(door1_id, door2_id)

	def get_random_unvisited_neighbor(self, place):
		temp = []
		temp_neigh = self.get_neighbors(place)
		for x in temp_neigh:
			if temp_neigh[x] != None:
				if self.is_visited(self.f_map[temp_neigh[x]]) == False:
					temp.append((x, temp_neigh[x]))
		return random.choice(temp)

	def has_unvisited_neighbor(self, place):
		temp = self.get_neighbors(place)
		for x in temp:
			if temp[x] != None:
				if self.is_visited(self.f_map[temp[x]]) == False:
					return True
		return False

	def is_visited(self, place):
		if place in self.unvisited:
			return False
		else:
			return True

	def get_neighbors(self, place):
		temp_neighbors = {"up": None, "right": None,
						  "down": None, "left": None}
		node_loc = self.world.WORLD['position'][place]
		# get up neighbor
		if self.world.WORLD['position'][place]['y'] != 0:
			temp_neighbors["up"] = node_loc['x'], node_loc['y'] - 1
		# get right neighbor
		if node_loc['x'] != self.d_xsize - 1:
			temp_neighbors["right"] = node_loc['x'] + 1, node_loc['y']
		# get down neighbor
		if node_loc['y'] != self.d_ysize - 1:
			temp_neighbors["down"] = node_loc['x'], node_loc['y'] + 1
		# get left neighbor
		if node_loc['x'] != 0:
			temp_neighbors["left"] = node_loc['x'] - 1, node_loc['y']
		return temp_neighbors


class Dungeon_Spicer:
	def __init__(self, world, d_map):
		self.world = world
		self.WORLD = self.world.WORLD
		self.dungeon = d_map
		self.max_enemies = 5
		self.max_rooms = 0
		for f in self.dungeon:
			for r in list(self.dungeon[f].values()):
				self.max_rooms += 1
		self.populate_dungeon()

	def populate_dungeon(self):
		for f in self.dungeon:
			for r in list(self.dungeon[f].values()):
				self.add_furniture(r)
				#self.initial_spawn_monster(r) # This function is broken, pls fix
		return self.world

	def initial_spawn_monster(self, room_id): 
		while self.max_enemies != 0:
			# I made this function ages ago and don't exactly remember what it does. pls fix.
			if random.randrange(0, 100) <= ((self.max_enemies / self.max_rooms) * 100): 
				new_monster = self.world.factory.random_monster_creator()
				self.world.add_to_inventory(new_monster, room_id)


	def add_furniture(self, room_id):
		for i in range(random.randrange(0, 6)):
			if random.randrange(0, 100) <= 30:  # Containers
				ent_id = self.world.factory.container_creator()
				self.world.add_to_inventory(ent_id, room_id)
				self.add_items(ent_id)
			# Chance  to spawn any loose items at all
			if random.randrange(0, 100) <= 40:
				self.add_items(room_id)

	def add_items(self, inv_id, i_type="random"):
		for i in range(random.randrange(1, 3)):
			if random.randrange(0, 100) <= 20:  # For weapons
				new_weapon = self.world.factory.weapon_creator()
				self.world.add_to_inventory(new_weapon, inv_id)

			if random.randrange(0, 100) <= 45:  # For consumables
				new_consumable = self.world.factory.create_consumbale()
				self.world.add_to_inventory(new_consumable, inv_id)
