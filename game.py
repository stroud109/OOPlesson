import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####
pass
####   End class definitions    ####

class Wall(GameElement):
    IMAGE = "StoneBlock"
    SOLID = True
    COLLECTIBLE = False

class Tree(GameElement):
    IMAGE = "TreeUgly"
    SOLID = False
    COLLECTIBLE = False

    def interact(self, player):
            
        GAME_BOARD.draw_msg("Oh look! There's a secret passageway behind the shrubbery!")

class DoorOpen(GameElement):
    IMAGE = "DoorOpen"
    SOLID = False
    COLLECTIBLE = False

class DoorClosed(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True
    COLLECTIBLE = False

    def interact(self, player):
        
        if len(player.inventory.get('keys', []))> 0:
            self.SOLID = False
            
            GAME_BOARD.draw_msg("You stealthily opened a door with your stolen key!")
            
        else:
            GAME_BOARD.draw_msg("Arg! The door is locked! Search the grounds for a key.")

class Bug(GameElement):
    IMAGE = "Bug"
    SOLID = True
    COLLECTIBLE = True
    
    def interact(self, player):
        player.inventory['bugs'] = []
        
        if len(player.inventory.get('keys', []))> 0:
            self.SOLID = False
            bugs = player.inventory.get('bugs', [])
            bugs.append(self)

            player.inventory['bugs'] = bugs 
            GAME_BOARD.draw_msg("You've collected the bug! You have %d bugs."%(len(player.inventory['bugs'])))
            
        else:
            GAME_BOARD.draw_msg("You need a key to unlock the exhibit and collect the bug!")

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = True
    COLLECTIBLE = True
    
    def interact(self, player):
        player.inventory['gems'] = []
        
        if len(player.inventory.get('keys', []))> 0:
            self.SOLID = False
            gems = player.inventory.get('gems', [])
            gems.append(self)

            #'gems' is the key, gems is the list of jewels.

            player.inventory['gems'] = gems 
            GAME_BOARD.draw_msg("The gem is yours! You have %d gems."%(len(player.inventory['gems'])))
            
        else:
            GAME_BOARD.draw_msg("You need a key to collect a gem!")
            


class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    COLLECTIBLE = True

    def interact(self, player):
        keys = player.inventory.get('keys', [])
        keys.append(self)

        player.inventory['keys'] = keys
        GAME_BOARD.draw_msg("You stole a key that you found lying on the ground. You have %d keys."%(len(player.inventory['keys'])))


class Character(GameElement):
    IMAGE = "Princess"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = {}

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"
    if KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()


    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if next_x in range(GAME_WIDTH) and next_y in range(GAME_HEIGHT):

            existing_el = GAME_BOARD.get_el(next_x, next_y)

            if existing_el:
                existing_el.interact(PLAYER)


            if existing_el is None or not existing_el.SOLID:
                ##Get position
                ##Look at map
                item = GAME_BOARD.original_map[PLAYER.y][PLAYER.x]
                ##see if there is something to redraw
                
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)
                ##redraw if applicible
              
                if item in "^OL":
                    print "not COLLECTIBLE!"
                    #draw_item(next_x, next_y, item)
                    draw_board()

       
def draw_board():

    map_file = open("game_map.txt")
    map_text_lines = map_file.readlines()
    GAME_BOARD.original_map = map_text_lines

    for y in range(len(map_text_lines)):
        row = map_text_lines[y]
        for x in range(len(row)):
            item = map_text_lines[y][x]

            
            if item == '#':
                wall = Wall()
                GAME_BOARD.register(wall)
                GAME_BOARD.set_el(x, y, wall)

            if item == '^':
                tree = Tree()
                GAME_BOARD.register(tree)
                GAME_BOARD.set_el(x, y, tree)

            if item == 'O':
                open_door = DoorOpen()
                GAME_BOARD.register(open_door)
                GAME_BOARD.set_el(x, y, open_door)

            if item == 'L':
                closed_door = DoorClosed()
                GAME_BOARD.register(closed_door)
                GAME_BOARD.set_el(x, y, closed_door)

            if item == '*':
                gem = Gem()
                GAME_BOARD.register(gem)
                GAME_BOARD.set_el(x, y, gem)

            if item == 'K':
                key = Key()
                GAME_BOARD.register(key)
                GAME_BOARD.set_el(x, y, key)

            if item == 'B':
                bug = Bug()
                GAME_BOARD.register(bug)
                GAME_BOARD.set_el(x, y, bug)


def draw_item(x, y,item):

            
    if item == '#':
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(x, y, wall)

    if item == '^':
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(x, y, tree)

    if item == 'O':
        open_door = DoorOpen()
        GAME_BOARD.register(open_door)
        GAME_BOARD.set_el(x, y, open_door)

    if item == 'L':
        closed_door = DoorClosed()
        GAME_BOARD.register(closed_door)
        GAME_BOARD.set_el(x, y, closed_door)

    if item == '*':
        gem = Gem()
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(x, y, gem)

    if item == 'K':
        key = Key()
        GAME_BOARD.register(key)
        GAME_BOARD.set_el(x, y, key)

    if item == 'B':
        bug = Bug()
        GAME_BOARD.register(bug)
        GAME_BOARD.set_el(x, y, bug)



def initialize():


    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0,4, PLAYER)

    GAME_BOARD.draw_msg("Princess Game!!!")


    keyboard_handler()
    draw_board()