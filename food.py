import pygame
import random
from config import BLOCK_SIZE, COLOR_RED

class Food:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = (0, 0)

    def randomize_position(self, snake_body):
        max_x = (self.width // BLOCK_SIZE) - 1
        max_y = (self.height // BLOCK_SIZE) - 1
        while True:
            x = random.randint(0, max_x) * BLOCK_SIZE
            y = random.randint(0, max_y) * BLOCK_SIZE
            if (x, y) not in snake_body:
                self.position = (x, y)
                break

    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))