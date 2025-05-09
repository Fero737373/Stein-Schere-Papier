import pygame
from enum import Enum, auto
from screens.homescreen import HomeScreen
from screens.menu import MenuScreen
from screens.settings import SettingsScreen
from screens.player_v_bot import PlayerVBotScreen
from screens.battle import BattleScreen
from screens.end import EndScreen
from screens.highscore import HighscoreScreen
from config import SETTINGS

class ScreenNames(Enum):
    HOME = auto()
    MENU = auto()
    SETTINGS = auto()
    PLAYER_V_BOT = auto()
    BATTLE = auto()
    END = auto()
    HIGHSCORE = auto()

class GameApp:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screens = {
            ScreenNames.HOME: HomeScreen(self),
            ScreenNames.MENU: MenuScreen(self),
            ScreenNames.SETTINGS: SettingsScreen(self),
            ScreenNames.PLAYER_V_BOT: PlayerVBotScreen(self),
            ScreenNames.BATTLE: BattleScreen(self),
            ScreenNames.END: EndScreen(self),
            ScreenNames.HIGHSCORE: HighscoreScreen(self),
        }
        self.current = ScreenNames.HOME

    def change_screen(self, new_screen: ScreenNames):
        self.current = new_screen
        self.screens[self.current].on_enter()

    def run(self, clock):
        running = True
        while running:
            dt = clock.tick(SETTINGS['FPS']) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.screens[self.current].handle_event(event)

            self.screens[self.current].update(dt)
            self.screens[self.current].draw()
            pygame.display.flip()

