# screens/pvp_screen.py

import pygame
import sys
import os
import math
from .screen_names import ScreenNames

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS = 60

# Farben für Fallbacks
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY  = (128, 128, 128)

class PlayerVPlayerScreen:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def on_enter(self):
        self.reset_game()

    def reset_game(self):
        # Game-State
        self.game_state = "waiting_start"   # waiting_start, countdown, input_phase, show_result, game_over
        self.countdown_stage = 0
        self.countdown_timer = 0
        self.input_timer = 0

        # Lives & Choices
        self.player1_lives = 3
        self.player2_lives = 3
        self.player1_choice = None
        self.player2_choice = None

        # Heart-Shake Animation
        self.heart_shake_timer = 0
        self.heart_shake_offset = 0

        # Lade Assets
        self.load_images()
        self.load_sounds()

    def load_images(self):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
        self.images = {}
        files = {
            'background':    'background.png',
            'heart_full':    'heart_full.png',
            'heart_empty':   'heart_empty.png',
            'countdown_1':   'countdown_1.png',
            'countdown_2':   'countdown_2.png',
            'countdown_3':   'countdown_3.png',
            'countdown_go':  'countdown_go.png',
            'hand_p1_idle':  'hand_p1_idle.gif',
            'hand_p1_rock':  'hand_p1_rock.png',
            'hand_p1_scissors':'hand_p1_scissors.png',
            'hand_p1_paper': 'hand_p1_paper.png',
            'hand_p2_idle':  'hand_p2_idle.gif',
            'hand_p2_rock':  'hand_p2_rock.png',
            'hand_p2_scissors':'hand_p2_scissors.png',
            'hand_p2_paper': 'hand_p2_paper.png',
            'button':        'button.png',
            'player1_wins':  'player1_wins.png',
            'player2_wins':  'player2_wins.png'
        }
        for key, fname in files.items():
            path = os.path.join(base, fname)
            try:
                if fname.endswith('.gif'):
                    surf = pygame.Surface((200, 200))
                    surf.fill(GRAY)
                    self.images[key] = surf
                else:
                    self.images[key] = pygame.image.load(path).convert_alpha()
            except:
                surf = pygame.Surface((100,100))
                surf.fill(GRAY)
                text = self.font.render(key, True, BLACK)
                surf.blit(text, text.get_rect(center=surf.get_rect().center))
                self.images[key] = surf

    def load_sounds(self):
        try:
            pygame.mixer.music.load('background_music.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except:
            print("Keine Hintergrundmusik gefunden.")

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.game_state == "waiting_start":
                self.start_countdown()
            elif self.game_state == "input_phase":
                # Player 1 (A,S,D)
                if event.key == pygame.K_a:
                    self.player1_choice = "rock"
                elif event.key == pygame.K_s:
                    self.player1_choice = "scissors"
                elif event.key == pygame.K_d:
                    self.player1_choice = "paper"
                # Player 2 (←,↓,→)
                elif event.key == pygame.K_LEFT:
                    self.player2_choice = "rock"
                elif event.key == pygame.K_DOWN:
                    self.player2_choice = "scissors"
                elif event.key == pygame.K_RIGHT:
                    self.player2_choice = "paper"

    def update(self, dt):
        # State-Updates
        if self.game_state == "countdown":
            self.update_countdown()
        elif self.game_state == "input_phase":
            self.update_input_phase()
        elif self.game_state == "show_result":
            self.update_show_result()
        elif self.game_state == "game_over":
            self.update_game_over()

        # Herz-Shake immer updaten
        self.update_heart_shake()

    def draw(self):
        # Hintergrund
        self.screen.blit(pygame.transform.scale(self.images['background'], (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))

        if self.game_state != "game_over":
            self.draw_hearts()
            self.draw_timer_area()
            self.draw_hands()
            self.draw_buttons()
        else:
            self.draw_game_over()

        pygame.display.flip()

    # ——— STATE-ÜBERGÄNGE —————————————————————————————————

    def start_countdown(self):
        self.game_state = "countdown"
        self.countdown_stage = 0
        self.countdown_timer = pygame.time.get_ticks()

    def update_countdown(self):
        now = pygame.time.get_ticks()
        if now - self.countdown_timer > 1000:
            self.countdown_stage += 1
            self.countdown_timer = now
            if self.countdown_stage > 3:
                self.start_input_phase()

    def start_input_phase(self):
        self.game_state = "input_phase"
        self.input_timer = pygame.time.get_ticks()
        self.player1_choice = None
        self.player2_choice = None

    def update_input_phase(self):
        if pygame.time.get_ticks() - self.input_timer > 2000:
            self.resolve_round()

    def resolve_round(self):
        # Default = rock
        if self.player1_choice is None: self.player1_choice = "rock"
        if self.player2_choice is None: self.player2_choice = "rock"
        winner = self.determine_winner(self.player1_choice, self.player2_choice)
        if winner == 1:
            self.player2_lives -= 1
            self.start_heart_shake()
        elif winner == 2:
            self.player1_lives -= 1
            self.start_heart_shake()

        if self.player1_lives <= 0 or self.player2_lives <= 0:
            self.game_state = "game_over"
            self.game_over_tim
