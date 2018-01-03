import json
import random


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
