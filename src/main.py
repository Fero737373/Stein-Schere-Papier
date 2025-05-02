import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Stein-Schere-Papier")
    clock = pygame.time.Clock()

    game = Game(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_input(event)

        game.update()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
