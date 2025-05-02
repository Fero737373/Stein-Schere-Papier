import pygame
from config import (
    HP_BAR_WIDTH,
    HP_BAR_HEIGHT,
    HP_COLOR_P1,
    HP_COLOR_P2,
    P1_HP_POS,
    P2_HP_POS,
    HP_MAX
)

class UI:
    @staticmethod
    def draw_hp(screen, hp1, hp2):
        # Spieler 1 HP
        width1 = (HP_BAR_WIDTH // HP_MAX) * hp1
        pygame.draw.rect(
            screen,
            HP_COLOR_P1,
            (*P1_HP_POS, width1, HP_BAR_HEIGHT)
        )
        # Spieler 2 HP
        width2 = (HP_BAR_WIDTH // HP_MAX) * hp2
        pygame.draw.rect(
            screen,
            HP_COLOR_P2,
            (*P2_HP_POS, width2, HP_BAR_HEIGHT)
        )