import pygame
from src.settings import *
from src.snake import Snake
from src.food import Food

pygame.init()

class Game:

    def __init__(self):

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Enhanced Snake Game")

        self.clock = pygame.time.Clock()

        self.snake = Snake()
        self.food = Food()

        self.running = True

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    self.snake.x_change = -SNAKE_SIZE
                    self.snake.y_change = 0

                elif event.key == pygame.K_RIGHT:
                    self.snake.x_change = SNAKE_SIZE
                    self.snake.y_change = 0

                elif event.key == pygame.K_UP:
                    self.snake.x_change = 0
                    self.snake.y_change = -SNAKE_SIZE

                elif event.key == pygame.K_DOWN:
                    self.snake.x_change = 0
                    self.snake.y_change = SNAKE_SIZE

    def update(self):

        self.snake.move()

    def draw(self):

        self.window.fill(GREY)

        self.food.draw(self.window)

        self.snake.draw(self.window)

        pygame.display.update()

    def run(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()