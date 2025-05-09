import pygame
from game import ScreenNames

class SettingsScreen:
    def __init__(self, app): self.app = app
    def on_enter(self): pass
    def handle_event(self, event): pass
    def update(self, dt): pass
    def draw(self):
        self.app.screen.fill((30,30,30))
        pass