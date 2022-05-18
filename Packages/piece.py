from enum import Enum
from pprint import pprint

from .constants import BLUE, WHITE, RED, SQUARE_SIZE, GREY, CROWN, ROCKET
import pygame



class Direction(Enum):
    Top = 0
    TopRight = 1
    Right = 2
    BottomRight = 3
    Bottom = 4
    BottomLeft = 5
    Left = 6
    TopLeft = 7

DIR_TO_ANGLE = {key: key.value * -45 for key in Direction}


class Piece:
    PADDING = 15
    OUTLINE = 3
    
    def __init__(self, row, col, color, dir):
        self.row = row
        self.col = col
        self.color = color
        self.dir = dir
        self.x = 0
        self.y = 0
        self.calc_pos()
        self.rocketNr = 0
        self.allow_movement = 0

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, RED, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        spinned = pygame.transform.rotate(CROWN, DIR_TO_ANGLE[self.dir])
        win.blit(spinned, (self.x - spinned.get_width() // 2, self.y - spinned.get_height() // 2))
        rocket = pygame.transform.rotate(ROCKET, DIR_TO_ANGLE[self.dir])
     

        if self.rocketNr == 1:
            win.blit(rocket, (self.x - rocket.get_width() + 25, self.y - rocket.get_height() - 5))
            return
        elif self.rocketNr == 2:
            win.blit(rocket, (self.x - rocket.get_width() + 25, self.y - rocket.get_height() - 5))
            win.blit(rocket, (self.x - rocket.get_width() - 5, self.y - rocket.get_height() - 5))
            return
               
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def moveDir(self, amount):
        self.dir = Direction((self.dir.value + amount) % len(Direction))       

    def __repr__(self):
        return str(self.color)