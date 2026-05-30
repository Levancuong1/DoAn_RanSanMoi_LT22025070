import pygame
import sys

class InputHandler:
    def __init__(self):
        pass

    def handle_menu_events(self, on_start):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    on_start()

    def handle_gameplay_events(self, snake):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    snake.change_direction("UP")
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    snake.change_direction("DOWN")
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    snake.change_direction("LEFT")
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    snake.change_direction("RIGHT")

    def handle_game_over_events(self, on_replay):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    on_replay()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()