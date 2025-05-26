import pygame
from screen_names import ScreenNames
from screens.homescreen import HomeScreen
from screens.menu import MenuScreen
from screens.settings import SettingsScreen
from screens.battle import BattleScreen
from screens.player_vs_bot import PlayerVsBotScreen
from screens.player_vs_player import PlayerVsPlayerScreen
from screens.difficulty import DifficultyScreen
from screens.end import EndScreen

class GameApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Stein-Schere-Papier")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.battle_time = 0
        self.p1_health = 3
        self.p2_health = 3
        
        # Screens initialisieren
        self.current = ScreenNames.HOME
        self.screens = {
            ScreenNames.HOME: HomeScreen(self.screen, self),
            ScreenNames.MENU: MenuScreen(self.screen, self),
            ScreenNames.SETTINGS: SettingsScreen(self.screen, self),
            ScreenNames.BATTLE: BattleScreen(self.screen, self),
            ScreenNames.PLAYER_VS_BOT: PlayerVsBotScreen(self.screen, self),
            ScreenNames.PLAYER_VS_PLAYER: PlayerVsPlayerScreen(self.screen, self),
            ScreenNames.DIFFICULTY: DifficultyScreen(self.screen, self)
        }
        self.screens[self.current].on_enter()

    def switch_screen(self, name):
        """Wechselt zu einem anderen Screen"""
        if name in self.screens:
            self.current = name
            self.screens[name].on_enter()

    def reset_battle(self):
        """Setzt Battle-Zustand zurück"""
        self.battle_time = 0
        self.p1_health = 3
        self.p2_health = 3

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.screens[self.current].handle_event(event)
            
            # Update & Draw
            self.screens[self.current].update(dt)
            self.screens[self.current].draw()
            pygame.display.flip()

        pygame.quit()

