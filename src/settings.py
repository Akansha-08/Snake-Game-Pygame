import pygame

pygame.init()

SNAKE_SIZE = 10

# Height (in px) of the top status ribbon reserved for score/mode/controls.
# Must stay a multiple of SNAKE_SIZE so the grid below it still lines up.
TOP_BAR_HEIGHT = 80

# Detect the laptop's actual screen resolution so the game fills thewhole display. 
# Rounded down to the nearest multiple of SNAKE_SIZE so the grid still lines up perfectly.
_display_info = pygame.display.Info()
WIDTH = (_display_info.current_w // SNAKE_SIZE) * SNAKE_SIZE
HEIGHT = (_display_info.current_h // SNAKE_SIZE) * SNAKE_SIZE

FPS = 15

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (51,102,0)
BLUE = (51,153,255)
GREY = (192,192,192)