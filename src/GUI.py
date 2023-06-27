import random
import numpy as np
from typing import List, Tuple, Dict
import pygame
from tile import *


class TetriX_GUI:
    def __init__(self):
        self.grid = [[NULL_COLOR for _ in range(NUM_COLUMNS)]
                     for _ in range(NUM_ROWS)]
        self.score = 0
        self.locked_pos = dict()
        self.game_running = True
        self.game_over = False
        self.current_piece = Tetrix_tile(5, 0, random.choice(SHAPES_LIST))
        self.next_piece = Tetrix_tile(5, 0, random.choice(SHAPES_LIST))
        self.change_current_piece = False
        self.game_clock = pygame.time.Clock()
        self.fall_time = 0
        self.fall_speed = INIT_SPEED
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def set_grid(self):
        for i, g in enumerate(self.grid):
            for j, _ in enumerate(g):
                if (j, i) in self.locked_pos:
                    self.grid[i][j] = self.locked_pos[(j, i)]
                else:
                    self.grid[i][j] = NULL_COLOR
        return self.grid

    def check_game_over(self):
        for pos in self.locked_pos:
            x, y = pos
            if y < 0:
                return True
        return False

    def clear_rows(self):
        num_cleared_rows = 0
        for i in range(len(self.grid)):
            if NULL_COLOR in self.grid[i]:
                continue
            num_cleared_rows += 1
            for j in range(len(self.grid[i])):
                if (j, i) in self.locked_pos.keys():
                    del self.locked_pos[(j, i)]
            temp_locked_pos = dict()
            for pos, val in self.locked_pos.items():
                x, y = pos
                if y < i:
                    temp_locked_pos[(x, y + 1)] = val
                else:
                    temp_locked_pos[(x, y)] = val
            self.locked_pos = temp_locked_pos
        self.score += REWARD[num_cleared_rows]

    def draw_game_window(self):
        self.window.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont(FONT, FONT_SIZE)
        label = font.render('TetriX', 1, FONT_COLOR)
        self.window.blit(
            label, (ORIGIN[0] + PLAY_WIDTH / 2 - (label.get_width() / 2), 10))
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(self.window, self.grid[i][j],
                                 (ORIGIN[0] + j * BLOCK_SIZE, ORIGIN[1] + i * BLOCK_SIZE,
                                     BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(self.window, EDGE_COLOR,
                                 (ORIGIN[0] + j * BLOCK_SIZE, ORIGIN[1] + i * BLOCK_SIZE,
                                     BLOCK_SIZE, BLOCK_SIZE), 1)

        pygame.draw.rect(self.window, EDGE_COLOR,
                         (ORIGIN[0], ORIGIN[1],
                             PLAY_WIDTH, PLAY_HEIGHT), 4)
        font = pygame.font.SysFont(FONT, FONT_SIZE)
        label = font.render('SCORE', 1, FONT_COLOR)
        start_x = ORIGIN[0] + PLAY_WIDTH + 20
        start_y = ORIGIN[1] + PLAY_HEIGHT / 2 + 70
        self.window.blit(label, (start_x + 10, start_y - 120))
        label = font.render(str(self.score), 1, FONT_COLOR)
        self.window.blit(label, (start_x + 10, start_y - 90))
        label = font.render('Next Tile', 1, FONT_COLOR)
        self.window.blit(label, (start_x + 10, start_y - 30))
        formatted_shape = self.next_piece.shape[self.next_piece.rotation % len(
            self.next_piece.shape)]
        for i, line in enumerate(formatted_shape):
            row = list(line)
            for j, column in enumerate(row):
                if column == '*':
                    pygame.draw.rect(self.window, self.next_piece.color,
                                     (start_x + j * BLOCK_SIZE, start_y + i * BLOCK_SIZE,
                                         BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(self.window, EDGE_COLOR,
                                     (start_x + j * BLOCK_SIZE, start_y + i * BLOCK_SIZE,
                                         BLOCK_SIZE, BLOCK_SIZE), 1)

    def get_grid_state(self):
        matrix = np.zeros((NUM_ROWS, NUM_COLUMNS))
        non_null_indices = np.where(self.grid != NULL_COLOR)
        matrix[non_null_indices] = 1
        return matrix

    def play_game(self, action=None):
        self.grid = self.set_grid()
        self.fall_time += self.game_clock.get_rawtime()
        self.game_clock.tick()
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            self.fall_speed /= ACCEL_RATE
            self.current_piece.y += 1
            if not self.current_piece.in_valid_space(self.grid) and self.current_piece.y > 0:
                self.current_piece.y -= 1
                self.change_current_piece = True

        if action is not None:
            if action == LEFT_KEY:
                self.current_piece.x -= 1
            elif action == RIGHT_KEY:
                self.current_piece.x += 1
            elif action == ROTATE_KEY:
                self.current_piece.rotation = (
                    self.current_piece.rotation + 1) % len(self.current_piece.shape)
            elif action == DOWN_KEY:
                self.current_piece.y += 0.2
            elif action == DROP_KEY:
                while self.current_piece.in_valid_space(self.grid):
                    self.current_piece.y += 1
                self.current_piece.y -= 1

            if not self.current_piece.in_valid_space(self.grid):
                if action == LEFT_KEY:
                    self.current_piece.x += 1
                elif action == RIGHT_KEY:
                    self.current_piece.x -= 1
                elif action == ROTATE_KEY:
                    self.current_piece.rotation = (
                        self.current_piece.rotation - 1) % len(self.current_piece.shape)
                elif action == DOWN_KEY:
                    self.current_piece.y -= 0.2

        formatter_shape = self.current_piece.get_formatted_shape()
        for i in range(len(formatter_shape)):
            x, y = formatter_shape[i]
            if y > -1:
                self.grid[y][x] = self.current_piece.color

        if self.change_current_piece:
            for pos in formatter_shape:
                p = (pos[0], pos[1])
                self.locked_pos[p] = self.current_piece.color
            self.current_piece = self.next_piece
            self.next_piece = Tetrix_tile(5, 0, random.choice(SHAPES_LIST))
            self.fall_speed = INIT_SPEED
            self.change_current_piece = False
            self.clear_rows()
        self.draw_game_window()
        pygame.display.update()
