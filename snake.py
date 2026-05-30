import pygame
from config import BLOCK_SIZE, COLOR_GREEN, COLOR_DARK_GREEN

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = "RIGHT"

    def change_direction(self, new_direction):
        opposites = {("UP", "DOWN"), ("DOWN", "UP"), ("LEFT", "RIGHT"), ("RIGHT", "LEFT")}
        if (self.direction, new_direction) not in opposites and (new_direction, self.direction) not in opposites:
            self.direction = new_direction

    def get_next_head_position(self):
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            return (head_x, head_y - BLOCK_SIZE)
        elif self.direction == "DOWN":
            return (head_x, head_y + BLOCK_SIZE)
        elif self.direction == "LEFT":
            return (head_x - BLOCK_SIZE, head_y)
        elif self.direction == "RIGHT":
            return (head_x + BLOCK_SIZE, head_y)
        return (head_x, head_y)

    def move(self, grow=False):
        new_head = self.get_next_head_position()
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()

    def check_collision(self, width, height):
        head = self.body[0]
        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            return True
        if head in self.body[1:]:
            return True
        return False

    def draw(self, surface):
        for index, block in enumerate(self.body):
            color = COLOR_DARK_GREEN if index == 0 else COLOR_GREEN
            pygame.draw.rect(surface, color, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))