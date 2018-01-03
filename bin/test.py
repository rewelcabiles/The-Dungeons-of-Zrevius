from dungeon_creator import Dungeon_Generator as dug
from ecs_systems import World
w = World()
dg = dug(w)
dg.create_dungeon(2)