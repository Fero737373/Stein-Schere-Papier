import pygame
from screen_names import ScreenNames  # Geändert von: from game import ScreenNames

class PlayerVBotScreen:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        
    def on_enter(self): 
        pass
    
    def handle_event(self, event): 
        pass
    
    def update(self, dt): 
        pass
    
    def draw(self):
        self.screen.fill((80,80,80))
        pass