import os
import json

game = True

save_loc = "save_01"
has_save = False

def startup():
    if os.path.ispath(save_loc):
        has_save = True

def newgame():
    pass

def PROMPT(text, answer, callback):
    print(text)
    callback(raw_input("> "))

def main_menu():
    if has_save == True:
        while True:
            print("1) New Game")
            print("2) Continue")
            user = raw_input(">> ");
            if user == "1":
                new_game()
            elif user == "2":
                continue_game()
            else:
                print("Invalid Command." )

def continue_game():
    pass

def new_game():
    Character = {
            name : None,
            place: [],
    }
    GAME(Character)


def GAME(savefile):
    pass



