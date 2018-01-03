import json
import random
import factory

class WorldInterface():
    def __init__(self, world):
        self.world_class = world
        self.WORLD       = self.world_class.WORLD

    def get_area(self):

        return list(self.WORLD['area'].keys())
        
    def get_rooms_in_area(self, area_id):
        return list(self.WORLD['area'][area_id]['rooms'].keys())

    def get_room_data(self, room_id):
        return list(self.WORLD['isroom'][room_id])



class World():

    def __init__(self):
        #Loads the files that contains all components
        with open ('data/components.json') as component_files:
           components = json.load(component_files)
        self.WORLD = {}
        self.COMPS = {}
        self.COMPS['none'] = 1 << 0
        iterator = 1
        for key in components:
            self.WORLD[key] = {}
            self.COMPS[key] = 1 << iterator
            iterator += 1
        self.entity_id_max = 1000
        self.factory = factory.Factory(self)


    def assign_entity_id(self):
        while True:
            entity_id = random.randint(1, self.entity_id_max)
            if entity_id not in list(self.WORLD['mask'].keys()):
                self.WORLD['mask'][entity_id] = self.COMPS['none']
                return entity_id


    def destroy_entity(entity_id):
        pass # ye.
