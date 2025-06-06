import pygame
from game import ScreenNames

class HighscoreScreen:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
    def on_enter(self): pass
    def handle_event(self, event): pass
    def update(self, dt): pass
    def draw(self):
        self.screen.fill((20,20,100))
        pass
