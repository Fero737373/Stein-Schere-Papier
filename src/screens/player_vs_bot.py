import pygame
from screen_names import ScreenNames

class PlayerVsBotScreen:
    def __init__(self, app):
        self.game = app
        self.screen = app.screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        # Colors
        self.BG_COLOR = (40, 40, 60)
        self.TEXT_COLOR = (255, 255, 255)
        self.font = pygame.font.Font(None, 36)
        
    def on_enter(self):
        print("Entered Player vs Bot Screen")
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.switch_screen(ScreenNames.MENU)
            
    def update(self, dt):
        pass
        
    def draw(self):
        self.screen.fill(self.BG_COLOR)
        text = self.font.render("Player vs Bot", True, self.TEXT_COLOR)
        text_rect = text.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(text, text_rect)