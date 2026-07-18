import pygame
from src.database import Database
from src.settings import *
from src.snake import Snake
from src.food import Food
from src.snake import Snake
from src.food import Food
from ai.ai_agent import AIAgent

pygame.init()

class Game:

    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Enhanced Snake Game")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("comicsansms", 25)

        self.snake = Snake()
        self.food = Food()

        # High Score Load
        self.high_score = 0

        self.db = Database()

        self.db.clear_leaderboard()

        self.player_name = ""

        try:
            with open("highscore.txt", "r") as file:
                self.high_score = int(file.read())
        except(FileNotFoundError, ValueError):
            self.high_score = 0

        self.running = True

        self.game_state = "NAME_INPUT"

        self.game_speed = FPS

        self.score_saved = False

        # AI Autoplay state (toggled with the "A" key)
        self.ai_mode = False
        self.ai_agent = AIAgent()


    def restart_game(self):
        self.snake = Snake()
        self.food = Food()
        self.game_state = "NAME_INPUT"
        self.player_name = ""
        self.score_saved = False


    def save_high_score(self):   
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))


    def save_to_leaderboard(self):
        if not self.score_saved:
            self.db.add_score(self.player_name, self.snake.length - 1)
            self.score_saved = True


    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # Emergency exit from fullscreen
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # Name Input System
                if self.game_state == "NAME_INPUT":

                    if event.key == pygame.K_RETURN:
                        if self.player_name.strip() != "":
                            self.game_state = "PLAYING"

                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]

                    else:
                        if len(self.player_name) < 10:
                            self.player_name += event.unicode

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
                
                 # Toggle AI autoplay mode
                elif event.key == pygame.K_a:
                    self.ai_mode = not self.ai_mode


    def update(self):
        # Stop updating when paused or game over
        if self.game_state != "PLAYING":
            return

        if self.ai_mode:
            dx, dy = self.ai_agent.get_next_direction(self.snake, self.food)
            self.snake.x_change = dx
            self.snake.y_change = dy

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

            self.save_to_leaderboard()

        # Food collision
        if head[0] == self.food.x and head[1] == self.food.y:

            self.food.generate_food()

            self.snake.grow()

            current_score = self.snake.length - 1

            if current_score > self.high_score:
                self.high_score = current_score
                self.save_high_score()

        # Self collision
        for block in list(self.snake.body)[:-1]:

            if block == head:
                self.game_state = "GAME_OVER"

                self.save_to_leaderboard()


    def draw(self):
        if self.game_state == "NAME_INPUT":

            self.window.fill(GREY)

            title = self.font.render("Enter Your Name:", True, BLUE)
            name_text = self.font.render(self.player_name, True, GREEN)
            info = self.font.render("Press ENTER to Start", True, RED)

            self.window.blit(title, [180, 120])
            self.window.blit(name_text, [180, 180])
            self.window.blit(info, [160, 240])

            
            pygame.display.update()
            return

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

        high_score_text = self.font.render(
            f"High Score: {self.high_score}",
            True,
            BLUE
        )

        self.window.blit(high_score_text, [10, 40])

        # Difficulty Display
        difficulty_text = self.font.render(
            f"Speed: {self.game_speed}",
            True,
            BLUE
        )
        self.window.blit(difficulty_text, [10, 70])

        mode_text = self.font.render(
            f"Mode: {'AI' if self.ai_mode else 'Manual'} (Press A to toggle)",
            True,
            BLUE
        )
        self.window.blit(mode_text, [10, 100])

        if self.ai_mode and self.ai_agent.current_path:
            for cell in self.ai_agent.current_path:
                pygame.draw.rect(
                    self.window,
                    (255, 165, 0),
                    [cell[0], cell[1], SNAKE_SIZE, SNAKE_SIZE],
                    1
                )

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

            # Clean white background
            self.window.fill(WHITE)
            # Game Over Message
            game_over_text = self.font.render(
                "GAME OVER!",
                True,
                RED
            )
            restart_text = self.font.render(
                "Press R to Restart",
                True,
                BLUE
            )
            self.window.blit(game_over_text, [210, 60])
            self.window.blit(restart_text, [170, 100])

            # Leaderboard Display
            leaderboard = self.db.get_top_scores()

            y = 170

            title = self.font.render(
                "Leaderboard",
                True,
                BLUE
            )

            self.window.blit(title, [210, y])

            y += 40

            for i, (name, score) in enumerate(leaderboard):

                text = self.font.render(
                    f"{i+1}. {name} - {score}",
                    True,
                    GREEN
                )

                self.window.blit(text, [180, y])

                y += 35
        
        pygame.display.update()


    def run(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(self.game_speed)

        pygame.quit()