import pygame
from game import ScreenNames

class MenuScreen:
    def __init__(self, app):
        self.app = app
        # Buttons: Player vs Bot / P1 vs P2 / Settings

    def on_enter(self): pass
    def handle_event(self, event):
        # Button-Klicks -> entsprechende ScreenNames
        pass
    def update(self, dt): pass
    def draw(self):
        self.app.screen.fill((40,40,40))
        pass
