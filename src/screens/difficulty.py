import pygame
from screen_names import ScreenNames

class DifficultyScreen:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        self.BG_COLOR = (40, 40, 60)
        self.TEXT_COLOR = (255, 255, 255)
        self.font = pygame.font.Font(None, 36)
        
    def on_enter(self):
        print("Entered Difficulty Screen")
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.switch_screen(ScreenNames.MENU)
            
    def update(self, dt):
        pass
        
    def draw(self):
        self.screen.fill(self.BG_COLOR)
        text = self.font.render("Difficulty Selection", True, self.TEXT_COLOR)
        text_rect = text.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(text, text_rect)