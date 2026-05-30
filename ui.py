import pygame
from config import COLOR_WHITE, COLOR_GREEN, COLOR_RED, COLOR_YELLOW, COLOR_GRAY, SKINS

class UI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_title = pygame.font.SysFont("Segoe UI", 42, bold=True)
        self.font_body = pygame.font.SysFont("Segoe UI", 20)
        self.font_small = pygame.font.SysFont("Segoe UI", 16)

    def draw_menu(self, surface, leader_board, active_skin_index, unlocked_achievements):
        surface.fill((10, 10, 12))
        title = self.font_title.render("SNAKE GAME ULTIMATE", True, COLOR_GREEN)
        surface.blit(title, (self.width // 2 - title.get_width() // 2, 25))
        
        prompt_classic = self.font_body.render("Press 1 to Play CLASSIC MODE", True, COLOR_WHITE)
        prompt_time = self.font_body.render("Press 2 to Play TIME ATTACK MODE", True, COLOR_YELLOW)
        prompt_skin = self.font_body.render(f"Press C to Change Skin: {SKINS[active_skin_index]['name']}", True, COLOR_GREEN)
        surface.blit(prompt_classic, (40, 100))
        surface.blit(prompt_time, (40, 135))
        surface.blit(prompt_skin, (40, 170))
        
        lb_title = self.font_body.render("--- TOP 5 LEADERBOARD ---", True, COLOR_GREEN)
        surface.blit(lb_title, (self.width - 280, 100))
        start_y = 135
        for i, score in enumerate(leader_board):
            rank_text = self.font_body.render(f"Top {i+1}: {score} pts", True, COLOR_WHITE if i > 0 else COLOR_YELLOW)
            surface.blit(rank_text, (self.width - 250, start_y))
            start_y += 28

        ach_title = self.font_body.render("--- UNLOCKED ACHIEVEMENTS ---", True, COLOR_YELLOW)
        surface.blit(ach_title, (40, 230))
        ach_y = 265
        all_ach = ["Tan binh", "Dung si diet moi", "Than toc", "Ke san vang"]
        for ach in all_ach:
            status = "[X]" if ach in unlocked_achievements else "[ ]"
            color = COLOR_GREEN if ach in unlocked_achievements else COLOR_GRAY
            ach_text = self.font_body.render(f"{status} {ach}", True, color)
            surface.blit(ach_text, (50, ach_y))
            ach_y += 28

        student_info = self.font_small.render("Sinh vien: Lê Văn Cường - MSV: LT22025070", True, COLOR_GRAY)
        surface.blit(student_info, (self.width // 2 - student_info.get_width() // 2, 565))

    def draw_gameplay(self, surface, score, level, is_golden, game_mode, time_left):
        score_text = self.font_body.render(f"Score: {score}", True, COLOR_WHITE)
        level_text = self.font_body.render(f"Level: {level}", True, COLOR_GREEN)
        mode_str = "CLASSIC" if game_mode == "CLASSIC" else "TIME ATTACK"
        mode_text = self.font_body.render(f"Mode: {mode_str} (Press P to Pause)", True, COLOR_WHITE)
        
        surface.blit(score_text, (20, 15))
        surface.blit(mode_text, (self.width // 2 - mode_text.get_width() // 2, 15))
        surface.blit(level_text, (self.width - level_text.get_width() - 20, 15))
        
        if game_mode == "TIME":
            bar_width = 200
            bar_height = 14
            fill_width = int((time_left / 6000) * bar_width)
            fill_width = max(0, min(bar_width, fill_width))
            pygame.draw.rect(surface, COLOR_GRAY, (self.width // 2 - bar_width // 2, 45, bar_width, bar_height), 1)
            pygame.draw.rect(surface, COLOR_RED, (self.width // 2 - bar_width // 2 + 2, 47, fill_width - 4, bar_height - 4))

        if is_golden:
            buff_text = self.font_small.render("BUFF SPEED & POINTS X2!", True, COLOR_YELLOW)
            surface.blit(buff_text, (20, 45))

    def draw_pause(self, surface):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((10, 10, 12, 180))
        surface.blit(overlay, (0, 0))
        pause_text = self.font_title.render("GAME PAUSED", True, COLOR_YELLOW)
        resume_text = self.font_body.render("Press P to Resume Game", True, COLOR_WHITE)
        surface.blit(pause_text, (self.width // 2 - pause_text.get_width() // 2, self.height // 2 - 40))
        surface.blit(resume_text, (self.width // 2 - resume_text.get_width() // 2, self.height // 2 + 20))

    def draw_game_over(self, surface, score, is_new_record, newly_unlocked):
        surface.fill((10, 10, 12))
        title = self.font_title.render("GAME OVER", True, COLOR_RED)
        score_text = self.font_body.render(f"Final Score: {score}", True, COLOR_WHITE)
        
        surface.blit(title, (self.width // 2 - title.get_width() // 2, 100))
        surface.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 170))

        start_y = 220
        if is_new_record:
            hs_msg = self.font_body.render("CONGRATULATIONS! NEW TOP 5 RECORD!", True, COLOR_YELLOW)
            surface.blit(hs_msg, (self.width // 2 - hs_msg.get_width() // 2, start_y))
            start_y += 35

        for ach in newly_unlocked:
            ach_msg = self.font_body.render(f"🏆 Achievement Unlocked: {ach}!", True, COLOR_GREEN)
            surface.blit(ach_msg, (self.width // 2 - ach_msg.get_width() // 2, start_y))
            start_y += 30
            
        prompt = self.font_body.render("Press R to return to Menu or ESC to Exit", True, COLOR_WHITE)
        surface.blit(prompt, (self.width // 2 - prompt.get_width() // 2, 420))
