#!/usr/bin/env python
import random
from world   import *
from factory import *

# This file puts the pieces together and creates the dungeon itself.


# TODO- Document this monstrosity of a class.
#       Possibly make this class create dungeon FLOORS instead of the whole dungeon.
#       And then create another class that calls this one if it needs more floors.

class Dungeon_Generator():
    def __init__(self):
        self.world = World()

    # As long as a user calls this function before calling create_dungeon, 
    # the class will use the provided world instead of using a Brand new one.
    # Whats the purpose of this? No idea, for future uses I suppose :3
    def set_world(self, world):
        self.world = world

    def get_world(self):
        return self.world

    def create_dungeon(self, floors):
        complexity = 3
        self.d_xsize    = complexity + 1
        self.d_ysize    = complexity + 1
        # Dungeons will have floors will have rooms
        d_map      = {} #Dict of floors where [key] = floor: [Value] = floor map
        for floor in range(floors):
            self.d_xsize = complexity
            self.d_ysize = complexity
            self.f_map = {}
            self.unvisited  = []
            self.generation_inits()
            self.randomize_maze()
            d_map[floor] = self.f_map
            complexity += 1

        self.connect_floors(d_map)
        Dungeon_Spicer(self.world, d_map)



    #Creates empty maps, creates unvisited list... etc.
    def generation_inits(self):
        area_id = self.world.factory.area_creator()
        for x in range(self.d_xsize):
            for y in range(self.d_ysize):
                ent_id =  self.world.factory.room_creator(x, y)
                self.world.WORLD['area'][area_id]['rooms'].append(ent_id)
                self.unvisited.append(ent_id)
                self.f_map[x, y] = ent_id


    def randomize_maze(self):
        WORLD = self.world.WORLD
        dfs_x = random.randint(0, self.d_xsize -1)
        dfs_y = random.randint(0, self.d_ysize -1)
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
                    WORLD['isroom'][current]['exits'][0]      = temp_current
                    self.connect_rooms(current, temp_current, "forward")

                elif tmp[0] == "right":
                    WORLD['isroom'][temp_current]['exits'][3] = current
                    WORLD['isroom'][current]['exits'][1]      = temp_current
                    self.connect_rooms(current, temp_current, "right")

                elif tmp[0] == "down":
                    WORLD['isroom'][temp_current]['exits'][0] = current
                    WORLD['isroom'][current]['exits'][2]      = temp_current
                    self.connect_rooms(current, temp_current, "back")

                elif tmp[0] == "left":
                    WORLD['isroom'][temp_current]['exits'][1] = current
                    WORLD['isroom'][current]['exits'][3]      = temp_current
                    self.connect_rooms(current, temp_current, "left")

                current = temp_current
                self.unvisited.remove(current)
            else:                                           # If the current node doesn't have any unvisited neighbors
                if len(place_stack) != 0:                   # If there are more nodes in the stack:
                    current = place_stack.pop()             # It gets the topmost node from the stack and set it to current


    def connect_floors(self, d_map):
        temp_dict = {}
        for floor in d_map:
            start = random.choice(list(d_map[floor].values()))
            end   = random.choice(list(d_map[floor].values()))
            if start != end:
                temp_dict[floor] = [start, end]

        for floor in temp_dict:
            if floor != list(temp_dict.keys())[-1]:
                self.connect_rooms(temp_dict[floor][1], temp_dict[floor + 1][0], "down")


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
        door2_id = self.world.factory.door_creator(temp_room, dir_2)
        self.world.WORLD['inventory'][current_room]['items'].append(door1_id)
        self.world.WORLD['inventory'][temp_room]['items'].append(door2_id)
        self.world.factory.pair_doors(door1_id,door2_id)            


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
        temp_neighbors = {"up": None, "right": None, "down": None, "left": None}
        node_loc  = self.world.WORLD['position'][place]
        #get up neighbor
        if self.world.WORLD['position'][place]['y'] != 0:
            temp_neighbors["up"] = node_loc['x']    , node_loc['y'] - 1
        #get right neighbor
        if node_loc['x'] != self.d_xsize - 1:
            temp_neighbors["right"] = node_loc['x'] + 1, node_loc['y']
        #get down neighbor
        if node_loc['y'] != self.d_ysize - 1:
            temp_neighbors["down"] = node_loc['x']    , node_loc['y'] + 1
        #get left neighbor
        if node_loc['x'] != 0:
            temp_neighbors["left"] = node_loc['x'] - 1, node_loc['y']
        return temp_neighbors



class Dungeon_Spicer:
    def __init__(self,world, d_map):
        self.world = world
        self.WORLD = self.world.WORLD
        #dungeon_generator = Dungeon_Generator(self.world)
        self.dungeon = d_map
        self.populate_dungeon()

    def populate_dungeon(self):
        for f in self.dungeon:
            for r in list(self.dungeon[f].values()):
                self.add_furniture(r)
        return self.world

    def add_furniture(self, room_id):
        for i in range(random.randrange(0, 6)):
            if random.randrange(0, 100) <= 30: # Containers
                ent_id  = self.world.factory.container_creator()
                self.WORLD['inventory'][room_id]['items'].append(ent_id)
                self.add_items(ent_id) 

            if random.randrange(0, 100) <= 40:
                self.add_items(room_id)


    def add_items(self, inv_id, i_type = "random"):
        for i in range(random.randrange(1, 4)):
            if random.randrange(0, 100) <= 30: # For weapons
                self.WORLD['inventory'][inv_id]['items'].append(self.world.factory.weapon_creator())



