import numpy
import pygame

shape = [
    [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [1, 1, 1, 1]],

    [[0, 0, 0, 0],
     [1, 1, 0, 0],
     [0, 1, 0, 0],
     [0, 1, 0, 0]],

    [[0, 0, 0, 0],
     [1, 1, 0, 0],
     [1, 0, 0, 0],
     [1, 0, 0, 0]],

    [[0, 0, 0, 0],
     [1, 0, 0, 0],
     [1, 1, 0, 0],
     [1, 0, 0, 0]],

    [[0, 0, 0, 0],
     [0, 1, 0, 0],
     [1, 1, 0, 0],
     [1, 0, 0, 0]],

    [[0, 0, 0, 0],
     [1, 0, 0, 0],
     [1, 1, 0, 0],
     [0, 1, 0, 0]],

    [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [1, 1, 0, 0],
     [1, 1, 0, 0]]
]

# I, L, L', T, /, \, o

color = [(78, 173, 234), (240, 150, 87), (158, 110, 205),
         (187, 39, 149), (196, 41, 28), (159, 206, 99), (245, 194, 66)]

class Tetrix_tiles:
    def __init__(self, type, pos):
        self.shape = shape[type]
        self.color = type
        self.pos = pos
        pass
