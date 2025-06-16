# screens/screen_manager.py
import pygame
from .screen_names import ScreenNames
from .homescreen import HomeScreen
from .pvp_screen import PlayerVPlayerScreen

class ScreenManager:
    def __init__(self, screen):
        self.screen = screen
        self.current_screen = HomeScreen(screen, self)
        self.current_screen.on_enter()

    def change_screen(self, screen_name):
        if screen_name == ScreenNames.HOME:
            self.current_screen = HomeScreen(self.screen, self)
        elif screen_name == ScreenNames.PVP:
            self.current_screen = PlayerVPlayerScreen(self.screen, self)
        self.current_screen.on_enter()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.current_screen.handle_event(event)
            self.current_screen.update(dt)
            self.current_screen.draw()
            pygame.display.flip()  # Wichtig: Screen aktualisieren
        pygame.quit()
