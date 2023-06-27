from math import floor
from typing import List
from conf import *
from skin import *
import random

SHAPE_S = [['.....',
            '.....',
            '..**.',
            '.**..',
            '.....'],
           ['.....',
            '..*..',
            '..**.',
            '...*.',
            '.....']]

SHAPE_Z = [['.....',
            '.....',
            '.**..',
            '..**.',
            '.....'],
           ['.....',
            '..*..',
            '.**..',
            '.*...',
            '.....']]

SHAPE_I = [['..*..',
            '..*..',
            '..*..',
            '..*..',
            '.....'],
           ['.....',
            '****.',
            '.....',
            '.....',
            '.....']]

SHAPE_O = [['.....',
            '.....',
            '.**..',
            '.**..',
            '.....']]

SHAPE_J = [['.....',
            '.*...',
            '.***.',
            '.....',
            '.....'],
           ['.....',
            '..**.',
            '..*..',
            '..*..',
            '.....'],
           ['.....',
            '.....',
            '.***.',
            '...*.',
            '.....'],
           ['.....',
            '..*..',
            '..*..',
            '.**..',
            '.....']]

SHAPE_L = [['.....',
            '...*.',
            '.***.',
            '.....',
            '.....'],
           ['.....',
            '..*..',
            '..*..',
            '..**.',
            '.....'],
           ['.....',
            '.....',
            '.***.',
            '.*...',
            '.....'],
           ['.....',
            '.**..',
            '..*..',
            '..*..',
            '.....']]

SHAPE_T = [['.....',
            '..*..',
            '.***.',
            '.....',
            '.....'],
           ['.....',
            '..*..',
            '..**.',
            '..*..',
            '.....'],
           ['.....',
            '.....',
            '.***.',
            '..*..',
            '.....'],
           ['.....',
            '..*..',
            '.**..',
            '..*..',
            '.....']]

SHAPES_LIST = [SHAPE_S, SHAPE_Z, SHAPE_I, SHAPE_O, SHAPE_J, SHAPE_L, SHAPE_T]


class Tetrix_tile:
    def __init__(self, column: int, row: int, shape: List[List]):
        self.x = random.randint(1,column)
        self.y = row
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES_LIST.index(shape)]
        self.rotation = 0

    def get_formatted_shape(self):
        positions = list()
        formatted_shape = self.shape[self.rotation % len(self.shape)]
        for i, line in enumerate(formatted_shape):
            row = list(line)
            for j, column in enumerate(row):
                if column == '*':
                    positions.append((self.x + j, floor(self.y) + i))
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
        return positions

    def in_valid_space(self, grid):
        accepted_pos = [[(j, i) for j in range(NUM_COLUMNS)
                        if grid[i][j] == NULL_COLOR] for i in range(NUM_ROWS)]
        accepted_pos = [pos for sub in accepted_pos for pos in sub]
        formatted_shape = self.get_formatted_shape()
        for pos in formatted_shape:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True
