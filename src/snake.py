from collections import deque
import pygame
from src.settings import *

class Snake:

    def __init__(self):

        self.body = deque()
        self.body.append([WIDTH//2, HEIGHT//2])

        self.x_change = 0
        self.y_change = 0

        self.length = 1

    def move(self):

        head_x = self.body[-1][0] + self.x_change
        head_y = self.body[-1][1] + self.y_change

        new_head = [head_x, head_y]

        self.body.append(new_head)

        if len(self.body) > self.length:
            self.body.popleft()

    def draw(self, window):

        for block in self.body:
            pygame.draw.rect(
                window,
                GREEN,
                [block[0], block[1], SNAKE_SIZE, SNAKE_SIZE]
            )

    def grow(self):
        self.length += 1