import pygame

SETTINGS = {
    'TITLE': 'Stein Schere Papier',
    'WINDOW_WIDTH': 800,
    'WINDOW_HEIGHT': 600,
    'FPS': 60,
    'LANGUAGES': ['DE', 'EN'],
    'DEFAULT_LANG': 'DE',
    'KEY_BINDINGS': {
        'p1': {'rock': pygame.K_a, 'paper': pygame.K_s, 'scissors': pygame.K_d},
        'p2': {'rock': pygame.K_LEFT, 'paper': pygame.K_DOWN, 'scissors': pygame.K_RIGHT}
    },
    'DIFFICULTIES': ['Anfänger', 'Profi', 'Meister'],
}