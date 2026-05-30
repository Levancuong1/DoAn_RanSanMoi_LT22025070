import pygame
from config import COLOR_WHITE, COLOR_GREEN, COLOR_RED

class UI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_title = pygame.font.SysFont("Segoe UI", 50, bold=True)
        self.font_body = pygame.font.SysFont("Segoe UI", 28)

    def draw_menu(self, surface):
        surface.fill((0, 0, 0))
        title = self.font_title.render("SNAKE GAME", True, COLOR_GREEN)
        prompt = self.font_body.render("Press SPACE to Play", True, COLOR_WHITE)
        student_info = self.font_body.render("Sinh viên: Lê Văn Cường - MSV: LT22025070", True, COLOR_WHITE)
        
        surface.blit(title, (self.width // 2 - title.get_width() // 2, 180))
        surface.blit(prompt, (self.width // 2 - prompt.get_width() // 2, 300))
        surface.blit(student_info, (self.width // 2 - student_info.get_width() // 2, 380))

    def draw_gameplay(self, surface, score):
        score_text = self.font_body.render(f"Score: {score}", True, COLOR_WHITE)
        surface.blit(score_text, (15, 15))

    def draw_game_over(self, surface, score):
        surface.fill((0, 0, 0))
        title = self.font_title.render("GAME OVER", True, COLOR_RED)
        score_text = self.font_body.render(f"Final Score: {score}", True, COLOR_WHITE)
        prompt = self.font_body.render("Press R to Replay or ESC to Exit", True, COLOR_WHITE)
        surface.blit(title, (self.width // 2 - title.get_width() // 2, 160))
        surface.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 280))
        surface.blit(prompt, (self.width // 2 - prompt.get_width() // 2, 380))