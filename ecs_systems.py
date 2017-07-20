import random
import json
import copy

class World():
    def __init__(self):


        # This is part of the component bit mask system.
        # It's used to check if an entity has a specific component
        # When an entity is first created, it comp mask will be self.COMPS['none'], or just none for short.
        # When components are added to or removed from an entity the masks gets updated to reflect the change
        #
        # To add a component to the component mask of an entity, it is done by using the following line.
        # For this example we will be adding a monster component to an entities component mask.
        #
        #           self.WORLD['mask'][entity_id] |= self.COMPS["monster"]
        #
        # To remove an entity from the component mask:
        #
        #           self.WORLD['mask'][entity_id] &= ~self.COMPS["monster"]
        #
        # Since the masks are just used as an easy way for systems to check for components.
        # You actually have to remove the component from the world as well, not just the masks.
        self.COMPS = {
            "none"       : 1L << 0,
            "position"   : 1L << 1,
            "inventory"  : 1L << 2,
            "descriptor" : 1L << 3,
            "isroom"     : 1L << 4,
            "stats"      : 1L << 5,
            "weapon"     : 1L << 6,
            "monster"    : 1L << 7,
            "equipment"  : 1L << 8,
            "p"          : 1L << 9,
            "p"          : 1L << 10,

        }


        with open ('components.json') as component_files:
           components = json.load(component_files)

        # This is where all the specific component dicts reside, inside the WORLD dictionary
        self.WORLD = {}
        self.COMPS = {}
        # This creates the specific dictionaries where the actual components resides in
        # The keys inside WORLD would be the names of each available component in the components.json file.
        # The values will be an empty dictionary
        # The Dictionaries are where all the actual entity components of the specific type will reside.
        self.COMPS['none'] = 1L << 0
        iterator = 1
        for key in components:
            self.WORLD[key] = {}
            self.COMPS[key] = 1L << iterator
            iterator += 1

        self.entity_id_max = 1000
        self.factory = Factory(self)

    def assign_entity_id(self):
        while True:
            entity_id = random.randint(1, self.entity_id_max)       # Generates a random id for an entity
            if entity_id not in self.WORLD['mask'].keys():          # Checks if the id is already in use.
                self.WORLD['mask'][entity_id] = self.COMPS['none']  # If not, create a mask with nothing in it.
                return entity_id                                    # Returns the id to whatever called the-
                                                                    # function.


    def destroy_entity(entity_id):
        self.all_entities.remove(entity_id) # This hasn't been updated to the new system yet.



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
        self.WORLD[comp][ent_id] = copy.deepcopy(self.components[comp])
        self.WORLD['mask'][ent_id] |= self.world.COMPS[comp]


    def lorify(self,ent_id):
        monster_mask = (self.world.COMPS['monster'])
        weapon_mask  = (self.world.COMPS['weapon'])

        if (self.world.WORLD['mask'][ent_id] & monster_mask) == monster_mask:
            monster_type = self.WORLD['monster'][ent_id]['type']
            self.WORLD['descriptor'][ent_id]['name'] = random.choice(self.descriptors['names']['monsters'][monster_type])

        if (self.world.WORLD['mask'][ent_id] & weapon_mask) == weapon_mask:
            weapon_type = self.WORLD['weapon'][ent_id]['type']
            if random.randrange(1,100) <= 10:
                rarity = 'unique'
            else:
                rarity = 'common'
            print rarity
            self.WORLD['descriptor'][ent_id]['name'] = random.choice(self.descriptors['names']['objects'][weapon_type][rarity])



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

        for component in self.archetypes['monster'].keys():
            self.create_components(component, ent_id)

        self.WORLD['monster'][ent_id]['type'] = monster_type
        self.lorify(ent_id)
        return ent_id

    def area_creator(self):
        ent_id = self.world.assign_entity_id()
        for component in self.archetypes['area'].keys():
            self.create_components(component, ent_id)
        return ent_id

    def weapon_creator(self, weapon_type = "random"):
        ent_id = self.world.assign_entity_id()
        if weapon_type == 'random':
            weapon_type = random.choice(self.descriptors['names']['objects'].keys())

        #Same as monster_creator
        self.create_components('descriptor',ent_id)
        self.create_components('weapon', ent_id)

        self.WORLD['weapon'][ent_id] =  self.archetypes[weapon_type]['weapon'].copy()
        self.lorify(ent_id)
        return ent_id

#w = World()
#f = Factory(w)









