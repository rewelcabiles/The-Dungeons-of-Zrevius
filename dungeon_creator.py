#!/usr/bin/env python
import random
from ecs_systems import *



class Dungeon_Generator():
    def __init__(self, world):
        self.world = world

    #Sets up initial maze variables
    def create_maze(self, sizex, sizey):
        self.d_xsize    = sizex
        self.d_ysize    = sizey
        self.d_map      = {}
        self.unvisited  = []
        self.generation_inits()
        self.randomize_maze()


    #Creates empty maps, creates unvisited list... etc.
    def generation_inits(self):

        area = self.world.factory.area_creator()

        for x in range(self.d_xsize):
            for y in range(self.d_ysize):
                ent_id =  self.world.factory.room_creator(x, y)
                self.world.WORLD['area'][area]['rooms'].append(ent_id)
                self.unvisited.append(ent_id)
                self.d_map[x, y] = ent_id

    def randomize_maze(self):
        WORLD = self.world.WORLD
        dfs_x = random.randint(0, self.d_xsize -1)
        dfs_y = random.randint(0, self.d_ysize -1)
        current = self.d_map[dfs_x, dfs_y]
        self.unvisited.remove(current)
        place_stack = []
        while len(self.unvisited) > 0:

            if self.has_unvisited_neighbor(current) == True:
                place_stack.append(current)
                tmp = self.get_random_unvisited_neighbor(current)
                temp_current = self.d_map[tmp[1]]

                if tmp[0] == "up":
                    print "Going Up!"
                    WORLD['isroom'][temp_current]['exits'][2] = current
                    WORLD['isroom'][current]['exits'][0]      = temp_current

                elif tmp[0] == "right":
                    print "Going Right!"
                    WORLD['isroom'][temp_current]['exits'][3] = current
                    WORLD['isroom'][current]['exits'][1]      = temp_current

                elif tmp[0] == "down":
                    print "Going Down!"
                    WORLD['isroom'][temp_current]['exits'][0] = current
                    WORLD['isroom'][current]['exits'][2]      = temp_current

                elif tmp[0] == "left":
                    print "Going Left!"
                    WORLD['isroom'][temp_current]['exits'][1] = current
                    WORLD['isroom'][current]['exits'][3]      = temp_current

                current = temp_current
                self.unvisited.remove(current)
            else:                                           # If the current node doesn't have any unvisited neighbors
                if len(place_stack) != 0:                   # If there are more nodes in the stack:
                    print 'taking a step back!'             # The generator backtracks
                    current = place_stack.pop()             # It gets the topmost node from the stack and set it to current
        self.create_dungeon_exits()

                                                            # Various helper functions.
    def create_dungeon_exits(self):
        while True:
            start = random.choice(self.world.WORLD['isroom'].keys())
            end   = random.choice(self.world.WORLD['isroom'].keys())
            if start != end:
                self.world.WORLD['isroom'][start]['type'] = spawn



    def get_random_unvisited_neighbor(self, place):
        temp = []
        temp_neigh = self.get_neighbors(place)
        for x in temp_neigh:
            if temp_neigh[x] != None:
                if self.is_visited(self.d_map[temp_neigh[x]]) == False:
                    temp.append((x, temp_neigh[x]))
        return random.choice(temp)


    def has_unvisited_neighbor(self, place):
        temp = self.get_neighbors(place)
        for x in temp:
            if temp[x] != None:
                if self.is_visited(self.d_map[temp[x]]) == False:
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
    def __init__(self, world):
        self.world = world
        self.WORLD = WORLD




#delete when on production
w  = World()
dg = Dungeon_Generator(w)
dg.create_maze(6,6)

