#!/usr/bin/env python
import random
from ecs_systems import *



class Dungeon_Generator():
    def __init__(self, world):
        self.world = world

    #Sets up initial maze variables
    def create_maze(self, sizex, sizey):
        self.d_xsize    = sizex                 # Width of maze (In terms of rooms) ex. d_xsize = 6 = six rooms from the leftmost side to the right
        self.d_ysize    = sizey                 # Same as above, but for height
        self.d_map      = {}                    # Map of maze, instead of using a 2d array, I use a dictionary. You will understand why later.
        self.unvisited  = []                    # The algorithm used to generate a random maze can be found in the "Maze Generation" Wikipedia
        self.generation_inits()
        self.randomize_maze()


    #Creates empty maps, creates unvisited list... etc.
    def generation_inits(self):
        print("Initializing Maps...")
        for x in range(self.d_xsize):                               # These two for loops get the coordinates for the different rooms in the maze
            for y in range(self.d_ysize):
                ent_id =  self.world.factory.room_creator(x, y)     # Creates an entity ID for the room, in the background, this also adds it to the WORLD dictionary
                self.unvisited.append(ent_id)                       # Adds the created room entities into a List called Unvisited, this is part of the maze generation algorithm
                self.d_map[x, y] = ent_id                           # The coordinates of each room is the key to the dictionary, while ent_id is the value.
                                                                    # If someone wanted to get the properties of a room. They would just have to do:
                                                                    # self.world.WORLD[component_needed][entity_id]         Where component needed is the name of the component.


    def randomize_maze(self):
        WORLD = self.world.WORLD                                    # Shortcut so I dont have to repeatedly type "self.world.WORLD"
        print("Maze Randomization Started.")                        # Since this is a text game, all the current print statements right now are temporary, and used for debugging
        dfs_x = random.randint(0, self.d_xsize -1)                  # The first part of the Algorithm requires that we get a random starting cell/node/room/place.
        dfs_y = random.randint(0, self.d_ysize -1)
        current = self.d_map[dfs_x, dfs_y]                          # Sets the random cell as current.
        print("Choosing Random Place: ", dfs_x, dfs_y)
        self.unvisited.remove(current)                              # Remove current cell from unvisited list
        place_stack = []                                            # Initiates empty stack. This stack is used by the maze generator to backtrack to previously visited nodes.

        while len(self.unvisited) > 0:                              # While there are still nodes inside the unvisited list.

            print "Current Node: ", WORLD['position'][current]['x'], WORLD['position'][current]['y']

            if self.has_unvisited_neighbor(current) == True:                                            # Check if current node has unvisited neighbors
                place_stack.append(current)                                                             # If true: add current to the stack.

                tmp = self.get_random_unvisited_neighbor(current)                                       # Get random unvisited neighbor
                temp_current = self.d_map[tmp[1]]
                                                                                                        # The following if statements connect the current node, and the random neighbor chosen
                if tmp[0] == "up":                                                                      # By editing the 'exit' properties in their 'isroom' component
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

                current = temp_current                                                      # Afterwards, set the randomly chosen neighbor as the current node
                self.unvisited.remove(current)                                              # remove the (new) current node from the unvisited stack (Therby making it visited)

            else:                                           # If the current node doesn't have any unvisited neighbors
                if len(place_stack) != 0:                   # If there are more nodes in the stack:
                    print 'taking a step back!'             # The generator backtracks
                    current = place_stack.pop()             # It gets the topmost node from the stack and set it to current
                                                            # If the current node has no unvisited neighbors and the stack is empty. The maze is done generating


                                                            # Various helper functions.

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
    def __init__(self):
        pass




#delete when on production
w  = World()
dg = Dungeon_Generator(w)
dg.create_maze(6,6)

