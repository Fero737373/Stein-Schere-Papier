import pygame
from game import ScreenNames

class BattleScreen:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
    def on_enter(self): pass
    def handle_event(self, event): pass
    def update(self, dt): pass
    def draw(self):
        self.screen.fill((0,100,0))
        pass