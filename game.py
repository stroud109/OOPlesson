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

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True


class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = True
    
    def interact(self, player):
        player.inventory['gems'] = []

        if len(player.inventory['keys'])> 0:
            self.SOLID = False
            gems = player.inventory.get('gems', [])
            gems.append(self)

            #'gems' is the key, gems is the list of jewels.

            player.inventory['gems'] = gems 
            GAME_BOARD.draw_msg("You just acquired a gem! You have %d gems!"%(len(player.inventory['gems'])))
        else:
            GAME_BOARD.draw_msg("You need a key to collect a gem!")


class Key(GameElement):
    IMAGE = "Key"
    SOLID = False

    def interact(self, player):
        keys = player.inventory.get('keys', [])
        keys.append(self)

        player.inventory['keys'] = keys
        GAME_BOARD.draw_msg("You just acquired a key! You have %d keys!"%(len(player.inventory['keys'])))


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
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)

       


def initialize():
    """Put game initialization code here"""
    rock_positions = [
        (2, 1),
        (1, 2),
        (3, 2),
        (2, 3)
        ]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False

    for rock in rocks:
        print rock

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,2, PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("Princess Game!!!")

    gem1 = Gem()
    GAME_BOARD.register(gem1)
    GAME_BOARD.set_el(3, 1, gem1)

    key1 = Key()
    GAME_BOARD.register(key1)
    GAME_BOARD.set_el(4,4, key1)

    key2 = Key()
    GAME_BOARD.register(key2)
    GAME_BOARD.set_el(2,7, key2)

    keyboard_handler()