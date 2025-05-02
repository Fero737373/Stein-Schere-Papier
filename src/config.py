import pygame

# Bildschirm- und Farben-Konstanten
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Farben (RGB)
BG_COLOR = (30, 30, 30)
HP_COLOR_P1 = (200, 50, 50)
HP_COLOR_P2 = (50, 50, 200)
HP_BAR_WIDTH = 150
HP_BAR_HEIGHT = 20
HP_MAX = 3

# Positionen der Lebensbalken
P1_HP_POS = (50, 50)
P2_HP_POS = (SCREEN_WIDTH - 50 - HP_BAR_WIDTH, 50)

# Schlüsselzuordnung
INPUT_KEYS = {
    'player1': {
        'rock': pygame.K_a,
        'paper': pygame.K_s,
        'scissors': pygame.K_d
    },
    'player2': {
        'rock': pygame.K_j,
        'paper': pygame.K_k,
        'scissors': pygame.K_l
    }
}
