# screens/pvp_screen.py

import pygame
import sys
import os
import math

# Import ScreenNames richtig - entweder aus parent oder local
try:
    from screen_names import ScreenNames
except ImportError:
    try:
        from .screen_names import ScreenNames
    except ImportError:
        # Fallback falls screen_names nicht existiert
        class ScreenNames:
            MAIN_MENU = "main_menu"
            HOME = "home"

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS = 60

# Farben für Fallbacks
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY  = (128, 128, 128)
RED = (255, 0, 0)

class PlayerVPlayerScreen:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.clock = pygame.time.Clock()
        
        # Font initialisieren
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state initialisieren
        self.reset_game()

    def on_enter(self):
        """Called when entering this screen"""
        self.reset_game()
        print("Entering Player vs Player Screen")

    def reset_game(self):
        """Reset all game variables"""
        # Game-State
        self.game_state = "waiting_start"   # waiting_start, countdown, input_phase, show_result, game_over
        self.countdown_stage = 0
        self.countdown_timer = 0
        self.input_timer = 0
        self.result_timer = 0
        self.game_over_timer = 0

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
        """Load all game images with proper error handling"""
        # Bessere Pfad-Behandlung
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', 'assets'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'assets'),
            'assets',
            'src/assets'
        ]
        
        base_path = None
        for path in possible_paths:
            if os.path.exists(path):
                base_path = os.path.abspath(path)
                print(f"Assets-Ordner gefunden: {base_path}")
                break
        
        if base_path is None:
            print("Warning: Assets folder not found in:", possible_paths)
            base_path = ""

        self.images = {}
        files = {
            'background': 'background_2.png',   # Hintergrundbild
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
            try:
                if not base_path:
                    raise FileNotFoundError("No assets path found")
                
                full_path = os.path.join(base_path, fname)
                
                # GIFs oder echte Bilder
                if fname.lower().endswith('.gif'):
                    # Einfacher Platzhalter für GIF
                    surf = pygame.Surface((180, 180), pygame.SRCALPHA)
                    surf.fill(GRAY)
                    text = self.font.render(key.replace('_', ' ').title(), True, BLACK)
                    rect = text.get_rect(center=surf.get_rect().center)
                    surf.blit(text, rect)
                    self.images[key] = surf
                else:
                    img = pygame.image.load(full_path)
                    self.images[key] = img.convert_alpha() if img.get_alpha() else img.convert()
            except Exception as e:
                # Fallback-Bild generieren
                if 'heart' in key:
                    size = (50, 50)
                    color = RED if 'full' in key else GRAY
                elif 'hand' in key:
                    size = (180, 180)
                    color = GRAY
                elif 'countdown' in key:
                    size = (120, 120)
                    color = WHITE
                elif 'wins' in key:
                    size = (400, 150)
                    color = WHITE
                else:
                    size = (100, 100)
                    color = GRAY

                surf = pygame.Surface(size)
                surf.fill(color)
                text = self.small_font.render(key.replace('_', ' ').title(), True, BLACK)
                rect = text.get_rect(center=surf.get_rect().center)
                surf.blit(text, rect)
                self.images[key] = surf

                print(f"Using fallback for '{key}' ({fname}): {e}")

    def load_sounds(self):
        """Load background music with error handling"""
        try:
            # Verschiedene mögliche Musik-Pfade
            music_files = [
                'background_battle_music.mp3',
                'assets/background_battle_music.mp3',
                'src/assets/background_battle_music.mp3',
                'background_music.mp3',
                'assets/background_music.mp3'
            ]
            
            music_loaded = False
            for music_file in music_files:
                try:
                    if os.path.exists(music_file):
                        pygame.mixer.music.load(music_file)
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                        music_loaded = True
                        print(f"Loaded music: {music_file}")
                        break
                except pygame.error:
                    continue
                    
            if not music_loaded:
                print("Warning: No background music found")
                
        except Exception as e:
            print(f"Error loading music: {e}")

    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.game_state == "waiting_start":
                self.start_countdown()
            elif event.key == pygame.K_ESCAPE:
                # Zurück zum Hauptmenü
                try:
                    pygame.mixer.music.stop()
                except:
                    pass
                self.manager.change_screen(ScreenNames.HOME)
            elif self.game_state == "input_phase":
                # Player 1 Controls (A,S,D)
                if event.key == pygame.K_a:
                    self.player1_choice = "rock"
                elif event.key == pygame.K_s:
                    self.player1_choice = "scissors"
                elif event.key == pygame.K_d:
                    self.player1_choice = "paper"
                # Player 2 Controls (←,↓,→)
                elif event.key == pygame.K_LEFT:
                    self.player2_choice = "rock"
                elif event.key == pygame.K_DOWN:
                    self.player2_choice = "scissors"
                elif event.key == pygame.K_RIGHT:
                    self.player2_choice = "paper"

    def update(self, dt):
        """Update game logic"""
        try:
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
            
        except Exception as e:
            print(f"Error in update: {e}")

    def draw(self):
        """Draw everything to screen"""
        try:
            # Hintergrund
            bg_img = pygame.transform.scale(self.images['background'], (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(bg_img, (0, 0))

            if self.game_state != "game_over":
                self.draw_hearts()
                self.draw_timer_area()
                self.draw_hands()
                self.draw_buttons()
                self.draw_instructions()
            else:
                self.draw_game_over()

        except Exception as e:
            print(f"Error in draw: {e}")
            # Fallback: Schwarzer Bildschirm mit Fehlermeldung
            self.screen.fill(BLACK)
            error_text = self.font.render("Drawing Error - Press ESC", True, WHITE)
            self.screen.blit(error_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))

    def draw_instructions(self):
        """Draw control instructions"""
        if self.game_state == "waiting_start":
            instructions = [
                "SPACE - Start Game",
                "ESC - Back to Menu",
                "",
                "Player 1: A=Rock, S=Scissors, D=Paper",
                "Player 2: ←=Rock, ↓=Scissors, →=Paper"
            ]
            
            y_start = SCREEN_HEIGHT - 150
            for i, instruction in enumerate(instructions):
                if instruction:  # Skip empty lines
                    text = self.small_font.render(instruction, True, WHITE)
                    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_start + i * 25))
                    self.screen.blit(text, text_rect)

    # ——— STATE-ÜBERGÄNGE —————————————————————————————————

    def start_countdown(self):
        """Start countdown sequence"""
        self.game_state = "countdown"
        self.countdown_stage = 0
        self.countdown_timer = pygame.time.get_ticks()
        print("Starting countdown...")

    def update_countdown(self):
        """Update countdown timer"""
        now = pygame.time.get_ticks()
        if now - self.countdown_timer > 1000:  # 1 second per stage
            self.countdown_stage += 1
            self.countdown_timer = now
            if self.countdown_stage > 3:  # After GO!
                self.start_input_phase()

    def start_input_phase(self):
        """Start input phase"""
        self.game_state = "input_phase"
        self.input_timer = pygame.time.get_ticks()
        self.player1_choice = None
        self.player2_choice = None
        print("Input phase started")

    def update_input_phase(self):
        """Update input phase and check timeout"""
        if pygame.time.get_ticks() - self.input_timer > 2000:  # 2 seconds
            self.resolve_round()

    def resolve_round(self):
        """Resolve the current round"""
        # Default = rock wenn keine Eingabe
        if self.player1_choice is None: 
            self.player1_choice = "rock"
        if self.player2_choice is None: 
            self.player2_choice = "rock"
            
        winner = self.determine_winner(self.player1_choice, self.player2_choice)
        
        print(f"P1: {self.player1_choice}, P2: {self.player2_choice}, Winner: {winner}")
        
        if winner == 1:
            self.player2_lives -= 1
            self.start_heart_shake()
        elif winner == 2:
            self.player1_lives -= 1
            self.start_heart_shake()
        # Draw = niemand verliert Leben

        # Check game over
        if self.player1_lives <= 0 or self.player2_lives <= 0:
            self.game_state = "game_over"
            self.game_over_timer = pygame.time.get_ticks()
        else:
            self.game_state = "show_result"
            self.result_timer = pygame.time.get_ticks()

    def update_show_result(self):
        """Update result display phase"""
        if pygame.time.get_ticks() - self.result_timer > 2000:  # 2 seconds
            self.game_state = "waiting_start"  # Back to waiting for next round

    def start_heart_shake(self):
        """Start heart shake animation"""
        self.heart_shake_timer = pygame.time.get_ticks()

    def update_heart_shake(self):
        """Update heart shake animation"""
        if self.heart_shake_timer > 0:
            elapsed = pygame.time.get_ticks() - self.heart_shake_timer
            if elapsed < 500:  # shake for 500ms
                self.heart_shake_offset = math.sin(elapsed * 0.02) * 5
            else:
                self.heart_shake_offset = 0
                self.heart_shake_timer = 0

    def determine_winner(self, choice1, choice2):
        """Determine winner of rock paper scissors"""
        if choice1 == choice2:
            return 0  # Draw
        wins = {
            'rock': 'scissors',
            'scissors': 'paper', 
            'paper': 'rock'
        }
        return 1 if wins.get(choice1) == choice2 else 2

    def update_game_over(self):
        """Update game over state"""
        if pygame.time.get_ticks() - self.game_over_timer > 5000:  # 5 seconds
            try:
                pygame.mixer.music.stop()
            except:
                pass
            # BUG FIX: Verwende change_screen statt switch_screen
            self.manager.change_screen(ScreenNames.MAIN_MENU)

    # ——— DRAWING METHODS —————————————————————————————————

    def draw_hearts(self):
        """Draw player hearts with shake effect"""
        heart_size = 50
        heart_spacing = 60
        
        # Player 1 hearts (left side)
        start_x = 50
        start_y = 50 + self.heart_shake_offset
        
        for i in range(3):
            x = start_x + i * heart_spacing
            heart_img = self.images['heart_full'] if i < self.player1_lives else self.images['heart_empty']
            scaled_heart = pygame.transform.scale(heart_img, (heart_size, heart_size))
            self.screen.blit(scaled_heart, (x, start_y))
            
        # Player 2 hearts (right side)  
        start_x = SCREEN_WIDTH - 50 - 3 * heart_spacing
        
        for i in range(3):
            x = start_x + i * heart_spacing
            heart_img = self.images['heart_full'] if i < self.player2_lives else self.images['heart_empty']
            scaled_heart = pygame.transform.scale(heart_img, (heart_size, heart_size))
            self.screen.blit(scaled_heart, (x, start_y))

    def draw_timer_area(self):
        """Draw center timer/countdown area"""
        center_x = SCREEN_WIDTH // 2
        center_y = 120
        
        if self.game_state == "countdown":
            countdown_images = ['countdown_1', 'countdown_2', 'countdown_3', 'countdown_go']
            if self.countdown_stage < len(countdown_images):
                img = self.images[countdown_images[self.countdown_stage]]
                scaled_img = pygame.transform.scale(img, (120, 120))
                img_rect = scaled_img.get_rect(center=(center_x, center_y))
                self.screen.blit(scaled_img, img_rect)
        elif self.game_state == "waiting_start":
            text = self.font.render("Press SPACE to Start", True, WHITE)
            text_rect = text.get_rect(center=(center_x, center_y))
            self.screen.blit(text, text_rect)
        elif self.game_state == "input_phase":
            remaining_time = max(0, 2000 - (pygame.time.get_ticks() - self.input_timer))
            time_text = f"Time: {remaining_time // 1000 + 1}"
            text = self.font.render(time_text, True, WHITE)
            text_rect = text.get_rect(center=(center_x, center_y))
            self.screen.blit(text, text_rect)

    def draw_hands(self):
        """Draw player hands"""
        # Player 1 hand (left side)
        p1_hand_center = (200, 300)
        
        if self.game_state in ["show_result"] and self.player1_choice:
            hand_img = self.images[f'hand_p1_{self.player1_choice}']
        else:
            hand_img = self.images['hand_p1_idle']
            
        scaled_hand = pygame.transform.scale(hand_img, (180, 180))
        hand_rect = scaled_hand.get_rect(center=p1_hand_center)
        self.screen.blit(scaled_hand, hand_rect)
        
        # Player 2 hand (right side)
        p2_hand_center = (600, 300)
        
        if self.game_state in ["show_result"] and self.player2_choice:
            hand_img = self.images[f'hand_p2_{self.player2_choice}']
        else:
            hand_img = self.images['hand_p2_idle']
            
        scaled_hand = pygame.transform.scale(hand_img, (180, 180))
        hand_rect = scaled_hand.get_rect(center=p2_hand_center)
        self.screen.blit(scaled_hand, hand_rect)

    def draw_buttons(self):
        """Draw control buttons at bottom"""
        # BUG FIX: Nur während der Input-Phase oder Waiting-Phase anzeigen
        if self.game_state not in ["input_phase", "waiting_start"]:
            return
            
        button_width = 90
        button_height = 60  # BUG FIX: Reduzierte Höhe um Überlappung zu vermeiden
        button_y = SCREEN_HEIGHT - 80  # BUG FIX: Höher positioniert
        
        # Player 1 buttons
        p1_buttons = [(120, "A\nRock"), (220, "S\nScissors"), (320, "D\nPaper")]
        
        for x, label in p1_buttons:
            button_rect = pygame.Rect(x - button_width//2, button_y - button_height//2, 
                                    button_width, button_height)
            pygame.draw.rect(self.screen, GRAY, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 3)
            
            # BUG FIX: Bessere Textpositionierung
            lines = label.split('\n')
            for i, line in enumerate(lines):
                text = self.small_font.render(line, True, WHITE)
                text_rect = text.get_rect(center=(x, button_y - 10 + i * 20))
                self.screen.blit(text, text_rect)
                
        # Player 2 buttons  
        p2_buttons = [(480, "←\nRock"), (580, "↓\nScissors"), (680, "→\nPaper")]
        
        for x, label in p2_buttons:
            button_rect = pygame.Rect(x - button_width//2, button_y - button_height//2, 
                                    button_width, button_height)
            pygame.draw.rect(self.screen, GRAY, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 3)
            
            # BUG FIX: Bessere Textpositionierung
            lines = label.split('\n')
            for i, line in enumerate(lines):
                text = self.small_font.render(line, True, WHITE)
                text_rect = text.get_rect(center=(x, button_y - 10 + i * 20))
                self.screen.blit(text, text_rect)

    def draw_game_over(self):
        """Draw game over screen"""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Bestimme Gewinner
        if self.player1_lives <= 0:
            winner_img = self.images['player2_wins']
            winner_text = "Player 2 Wins!"
        else:
            winner_img = self.images['player1_wins']  
            winner_text = "Player 1 Wins!"
            
        # Zeige Gewinner-Bild
        scaled_img = pygame.transform.scale(winner_img, (400, 150))
        img_rect = scaled_img.get_rect(center=(center_x, center_y - 50))
        self.screen.blit(scaled_img, img_rect)
        
        # Fallback-Text falls Bild nicht sichtbar
        text = self.font.render(winner_text, True, WHITE)
        text_rect = text.get_rect(center=(center_x, center_y + 80))
        self.screen.blit(text, text_rect)
        
        # Countdown bis Rückkehr
        remaining = max(0, 5000 - (pygame.time.get_ticks() - self.game_over_timer))
        countdown_text = f"Returning to menu in {remaining // 1000 + 1}..."
        small_text = self.small_font.render(countdown_text, True, WHITE)
        small_rect = small_text.get_rect(center=(center_x, center_y + 120))
        self.screen.blit(small_text, small_rect)