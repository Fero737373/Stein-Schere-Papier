import pygame
from config import HP_MAX, INPUT_KEYS
from ui import UI

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.hp1 = HP_MAX
        self.hp2 = HP_MAX
        self.choice1 = None
        self.choice2 = None

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            for player, keys in INPUT_KEYS.items():
                for choice, key in keys.items():
                    if event.key == key:
                        if player == 'player1':
                            self.choice1 = choice
                        else:
                            self.choice2 = choice
                        self.resolve_round()

    def resolve_round(self):
        if self.choice1 and self.choice2:
            result = Game.evaluate(self.choice1, self.choice2)
            if result == 1:
                self.hp2 -= 1
            elif result == 2:
                self.hp1 -= 1
            # Für die nächste Runde zurücksetzen
            self.choice1 = None
            self.choice2 = None

    @staticmethod
    def evaluate(c1, c2):
        wins = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
        if c1 == c2:
            return 0
        return 1 if wins[c1] == c2 else 2

    def update(self):
        self.screen.fill((30, 30, 30))
        UI.draw_hp(self.screen, self.hp1, self.hp2)

        # Spielende prüfen
        if self.hp1 <= 0 or self.hp2 <= 0:
            self.game_over()

    def game_over(self):
        font = pygame.font.Font(None, 74)
        if self.hp1 <= 0:
            text = font.render("Player 2 gewinnt!", True, (255, 255, 255))
        else:
            text = font.render("Player 1 gewinnt!", True, (255, 255, 255))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        exit()
