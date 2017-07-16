class position:
    def __init__(self):
        self.x = 0
        self.y = 0

#class inventory:
#    def __init__(self):
#        self.name   = None
#        self.items  = []

def inventory():
    return {
            'name' : None,
            'items': None
            }

class descriptor:
    def __init__(self):
        self.name = None
        self.desc = None

class isroom:
    def __init__(self):
        self.name = None
        self.desc = None
        self.exits= [0,0,0,0]

