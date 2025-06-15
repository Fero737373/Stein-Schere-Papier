# main.py
import pygame
from screens.screen_manager import ScreenManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Stein–Schere–Papier")
    manager = ScreenManager(screen)
    manager.run()

if __name__ == "__main__":
    main()
