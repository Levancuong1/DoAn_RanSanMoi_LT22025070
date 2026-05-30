import pygame
import json
import os
import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BLACK, INITIAL_SPEED, SPEED_INCREMENT, SCORE_INCREMENT, BLOCK_SIZE, COLOR_GRID, COLOR_GRAY, TIME_ATTACK_LIMIT
from snake import Snake
from food import Food
from ui import UI
from input_handler import InputHandler

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game Ultimate - Lê Văn Cường - LT22025070")
        self.clock = pygame.time.Clock()
        
        self.snake = Snake()
        self.food = Food(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.ui = UI(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.input_handler = InputHandler()
        
        self.state = "MENU"
        self.score = 0
        self.level = 1
        self.game_mode = "CLASSIC"
        self.leader_board = [0, 0, 0, 0, 0]
        self.unlocked_achievements = []
        self.newly_unlocked_this_run = []
        self.obstacles = []
        self.is_new_record = False
        
        self.shake_timer = 0
        self.shake_intensity = 0
        self.offset_x = 0
        self.offset_y = 0
        
        self.golden_food_eaten_count = 0
        self.survival_timer = 0
        self.time_attack_remaining = TIME_ATTACK_LIMIT
        self.last_update_time = 0
        
        self.load_game_data()
        self.generate_obstacles()
        self.food.randomize_position(self.snake.body, self.obstacles)

    def load_game_data(self):
        if os.path.exists("highscore.json"):
            try:
                with open("highscore.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.leader_board = data.get("leaderboard", [0, 0, 0, 0, 0])
                    self.leader_board.sort(reverse=True)
                    self.leader_board = self.leader_board[:5]
                    self.unlocked_achievements = data.get("achievements", [])
            except:
                self.leader_board = [0, 0, 0, 0, 0]
                self.unlocked_achievements = []

    def save_game_data(self):
        self.is_new_record = False
        if self.score > min(self.leader_board):
            self.is_new_record = True
            self.leader_board.append(self.score)
            self.leader_board.sort(reverse=True)
            self.leader_board = self.leader_board[:5]
            
        for ach in self.newly_unlocked_this_run:
            if ach not in self.unlocked_achievements:
                self.unlocked_achievements.append(ach)
                
        with open("highscore.json", "w", encoding="utf-8") as f:
            json.dump({
                "leaderboard": self.leader_board,
                "achievements": self.unlocked_achievements
            }, f, ensure_ascii=False)

    def check_achievements_at_end(self):
        self.newly_unlocked_this_run = []
        if self.score >= SCORE_INCREMENT and "Tan binh" not in self.unlocked_achievements:
            self.newly_unlocked_this_run.append("Tan binh")
        if self.score >= 100 and "Dung si diet moi" not in self.unlocked_achievements:
            self.newly_unlocked_this_run.append("Dung si diet moi")
        if self.game_mode == "TIME" and self.survival_timer >= 30000 and "Than toc" not in self.unlocked_achievements:
            self.newly_unlocked_this_run.append("Than toc")
        if self.golden_food_eaten_count >= 3 and "Ke san vang" not in self.unlocked_achievements:
            self.newly_unlocked_this_run.append("Ke san vang")

    def trigger_shake(self, duration, intensity):
        self.shake_timer = duration
        self.shake_intensity = intensity

    def toggle_pause(self):
        if self.state == "PLAYING":
            self.state = "PAUSED"
        elif self.state == "PAUSED":
            self.state = "PLAYING"
            self.last_update_time = pygame.time.get_ticks()

    def generate_obstacles(self):
        self.obstacles = []
        if self.level == 2:
            for x in range(200, 600, BLOCK_SIZE):
                self.obstacles.append((x, 160))
                self.obstacles.append((x, 440))
        elif self.level == 3:
            for y in range(140, 460, BLOCK_SIZE):
                self.obstacles.append((240, y))
                self.obstacles.append((560, y))

    def start_classic_game(self):
        self.game_mode = "CLASSIC"
        self.state = "PLAYING"
        self.survival_timer = 0
        self.golden_food_eaten_count = 0
        self.last_update_time = pygame.time.get_ticks()

    def start_time_game(self):
        self.game_mode = "TIME"
        self.time_attack_remaining = TIME_ATTACK_LIMIT
        self.state = "PLAYING"
        self.survival_timer = 0
        self.golden_food_eaten_count = 0
        self.last_update_time = pygame.time.get_ticks()

    def change_snake_skin(self):
        self.snake.change_skin()

    def reset_game(self):
        self.snake.reset()
        self.score = 0
        self.level = 1
        self.generate_obstacles()
        self.food.randomize_position(self.snake.body, self.obstacles)
        self.state = "MENU"

    def update(self):
        if self.state == "PLAYING":
            current_time = pygame.time.get_ticks()
            delta_time = current_time - self.last_update_time
            self.last_update_time = current_time
            
            self.survival_timer += delta_time
            
            if self.shake_timer > 0:
                self.shake_timer -= delta_time
                self.offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
                self.offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            else:
                self.offset_x = 0
                self.offset_y = 0

            if self.game_mode == "TIME":
                self.time_attack_remaining -= delta_time
                if self.time_attack_remaining <= 0:
                    self.trigger_shake(300, 8)
                    self.check_achievements_at_end()
                    self.save_game_data()
                    self.state = "GAME_OVER"
                    return

            self.food.update()
            next_head = self.snake.get_next_head_position()
            
            if next_head == self.food.position:
                self.food.trigger_burst()
                
                if self.food.type == "GOLDEN":
                    self.score += SCORE_INCREMENT * 2
                    self.golden_food_eaten_count += 1
                    self.trigger_shake(200, 5)
                else:
                    self.score += SCORE_INCREMENT
                
                if self.game_mode == "TIME":
                    self.time_attack_remaining = TIME_ATTACK_LIMIT

                self.snake.move(grow=True)
                
                new_level = 1 + (self.score // 100)
                if new_level != self.level:
                    self.level = min(new_level, 3)
                    self.generate_obstacles()
                    
                self.food.randomize_position(self.snake.body, self.obstacles)
            else:
                self.snake.move(grow=False)

            if self.snake.check_collision(WINDOW_WIDTH, WINDOW_HEIGHT, self.obstacles):
                self.trigger_shake(400, 10)
                self.check_achievements_at_end()
                self.save_game_data()
                self.state = "GAME_OVER"

    def render(self):
        if self.state == "MENU":
            self.ui.draw_menu(self.screen, self.leader_board, self.snake.skin_index, self.unlocked_achievements)
        elif self.state in ["PLAYING", "PAUSED"]:
            self.screen.fill(COLOR_BLACK)
            for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
                pygame.draw.line(self.screen, COLOR_GRID, (x + self.offset_x, 0), (x + self.offset_x, WINDOW_HEIGHT))
            for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
                pygame.draw.line(self.screen, COLOR_GRID, (0, y + self.offset_y), (WINDOW_WIDTH, y + self.offset_y))
                
            for block in self.obstacles:
                pygame.draw.rect(self.screen, COLOR_GRAY, (block[0] + self.offset_x, block[1] + self.offset_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
                pygame.draw.rect(self.screen, (50, 50, 55), (block[0] + self.offset_x, block[1] + self.offset_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
                
            self.snake.draw(self.screen, self.offset_x, self.offset_y)
            self.food.draw(self.screen, self.offset_x, self.offset_y)
            self.ui.draw_gameplay(self.screen, self.score, self.level, self.food.type == "GOLDEN", self.game_mode, self.time_attack_remaining)
            
            if self.state == "PAUSED":
                self.ui.draw_pause(self.screen)
        elif self.state == "GAME_OVER":
            self.ui.draw_game_over(self.screen, self.score, self.is_new_record, self.newly_unlocked_this_run)
        pygame.display.flip()

    def run(self):
        while True:
            if self.state == "MENU":
                self.input_handler.handle_menu_events(self.start_classic_game, self.start_time_game, self.change_snake_skin)
            elif self.state == "PLAYING":
                self.input_handler.handle_gameplay_events(self.snake, self.toggle_pause)
                self.update()
            elif self.state == "PAUSED":
                self.input_handler.handle_pause_events(self.toggle_pause)
            elif self.state == "GAME_OVER":
                self.input_handler.handle_game_over_events(self.reset_game)
            
            self.render()
            current_speed = INITIAL_SPEED + (self.level * SPEED_INCREMENT)
            if self.food.type == "GOLDEN":
                current_speed *= 1.5
            self.clock.tick(current_speed)
