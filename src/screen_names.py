import os
import pygame

class ScreenNames:
    HOME = "home"
    MENU = "menu"
    SETTINGS = "settings"
    BATTLE = "battle"
    PLAYER_VS_BOT = "player_vs_bot"
    PLAYER_VS_PLAYER = "player_vs_player"
    DIFFICULTY = "difficulty"
    END = "end"

# Template für neue Screen-Klassen
class ScreenTemplate:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        # Assets laden
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
        # self.bg = pygame.image.load(os.path.join(base, 'background.png')).convert()
        
    def on_enter(self):
        """Called when screen becomes active"""
        pass
        
    def handle_event(self, event):
        """Handle input events"""
        pass
        
    def update(self, dt):
        """Update game logic"""
        pass
        
    def draw(self):
        """Draw screen content"""
        pass