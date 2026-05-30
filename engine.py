import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_DARK_GRAY, INITIAL_SPEED, SPEED_INCREMENT, SCORE_INCREMENT
from snake import Snake
from food import Food
from ui import UI
from input_handler import InputHandler

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game - Đồ Án Python - Lê Văn Cường")
        self.clock = pygame.time.Clock()
        
        self.snake = Snake()
        self.food = Food(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.ui = UI(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.input_handler = InputHandler()
        
        self.state = "MENU"
        self.score = 0
        self.speed = INITIAL_SPEED
        self.food.randomize_position(self.snake.body)

    def start_game(self):
        self.state = "PLAYING"

    def reset_game(self):
        self.snake.reset()
        self.score = 0
        self.speed = INITIAL_SPEED
        self.food.randomize_position(self.snake.body)
        self.state = "PLAYING"

    def update(self):
        if self.state == "PLAYING":
            next_head = self.snake.get_next_head_position()
            if next_head == self.food.position:
                self.snake.move(grow=True)
                self.score += SCORE_INCREMENT
                self.speed = INITIAL_SPEED + (self.score // (SCORE_INCREMENT * 3)) * SPEED_INCREMENT
                self.food.randomize_position(self.snake.body)
            else:
                self.snake.move(grow=False)

            if self.snake.check_collision(WINDOW_WIDTH, WINDOW_HEIGHT):
                self.state = "GAME_OVER"

    def render(self):
        if self.state == "MENU":
            self.ui.draw_menu(self.screen)
        elif self.state == "PLAYING":
            self.screen.fill(COLOR_DARK_GRAY)
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.ui.draw_gameplay(self.screen, self.score)
        elif self.state == "GAME_OVER":
            self.ui.draw_game_over(self.screen, self.score)
        pygame.display.flip()

    def run(self):
        while True:
            if self.state == "MENU":
                self.input_handler.handle_menu_events(self.start_game)
            elif self.state == "PLAYING":
                self.input_handler.handle_gameplay_events(self.snake)
                self.update()
            elif self.state == "GAME_OVER":
                self.input_handler.handle_game_over_events(self.reset_game)
            
            self.render()
            self.clock.tick(self.speed)