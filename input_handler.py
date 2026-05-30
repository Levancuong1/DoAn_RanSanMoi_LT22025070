import pygame
import sys

class InputHandler:
    def __init__(self):
        pass

    def handle_menu_events(self, on_start_classic, on_start_time, on_change_skin):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    on_start_classic()
                elif event.key == pygame.K_2:
                    on_start_time()
                elif event.key == pygame.K_c:
                    on_change_skin()

    def handle_gameplay_events(self, snake, on_toggle_pause):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    on_toggle_pause()
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    snake.change_direction("UP")
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    snake.change_direction("DOWN")
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    snake.change_direction("LEFT")
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    snake.change_direction("RIGHT")

    def handle_pause_events(self, on_toggle_pause):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    on_toggle_pause()

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
