import pygame
import random
import math
from config import BLOCK_SIZE, COLOR_RED, COLOR_YELLOW

class Food:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = (0, 0)
        self.type = "NORMAL"
        self.spawn_time = 0
        self.animation_angle = 0  
        self.burst_particles = [] 

    def randomize_position(self, snake_body, obstacles):
        max_x = (self.width // BLOCK_SIZE) - 1
        max_y = (self.height // BLOCK_SIZE) - 1
        
        if random.random() < 0.25:
            self.type = "GOLDEN"
            self.spawn_time = pygame.time.get_ticks()
        else:
            self.type = "NORMAL"

        while True:
            x = random.randint(0, max_x) * BLOCK_SIZE
            y = random.randint(0, max_y) * BLOCK_SIZE
            if (x, y) not in snake_body and (x, y) not in obstacles:
                self.position = (x, y)
                break

    def trigger_burst(self):
        color = COLOR_YELLOW if self.type == "GOLDEN" else COLOR_RED
        center_x = self.position[0] + BLOCK_SIZE // 2
        center_y = self.position[1] + BLOCK_SIZE // 2
        for _ in range(15):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 5)
            self.burst_particles.append({
                "x": center_x,
                "y": center_y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "radius": random.randint(2, 5),
                "alpha": 255,
                "color": color
            })

    def update(self):
        if self.type == "GOLDEN":
            if pygame.time.get_ticks() - self.spawn_time > 5000:
                self.type = "NORMAL"
                
        self.animation_angle += 0.15
        if self.animation_angle > math.pi * 2:
            self.animation_angle = 0

        for p in self.burst_particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["alpha"] -= 12
            p["radius"] -= 0.08
            if p["alpha"] <= 0 or p["radius"] <= 0:
                self.burst_particles.remove(p)

    def draw(self, surface, offset_x=0, offset_y=0):
        for p in self.burst_particles:
            p_surface = pygame.Surface((p["radius"] * 2, p["radius"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(p_surface, (*p["color"], int(p["alpha"])), (int(p["radius"]), int(p["radius"])), int(p["radius"]))
            surface.blit(p_surface, (int(p["x"] - p["radius"]) + offset_x, int(p["y"] - p["radius"]) + offset_y))

        pulse_modifier = math.sin(self.animation_angle) * 2  
        base_radius = BLOCK_SIZE // 2 - 1
        current_radius = max(4, int(base_radius + pulse_modifier))
        
        center_x = self.position[0] + BLOCK_SIZE // 2 + offset_x
        center_y = self.position[1] + BLOCK_SIZE // 2 + offset_y
        
        color = COLOR_YELLOW if self.type == "GOLDEN" else COLOR_RED
        glow_color = (255, 215, 0, 60) if self.type == "GOLDEN" else (255, 65, 54, 60)
        
        glow_surf = pygame.Surface((BLOCK_SIZE * 2, BLOCK_SIZE * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, glow_color, (BLOCK_SIZE, BLOCK_SIZE), current_radius + 6)
        surface.blit(glow_surf, (center_x - BLOCK_SIZE, center_y - BLOCK_SIZE))
        
        pygame.draw.circle(surface, color, (center_x, center_y), current_radius)
        pygame.draw.circle(surface, (255, 255, 255), (center_x - 2, center_y - 2), 2)
