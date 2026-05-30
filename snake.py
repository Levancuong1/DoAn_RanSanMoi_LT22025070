import pygame
import random
from config import BLOCK_SIZE, SKINS

class Snake:
    def __init__(self):
        self.skin_index = 0
        self.reset()

    def reset(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = "RIGHT"
        self.particles = []  

    def change_skin(self):
        self.skin_index = (self.skin_index + 1) % len(SKINS)

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
        
        tail = self.body[-1]
        self.particles.append({
            "x": tail[0] + BLOCK_SIZE // 2 + random.randint(-3, 3),
            "y": tail[1] + BLOCK_SIZE // 2 + random.randint(-3, 3),
            "radius": random.randint(3, 6),
            "alpha": 150,
            "color": SKINS[self.skin_index]["tail"]
        })
        
        if not grow:
            self.body.pop()
            
        for p in self.particles[:]:
            p["alpha"] -= 8  
            p["radius"] -= 0.1  
            if p["alpha"] <= 0 or p["radius"] <= 0:
                self.particles.remove(p)

    def check_collision(self, width, height, obstacles):
        head = self.body[0]
        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            return True
        if head in self.body[1:]:
            return True
        if head in obstacles:
            return True
        return False

    def draw(self, surface, offset_x=0, offset_y=0):
        current_skin = SKINS[self.skin_index]
        head_color = current_skin["head"]
        tail_color = current_skin["tail"]

        for p in self.particles:
            p_surface = pygame.Surface((p["radius"] * 2, p["radius"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(p_surface, (*p["color"], int(p["alpha"])), (int(p["radius"]), int(p["radius"])), int(p["radius"]))
            surface.blit(p_surface, (int(p["x"] - p["radius"]) + offset_x, int(p["y"] - p["radius"]) + offset_y))

        for index, block in enumerate(self.body):
            if len(self.body) > 1:
                t = index / (len(self.body) - 1)
            else:
                t = 0
            r = int(head_color[0] + (tail_color[0] - head_color[0]) * t)
            g = int(head_color[1] + (tail_color[1] - head_color[1]) * t)
            b = int(head_color[2] + (tail_color[2] - head_color[2]) * t)
            current_color = (r, g, b)

            bx = block[0] + offset_x
            by = block[1] + offset_y

            if index == 0:
                pygame.draw.rect(surface, current_color, (bx, by, BLOCK_SIZE, BLOCK_SIZE), border_radius=8)
                pygame.draw.rect(surface, (255, 255, 255, 70), (bx+2, by+2, BLOCK_SIZE-4, BLOCK_SIZE//2), border_radius=4)
                
                eye_color = (255, 255, 255)
                pupil_color = (10, 10, 15)  
                if self.direction in ["RIGHT", "LEFT"]:
                    pygame.draw.circle(surface, eye_color, (bx + BLOCK_SIZE//2, by + 5), 3)
                    pygame.draw.circle(surface, pupil_color, (bx + BLOCK_SIZE//2 + (2 if self.direction=="RIGHT" else -2), by + 5), 1)
                    pygame.draw.circle(surface, eye_color, (bx + BLOCK_SIZE//2, by + BLOCK_SIZE - 5), 3)
                    pygame.draw.circle(surface, pupil_color, (bx + BLOCK_SIZE//2 + (2 if self.direction=="RIGHT" else -2), by + BLOCK_SIZE - 5), 1)
                else:
                    pygame.draw.circle(surface, eye_color, (bx + 5, by + BLOCK_SIZE//2), 3)
                    pygame.draw.circle(surface, pupil_color, (bx + 5, by + BLOCK_SIZE//2 + (2 if self.direction=="DOWN" else -2)), 1)
                    pygame.draw.circle(surface, eye_color, (bx + BLOCK_SIZE - 5, by + BLOCK_SIZE//2), 3)
                    pygame.draw.circle(surface, pupil_color, (bx + BLOCK_SIZE - 5, by + BLOCK_SIZE//2 + (2 if self.direction=="DOWN" else -2)), 1)
            else:
                pygame.draw.rect(surface, current_color, (bx, by, BLOCK_SIZE, BLOCK_SIZE), border_radius=5)
                pygame.draw.rect(surface, (255, 255, 255, 45), (bx+2, by+2, BLOCK_SIZE-4, BLOCK_SIZE//2-1), border_radius=2)
