import pygame, sys, random
from pygame.math import Vector2
import asyncio

pygame.init()

title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)
level_font = pygame.font.Font(None, 30)

BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (98, 0, 238)
SNAKE_COLOR = (0, 255, 127)
FOOD_COLOR = (255, 215, 0)

cell_size = 30
number_of_cells = 25

OFFSET = 75

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, 
                                cell_size, cell_size)
        pygame.draw.ellipse(screen, FOOD_COLOR, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells-1)
        y = random.randint(0, number_of_cells-1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1, 0)
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            segment_rect = pygame.Rect(OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size,
                                       cell_size, cell_size)
            pygame.draw.rect(screen, SNAKE_COLOR, segment_rect)

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1, 0)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
        self.level = 1

    def draw(self):
        self.food.draw()
        self.snake.draw()
        if self.state == "STOPPED":
            temp = self.score
            game_over_surface = title_font.render(f'Game Over! Final Score: {temp}', True, BORDER_COLOR)
            game_over_rect = game_over_surface.get_rect(center=(OFFSET + number_of_cells * cell_size / 2, OFFSET + number_of_cells * cell_size / 2))
            screen.blit(game_over_surface, game_over_rect)
            sleep_surface = title_font.render("Press SPACE to play again", True, BORDER_COLOR)
            sleep_rect = sleep_surface.get_rect(center=(OFFSET + number_of_cells * cell_size / 2, OFFSET + number_of_cells * cell_size / 2 + 60))
            screen.blit(sleep_surface, sleep_rect)

            # self.score = 0

    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            if self.score % 5 == 0:
                self.level += 1
                pygame.time.set_timer(SNAKE_UPDATE, max(50, 200 - self.level * 20))

    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        self.level = 1

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

screen = pygame.display.set_mode((2*OFFSET + cell_size*number_of_cells, 2*OFFSET + cell_size*number_of_cells))
pygame.display.set_caption("Retro Snake")

clock = pygame.time.Clock()

game = Game()

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

async def main():
    while True:
        for event in pygame.event.get():
            if event.type == SNAKE_UPDATE:
                game.update()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game.state == "STOPPED" and event.key == pygame.K_SPACE:
                    game.state = "RUNNING"
                    game.score = 0
                    game.level = 1
                if game.state == "RUNNING":
                    if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                        game.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                        game.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                        game.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                        game.snake.direction = Vector2(1, 0)

        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, BORDER_COLOR, 
                         (OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)
        game.draw()
        if game.state != "STOPPED":
            title_surface = title_font.render("World of Snake! Player Name: Sanket", True, BORDER_COLOR)
            score_surface = score_font.render(f'Score: {game.score}', True, BORDER_COLOR)
            level_surface = score_font.render(f'Level: {game.level}', True, BORDER_COLOR)
            screen.blit(title_surface, (OFFSET, 20))
            screen.blit(score_surface, (OFFSET-5, OFFSET + cell_size*number_of_cells + 10))
            screen.blit(level_surface, (OFFSET + 250, OFFSET + cell_size*number_of_cells + 10))
        
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
