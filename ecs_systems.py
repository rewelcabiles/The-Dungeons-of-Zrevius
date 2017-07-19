import random
import json

class World():
    def __init__(self):
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
            "isroom"     : 1L << 4,
            "stats"      : 1L << 5,
            "weapon"     : 1L << 6,
            "monster"    : 1L << 7,
            "p"          : 1L << 8,
            "p"          : 1L << 9,
            "p"          : 1L << 10,

        }
        self.WORLD = {
                "mask"       : {},
                "position"   : {},
                "inventory"  : {},
                "descriptor" : {},
                "isroom"     : {},
                "stats"      : {},
                "weapon"     : {},
                "monster"    : {}
        }
        self.entity_id_max = 1000
        self.factory = Factory(self)

    def assign_entity_id(self):
        while True:
            entity_id = random.randint(1, self.entity_id_max)
            if entity_id not in self.WORLD['mask'].keys():
                self.WORLD['mask'][entity_id] = self.COMPS['none']
                return entity_id


    def destroy_entity(entity_id):
        self.all_entities.remove(entity_id)



class Factory():

    def __init__(self,WORLD):
        self.world = WORLD
        self.WORLD = self.world.WORLD
        with open('archetype.json') as data_file:
            self.archetypes = json.load(data_file)
        with open('components.json') as component_files:
            self.components = json.load(component_files)
        with open('descriptors.json') as descriptor_files:
            self.descriptors= json.load(descriptor_files)

    def create_components(self, comp, ent_id):
        self.WORLD[comp][ent_id] = self.components[comp].copy()
        self.WORLD['mask'][ent_id] |= self.world.COMPS[comp]


    def lorify(self,ent_id):
        monster_mask = (self.world.COMPS['monster'])
        weapon_mask  = (self.world.COMPS['weapon'])
        if (self.world.WORLD['masks'][ent_id] & monster_mask) == monster_mask:
            monster_type = self.WORLD['monster']['type']

        if (self.world.WORLD['masks'][ent_id] & weapon_mask) == weapon_mask:
            pass



    #MAKE ALL CREATORS USE ARCHETYPE.JSON FILE ATTRIBUTES.
    def room_creator(self,x ,y):
        ent_id = self.world.assign_entity_id()
        for component in self.archetypes['room'].keys():
            self.create_components(component, ent_id)
        self.WORLD['position'][ent_id]['x'] = x
        self.WORLD['position'][ent_id]['y'] = y

        return ent_id

    def monster_creator(self, monster_type = 'random'):
        ent_id = self.world.assign_entity_id()
        if monster_type == 'random':
            monster_type = random.choice(self.descriptors['names']['monsters'].keys())

        #Possibly move this into the Archetype json as a generic monster
        #Add special/unqiue/random components afterwards.
        self.create_components('stats',ent_id)
        self.create_components('descriptor',ent_id)
        self.create_components('monster',ent_id)
        self.create_components('inventory',ent_id)

        self.WORLD['monster'][ent_id]['type'] = monster_type
        return ent_id

    def weapon_creator(self, weapon_type = "random"):
        ent_id = self.world.assign_entity_id()
        if weapon_type == 'random':
            weapon_type = random.choice(self.descriptors['names']['objects'].keys())

        self.WORLD['weapon'][ent_id] =  self.archetypes['bow']['weapon'].copy()

        #Same as monster_creator
        self.create_components('descriptor')
        self.create_components('weapon')

        return ent_id

#w = World()
#f = Factory(w)









