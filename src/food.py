import pygame
import random
from src.settings import *

class Food:

    def __init__(self):
        self.generate_food()

    def generate_food(self):

        self.x = random.randrange(0, WIDTH-SNAKE_SIZE, 10)
        # Start below the top status ribbon so food never spawns under it
        self.y = random.randrange(TOP_BAR_HEIGHT, HEIGHT-SNAKE_SIZE, 10)

    def draw(self, window):

        pygame.draw.rect(
            window,
            RED,
            [self.x, self.y, SNAKE_SIZE, SNAKE_SIZE]
        )