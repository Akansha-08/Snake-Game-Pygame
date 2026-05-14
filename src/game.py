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

        self.font = pygame.font.SysFont("comicsansms", 25)

        self.snake = Snake()
        self.food = Food()

        self.running = True

        self.game_state = "PLAYING"

        self.game_speed = FPS

    def restart_game(self):

        self.snake = Snake()

        self.food = Food()

        self.game_state = "PLAYING"

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                # Snake Movement
                if (self.game_state == "PLAYING" and
                    event.key == pygame.K_LEFT and
                    self.snake.x_change == 0
                ):
                    self.snake.x_change = -SNAKE_SIZE
                    self.snake.y_change = 0

                elif (self.game_state == "PLAYING" and
                    event.key == pygame.K_RIGHT and
                    self.snake.x_change == 0
                ):
                    self.snake.x_change = SNAKE_SIZE
                    self.snake.y_change = 0

                elif (self.game_state == "PLAYING" and
                    event.key == pygame.K_UP and
                    self.snake.y_change == 0
                ):
                    self.snake.x_change = 0
                    self.snake.y_change = -SNAKE_SIZE

                elif (self.game_state == "PLAYING" and
                    event.key == pygame.K_DOWN and
                    self.snake.y_change == 0
                ):
                    self.snake.x_change = 0
                    self.snake.y_change = SNAKE_SIZE
                
                # Pause / Resume
                elif event.key == pygame.K_p:

                    if self.game_state == "PLAYING":
                        self.game_state = "PAUSED"

                    elif self.game_state == "PAUSED":
                        self.game_state = "PLAYING"

                # Restart game
                elif event.key == pygame.K_r:

                    if self.game_state == "GAME_OVER":
                        self.restart_game()
                
                # Difficulty levels
                elif event.key == pygame.K_1:
                    self.game_speed = 10

                elif event.key == pygame.K_2:
                    self.game_speed = 15

                elif event.key == pygame.K_3:
                    self.game_speed = 25

    def update(self):

        # Stop updating when paused or game over
        if self.game_state != "PLAYING":
            return

        self.snake.move()

        head = self.snake.body[-1]

        # Wall collision
        if (
            head[0] >= WIDTH or
            head[0] < 0 or
            head[1] >= HEIGHT or
            head[1] < 0
        ):
            self.game_state = "GAME_OVER"

        # Food collision
        if head[0] == self.food.x and head[1] == self.food.y:

            self.food.generate_food()

            self.snake.grow()

        # Self collision
        for block in list(self.snake.body)[:-1]:

            if block == head:
                self.game_state = "GAME_OVER"

    def draw(self):

        self.window.fill(GREY)

        for x in range(0, WIDTH, SNAKE_SIZE):
            pygame.draw.line(
                self.window,
                WHITE,
                (x, 0),
                (x, HEIGHT)
            )

        for y in range(0, HEIGHT, SNAKE_SIZE):
            pygame.draw.line(
                self.window,
                WHITE,
                (0, y),
                (WIDTH, y)
            )

        self.food.draw(self.window)

        self.snake.draw(self.window)

        # Score Display
        score_text = self.font.render(
            f"Score: {self.snake.length - 1}",
            True,
            RED
        )
        self.window.blit(score_text, [10,10])

        # Difficulty Display
        difficulty_text = self.font.render(
            f"Speed: {self.game_speed}",
            True,
            BLUE
        )
        self.window.blit(difficulty_text, [400, 10])

        # Pause Screen
        if self.game_state == "PAUSED":
            pause_text = self.font.render(
                "GAME PAUSED",
                True,
                BLUE
            )
            self.window.blit(pause_text, [220, 180])
        
        # Game Over Screen
        if self.game_state == "GAME_OVER":
            game_over_text = self.font.render(
                "GAME OVER! Press R to Restart",
                True,
                RED
            )
            self.window.blit(game_over_text, [120, 180])
        
        pygame.display.update()

    def run(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(self.game_speed)

        pygame.quit()