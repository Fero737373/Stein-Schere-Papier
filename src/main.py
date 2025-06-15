import pygame
from enum import Enum, auto
from screen_names import ScreenNames
from game import GameApp
from screens.homescreen import HomeScreen
from screens.menu import MenuScreen

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

        # Starte mit dem HomeScreen und übergebe 'self' als Manager
        self.current_screen = HomeScreen(self.screen, self)
        self.current_screen.on_enter()

        # Platzhalter für Einstellungen
        self.language = 'DE'
        self.key_bindings = {
            'p1': {'rock': pygame.K_a, 'paper': pygame.K_s, 'scissors': pygame.K_d},
            'p2': {'rock': pygame.K_LEFT, 'paper': pygame.K_DOWN, 'scissors': pygame.K_RIGHT}
        }
        self.difficulty = 'Anfänger'

    def change_screen(self, screen_name):
        if screen_name == ScreenNames.MENU:
            self.current_screen = MenuScreen(self)
            self.current_screen.on_enter()
        elif screen_name == ScreenNames.HOME:
            from screens.homescreen import HomeScreen  # falls nötig
            self.current_screen = HomeScreen(self.screen, self)
            self.current_screen.on_enter()
        # Hier können ggf. weitere Screens ergänzt werden

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
            pygame.display.flip()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.START and event.key == pygame.K_SPACE:
                    self.state = GameState.MENU
                # ... weitere Events wie gehabt ...

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
        pass

    def draw_start(self):
        self.current_screen.draw()  # Nur noch diese Zeile!

    def update_menu(self):
        pass

    def draw_menu(self):
        self.screen.fill((40, 40, 40))

    def update_settings(self):
        pass

    def draw_settings(self):
        self.screen.fill((30, 30, 30))

    def update_selection(self):
        pass

    def draw_selection(self):
        self.screen.fill((80, 80, 80))

    def update_battle(self):
        pass

    def draw_battle(self):
        self.screen.fill((0, 100, 0))

    def update_end(self):
        pass

    def draw_end(self):
        self.screen.fill((100, 0, 0))

if __name__ == '__main__':
    app = GameApp()
    app.run()

# Template for all screen classes
def __init__(self, screen, game):
    self.screen = screen
    self.game = game
    self.width = self.screen.get_width()
    self.height = self.screen.get_height()
