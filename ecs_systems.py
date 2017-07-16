import ecs_components
import random
import json

class COMPS:
    NONE = 0
    POS  = 1L << 0
    INV  = 2L << 1
    DESC = 1L << 2
    ROOM = 1L << 3


class World():
    def __init__(self):
        self.factory = Factory(self)
        #To add to the mask  , do: self.WORLD['mask'][entity_id] |= self.COMPS[compname]
        #To test for the mask, First, Create mask:
        #                          mask = (self.COMPS['position'] | self.comps['isroom'])
        #                      Then, Compare:
        #                          (self.WORLD['masks'][entity_id] & mask) == mask
        self.COMPS = {
            "none"       : 1L << 0,
            "position"   : 1L << 1,
            "inventory"  : 1L << 2,
            "descriptor" : 1L << 3,
            "isroom"     : 1L << 4
        }
        self.WORLD = {
                "mask"       : {},
                "position"   : {},
                "inventory"  : {},
                "descriptor" : {},
                "isroom"     : {}
        }
        self.entity_id_max = 1000

    def assign_entity_id(self):
        while True:
            entity_id = random.randint(1, self.entity_id_max)
            if entity_id not in self.WORLD['mask'].keys():
                self.WORLD['mask'][entity_id] = self.COMPS['none']
                return entity_id

    def destroy_entity(entity_id):
        self.all_entities.remove(entity_id)

#Make ecs_components.py a json file instead.
class Factory():
    def __init__(self,WORLD):
        self.world = WORLD
        with open('archetype.json') as data_file:
            self.archetypes = json.load(data_file)
        with open('components.json') as component_files:
            self.components = json.load(component_files)

    def create_components(self, comp, ent_id):
        WORLD = self.world.WORLD
        WORLD['mask'][ent_id]
        if   comp == "descriptor":
            WORLD['descriptor'][ent_id] = self.components['descriptor'].copy()
            WORLD['mask'][ent_id] |= self.world.COMPS['descriptor']
        elif comp == "position":
            #WORLD['position'][ent_id]  = ecs_components.position()
            WORLD['position'][ent_id]  = self.components['position'].copy()
            WORLD['mask'][ent_id] |= self.world.COMPS['position']
        elif comp == 'isroom':
            WORLD['isroom'][ent_id] = self.components['isroom'].copy()
            WORLD['mask'][ent_id] |= self.world.COMPS['isroom']
        elif comp == 'inventory':
            WORLD['inventory'][ent_id] = self.components['inventory'].copy()
            WORLD['mask'][ent_id] |= self.world.COMPS['inventory']

        else:
            print "ERROR: No Known Component Name!"


    #MAKE ALL CREATORS USE ARCHETYPE.JSON FILE ATTRIBUTES.
    def room_creator(self,x ,y):
        ent_id = self.world.assign_entity_id()
        for component in self.archetypes['room'].keys():
            self.create_components(component, ent_id)
            print component
        self.world.WORLD['position'][ent_id]['x'] = x
        self.world.WORLD['position'][ent_id]['y'] = y
        print ent_id
        #print self.world.WORLD['position'][ent_id]['x'], self.world.WORLD['position'][ent_id]['y']
        return ent_id


#w = World()
#f = Factory(w)
#f.room_creator()









