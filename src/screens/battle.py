import pygame
from screen_names import ScreenNames

class BattleScreen:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.font = pygame.font.Font(None, 36)
        self.BG_COLOR = (0, 100, 0)

    def on_enter(self):
        self.game.reset_battle()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.switch_screen(ScreenNames.MENU)

    def update(self, dt):
        self.game.battle_time += dt

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        time_text = self.font.render(f"Time: {self.game.battle_time:.1f}s", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 10))

        bar_width = 150
        bar_height = 20
        pygame.draw.rect(self.screen, (200, 0, 0), (10, self.height - 30, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 200, 0), (self.width - bar_width - 10, self.height - 30, bar_width, bar_height))

