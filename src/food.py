import pygame
import random
from src.settings import *

class Food:

    def __init__(self):
        self.generate_food()

    def generate_food(self):

        self.x = random.randrange(0, WIDTH-SNAKE_SIZE, 10)
        self.y = random.randrange(0, HEIGHT-SNAKE_SIZE, 10)

    def draw(self, window):

        pygame.draw.rect(
            window,
            RED,
            [self.x, self.y, SNAKE_SIZE, SNAKE_SIZE]
        )