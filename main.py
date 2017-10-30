from dungeon_creator import *
import json

class Game:
    def __init__(self):
        self.world
        self.GAME = True
        self.current_screen = main_menu
        with open("text.json") as text_files:
            self.TEXT = json.load(text_files)

    def game_loop(self):
        while self.GAME:
            user = input()
            self.current_screen(user)

    def main_menu(self, user):
        menu_text = self.TEXT['menu']
        for lines in menu_text['main_menu']:
            print(lines)

        

        
    
