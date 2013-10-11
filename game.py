import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
GUARD = None
######################

GAME_WIDTH = 10
GAME_HEIGHT = 7

#### Put class definitions here ####
pass
####   End class definitions    ####

class Wall(GameElement):
    IMAGE = "StoneBlock"
    SOLID = True
    COLLECTIBLE = False

class FakeWall(GameElement):
    IMAGE = "StoneBlock"
    SOLID = False
    COLLECTIBLE = False

    def interact(self, player):

        draw_museum()
        GAME_BOARD.draw_msg("You picked the lock on the prison gate. Looks like pretty princess crowns are useful after all.")

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
        
        if len(player.inventory.get('keys'))> 0:
            self.SOLID = False
            
            GAME_BOARD.draw_msg("You stealthily opened a door with your stolen key!")
            
        else:
            GAME_BOARD.draw_msg("Arg! The door is locked! Search the grounds for a key.")

class Bug(GameElement):
    IMAGE = "Bug"
    SOLID = True
    COLLECTIBLE = True
    
    def interact(self, player):
        #player.inventory['bugs'] = []
        
        if len(player.inventory.get('keys'))> 0:
            self.SOLID = False
            # bugs = player.inventory.get('bugs', [])
            # bugs.append(self)

            player.inventory['bugs'].append(self)
            GAME_BOARD.draw_msg("You've collected the enormous, semi-precious bug! You have %d bug in your loot."%(len(player.inventory['bugs'])))
            
        else:
            GAME_BOARD.draw_msg("You need a key to unlock the exhibit and collect the bug!")

class Star(GameElement):
    IMAGE = "Star"
    SOLID = True
    COLLECTIBLE = True

    def interact(self, player):
        #use for loop to iterate through inventory.items()
            #sum items in inventory
        #divide float(sum) by total number of items to calculate chance of success
        #automatically proceed with heist, randomly generate win/lose scenario
        #draw message for player based on outcome

        temp = 0
        for loot_name, value_list in player.inventory.items():
            temp += len(value_list)
        success_likelihood = float(temp)/4

        if success_likelihood >= random.randint(0, 1):
            self.SOLID = False
            GAME_BOARD.draw_msg("Bravo! You pulled off the heist! Enjoy your intergalactic treasure in the privacy of your enchanted garden.")
            draw_win_map()
        else: 
            GAME_BOARD.draw_msg("Blinded by greed, you attempted this heist without adequate preperation. Back to jail you go.")
            draw_prison()

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = False
    COLLECTIBLE = True

    def interact(self, player):

        player.inventory['rocks'].append(self)
        GAME_BOARD.draw_msg("Ha hah! You've acquired the moon rock! You have %d moon rock in your loot."%(len(player.inventory['rocks'])))


class Boy(GameElement):
    IMAGE = "Boy"
    SOLID = True
    COLLECTIBLE = False

    def interact(self, player):
        draw_prison()
        GAME_BOARD.draw_msg("Turns out the sleeping boy was an incognito guard. Let this be a lesson not to talk to strangers in closed museums.")


class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = True
    COLLECTIBLE = True
    
    def interact(self, player):
        
        if len(player.inventory.get('keys'))> 0:
            self.SOLID = False

            player.inventory['gems'].append(self)
            GAME_BOARD.draw_msg("The gem is yours! You have %d gems."%(len(player.inventory['gems'])))
            
        else:
            GAME_BOARD.draw_msg("You need a key to collect this gem.")
            


class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    COLLECTIBLE = True

    def interact(self, player):

        player.inventory['keys'].append(self)
        GAME_BOARD.draw_msg("You stole a key that you found lying on the ground. You have %d key."%(len(player.inventory['keys'])))


class Character(GameElement):
    IMAGE = "Princess"

    def __init__(self):
        GameElement.__init__(self)
        self.reset_inventory()

    def reset_inventory(self):
        self.inventory = {
            "gems": [],
            "keys": [],
            "rocks": [],
            "bugs": [],
        }
        
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

class Guard(Character):
    IMAGE = "Horns"
    SOLID = True
    COLLECTIBLE = False

    def move_guard(self):

        if DEBUG:
            return 

        direction = random.choice(["up", "down", "left", "right"])
        next_x, next_y = self.next_pos(direction)

        if next_x in range(GAME_WIDTH) and next_y in range(GAME_HEIGHT):

            existing_el = GAME_BOARD.get_el(next_x, next_y)

            if existing_el is None:
                GAME_BOARD.del_el(GUARD.x, GUARD.y)
                GAME_BOARD.set_el(next_x, next_y, GUARD)

    def interact(self, player):
        
        draw_prison()
        GAME_BOARD.draw_msg("Oh no! There are only a few essential employees in the building, but one of them caught you! No more fancy art collecting for you.")

class ShortTree(GameElement):
    IMAGE = "ShortTree"
    SOLID = True
    COLLECTIBLE = False

class GreenGem(GameElement):
    IMAGE = "GreenGem"
    SOLID = True
    COLLECTIBLE = False

class OpenChest(GameElement):
    IMAGE = "OpenChest"
    SOLID = True
    COLLECTIBLE = False

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
        GUARD.move_guard()
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
                item = GAME_BOARD.current_map[PLAYER.y][PLAYER.x]
                ##see if there is something to redraw
                
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                if item in "^OL":
                    draw_item(PLAYER.x, PLAYER.y, item)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)
                ##redraw if applicible

def render_board(board_text):
    '''
    This will draw any board
    '''
    for y in range(len(board_text)):
        row = board_text[y]
        for x in range(len(row)):
            item = board_text[y][x]

            draw_item(x, y, item)
       
def draw_museum():

    map_file = open("game_map.txt")
    map_text_lines = map_file.readlines()
    GAME_BOARD.current_map = map_text_lines

    render_board(map_text_lines)


    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0,3, PLAYER)

    
    GAME_BOARD.register(GUARD)
    GAME_BOARD.set_el(5,2, GUARD)

def draw_prison():

    prison_file = open("prison_cell.txt")
    prison_text_lines = prison_file.readlines()
    GAME_BOARD.current_map = prison_text_lines

    render_board(prison_text_lines)

    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(4,3, PLAYER)

    GAME_BOARD.register(GUARD)
    GAME_BOARD.set_el(2,3, GUARD)

    PLAYER.reset_inventory()

def draw_win_map():

    win_file = open("win_map.txt")
    win_text_lines = win_file.readlines()
    GAME_BOARD.current_map = win_text_lines

    render_board(win_text_lines)

    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,4, PLAYER)

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

    if item == '.':
        GAME_BOARD.del_el(x, y)

    if item == "@":
        star = Star()
        GAME_BOARD.register(star)
        GAME_BOARD.set_el(x, y, star)

    if item == "R":
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(x, y, rock)

    if item == "Z":
        boy = Boy()
        GAME_BOARD.register(boy)
        GAME_BOARD.set_el(x, y, boy)

    if item == "F":
        fake_wall = FakeWall()
        GAME_BOARD.register(fake_wall)
        GAME_BOARD.set_el(x, y, fake_wall)

    if item == "!":
        short_tree = ShortTree()
        GAME_BOARD.register(short_tree)
        GAME_BOARD.set_el(x, y, short_tree)

    if item == "$":
        green_gem = GreenGem()
        GAME_BOARD.register(green_gem)
        GAME_BOARD.set_el(x, y, green_gem)

    if item == "T":
        open_chest = OpenChest()
        GAME_BOARD.register(open_chest)
        GAME_BOARD.set_el(x, y, open_chest)


def initialize():

    global PLAYER
    PLAYER = Character()

    global GUARD
    GUARD = Guard()

    draw_museum()

    GAME_BOARD.draw_msg("Museum Heist, Government Shutdown Edition: As a princess with an eye for rare treasure, you decide to 'peruse' the Smithsonian.")

    keyboard_handler()
    
    #draw_prison()
    #GUARD.move_guard()
