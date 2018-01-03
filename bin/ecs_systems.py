import random
import json
import copy

class World():

    def __init__(self):

        #Loads the files that contains all components
        with open ('components.json') as component_files:
           components = json.load(component_files)

        # This is where all the specific component dicts reside, inside the WORLD dictionary
        self.WORLD = {}
        self.COMPS = {}
        # Creates the dictionaries for each component in the components.json files
        self.COMPS['none'] = 1 << 0
        iterator = 1
        for key in components:
            self.WORLD[key] = {}
            self.COMPS[key] = 1 << iterator
            iterator += 1
        self.entity_id_max = 1000
        self.factory = Factory(self)


    def assign_entity_id(self):
        while True:
            entity_id = random.randint(1, self.entity_id_max)
            if entity_id not in list(self.WORLD['mask'].keys()):
                self.WORLD['mask'][entity_id] = self.COMPS['none']
                return entity_id



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
    def create_from_archetype(self,ent_id, archetype_name):
        for component in list(self.archetypes[archetype_name].keys()):
            self.create_components(component, ent_id)


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
            print(rarity)
            self.WORLD['descriptor'][ent_id]['name'] = random.choice(self.descriptors['names']['objects'][weapon_type][rarity])



    def room_creator(self,x ,y):
        ent_id = self.world.assign_entity_id()
        self.create_from_archetype(ent_id, 'room')
        self.WORLD['position'][ent_id]['x'] = x
        self.WORLD['position'][ent_id]['y'] = y
        return ent_id


    def monster_creator(self, monster_type = 'random'):
        ent_id = self.world.assign_entity_id()
        if monster_type == 'random':
            monster_type = random.choice(list(self.descriptors['names']['monsters'].keys()))

        for component in list(self.archetypes['monster'].keys()):
            self.create_components(component, ent_id)

        self.WORLD['monster'][ent_id]['type'] = monster_type
        self.lorify(ent_id)
        return ent_id


    def area_creator(self):
        ent_id = self.world.assign_entity_id()
        for component in list(self.archetypes['area'].keys()):
            self.create_components(component, ent_id)
        return ent_id


    def furniture_creator(self, f_type = "random", f_name = 'random'):
        ent_id = self.world.assign_entity_id()
        if f_type == "random":
            f_type = random.choice(list(self.archetypes['furniture'].keys()))
            f_name = random.choice(list(self.archetypes['furniture'][f_type].keys()))
        print("Creating Furniture!")
        print(f_type)
        print(f_name)
        for component in list(self.archetypes['furniture'][f_type][f_name].keys()):
           self.create_components(component, ent_id)
        return ent_id, f_type


    def door_creator(self, targets, direction):
        ent_id = self.world.assign_entity_id()
        self.create_from_archetype(ent_id, 'door')
        self.WORLD['transition'][ent_id]['target'] = targets
        if direction == "up" or direction == "down":
            self.WORLD['descriptor'][ent_id]['name'] = "Stairs"
            self.WORLD['descriptor'][ent_id]['desc'] = "The stairs go", direction
        else:
            self.WORLD['descriptor'][ent_id]['desc'] = "The door goes",direction
        return ent_id


    def weapon_creator(self, weapon_type = "random"):
        ent_id = self.world.assign_entity_id()
        if weapon_type == 'random':
            weapon_type = random.choice(list(self.descriptors['names']['objects'].keys()))

        #Same as monster_creator
        self.create_components('descriptor',ent_id)
        self.create_components('weapon', ent_id)

        self.WORLD['weapon'][ent_id] =  self.archetypes[weapon_type]['weapon'].copy()
        self.lorify(ent_id)
        return ent_id

#w = World()
#f = Factory(w)









