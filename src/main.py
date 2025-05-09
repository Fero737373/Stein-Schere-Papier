import pygame
from enum import Enum, auto

# Spielzustände definieren
class GameState(Enum):
    START = auto()
    MENU = auto()
    SETTINGS = auto()
    P1_VS_P2 = auto()
    P1_VS_BOT = auto()
    BATTLE = auto()
    END = auto()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Stein Schere Papier")
        self.clock = pygame.time.Clock()
        self.state = GameState.START
        self.running = True

        # Platzhalter für Einstellungen
        self.language = 'DE'
        self.key_bindings = {
            'p1': {'rock': pygame.K_a, 'paper': pygame.K_s, 'scissors': pygame.K_d},
            'p2': {'rock': pygame.K_LEFT, 'paper': pygame.K_DOWN, 'scissors': pygame.K_RIGHT}
        }
        self.difficulty = 'Anfänger'
        
        # TODO: Assets laden (Pixel-Art, Schriften, Sounds)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # Gemeinsame Logik während Countdown o.ä. überspringen
                if self.state == GameState.START and event.key == pygame.K_SPACE:
                    self.state = GameState.MENU
                elif self.state == GameState.MENU:
                    # TODO: Navigation zwischen Knöpfen
                    pass
                elif self.state == GameState.SETTINGS:
                    # TODO: Settings-Interaktion
                    pass
                elif self.state in (GameState.P1_VS_P2, GameState.P1_VS_BOT):
                    # TODO: Auswahl der Spielmodi/Difficulty
                    pass
                elif self.state == GameState.BATTLE:
                    # TODO: Während "GO!"-Phase Eingaben abfragen
                    pass
                elif self.state == GameState.END and event.key == pygame.K_RETURN:
                    self.state = GameState.START

    def update(self):
        if self.state == GameState.START:
            self.update_start()
        elif self.state == GameState.MENU:
            self.update_menu()
        elif self.state == GameState.SETTINGS:
            self.update_settings()
        elif self.state in (GameState.P1_VS_P2, GameState.P1_VS_BOT):
            self.update_selection()
        elif self.state == GameState.BATTLE:
            self.update_battle()
        elif self.state == GameState.END:
            self.update_end()

    def draw(self):
        if self.state == GameState.START:
            self.draw_start()
        elif self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.SETTINGS:
            self.draw_settings()
        elif self.state in (GameState.P1_VS_P2, GameState.P1_VS_BOT):
            self.draw_selection()
        elif self.state == GameState.BATTLE:
            self.draw_battle()
        elif self.state == GameState.END:
            self.draw_end()

    # ---- Platzhalter-Methoden für jeden Zustand ----
    def update_start(self):
        # Hintergrundanimation aktualisieren
        pass

    def draw_start(self):
        # Startscreen zeichnen: bewegter BG, Start-Button, Sprach-Icons
        self.screen.fill((0, 0, 0))
        pass

    def update_menu(self):
        pass

    def draw_menu(self):
        self.screen.fill((40, 40, 40))
        pass

    def update_settings(self):
        pass

    def draw_settings(self):
        self.screen.fill((30, 30, 30))
        pass

    def update_selection(self):
        pass

    def draw_selection(self):
        self.screen.fill((80, 80, 80))
        pass

    def update_battle(self):
        # Countdown, Eingabefenster, Ergebnislogik
        pass

    def draw_battle(self):
        self.screen.fill((0, 100, 0))
        pass

    def update_end(self):
        pass

    def draw_end(self):
        self.screen.fill((100, 0, 0))
        pass

if __name__ == '__main__':
    Game().run()
