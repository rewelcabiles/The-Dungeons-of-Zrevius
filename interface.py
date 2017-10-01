#/usr/bin/env python

from dungeon_creator import Dungeon_Spicer, Dungeon_Generator
from ecs_systems import World

#This is where we add functions that interface with the world object
#Things like, move_entity and whatnot



class Interface:

    def __init__(self, world):
        self.world = world


