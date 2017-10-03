#/usr/bin/env python

from dungeon_creator import Dungeon_Spicer, Dungeon_Generator
from ecs_systems import World

#This is where we add functions that interface with the world object
#Things like, move_entity and whatnot


class Interface:

    def __init__(self, world):
        self.world = world


    def move_ent(self, eid): # eid will refer to the entity ID of entities.
        pass


    def get_ent_pos(self, eid):
        pass


    def get_ent_stats(self, eid):
        pass
