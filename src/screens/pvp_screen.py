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

class GifAnimation:
    """Simple GIF animation handler for Pygame"""
    def __init__(self, gif_path):
        self.frames = []
        self.current_frame = 0
        self.last_update = 0
        self.frame_duration = 100  # milliseconds per frame
        
        try:
            # Try to load GIF frames using PIL/Pillow if available
            from PIL import Image
            
            gif = Image.open(gif_path)
            
            # Start from the first frame
            gif.seek(0)
            
            # Extract all frames
            frame_index = 0
            while True:
                try:
                    # Ensure we're at the correct frame
                    gif.seek(frame_index)
                    
                    # Convert PIL image to Pygame surface
                    frame = gif.convert("RGBA")
                    mode = frame.mode
                    size = frame.size
                    data = frame.tobytes()
                    
                    py_frame = pygame.image.fromstring(data, size, mode)
                    self.frames.append(py_frame)
                    
                    # Try to get frame duration
                    if 'duration' in gif.info:
                        self.frame_duration = gif.info['duration']
                    
                    frame_index += 1
                except EOFError:
                    break
                    
            print(f"✅ GIF loaded with {len(self.frames)} frames")
                    
        except ImportError:
            # If PIL not available, load as static image
            print("PIL/Pillow not found - loading GIF as static image")
            static_frame = pygame.image.load(gif_path)
            self.frames = [static_frame]
        except Exception as e:
            print(f"Error loading GIF {gif_path}: {e}")
            # Create a fallback frame
            fallback = pygame.Surface((200, 200))
            fallback.fill(WHITE)
            text = pygame.font.Font(None, 24).render("GIF", True, BLACK)
            fallback.blit(text, text.get_rect(center=fallback.get_rect().center))
            self.frames = [fallback]
    
    def update(self, current_time):
        """Update animation frame based on time"""
        if len(self.frames) > 1:
            if current_time - self.last_update > self.frame_duration:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.last_update = current_time
    
    def get_current_frame(self):
        """Get the current frame"""
        if self.frames:
            return self.frames[self.current_frame]
        return pygame.Surface((200, 200))  # Fallback
    
    def reset(self):
        """Reset animation to first frame"""
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

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
        print("\n=== ASSET LOADING START ===")
        
        # Bessere Pfad-Behandlung - erweitert um mehr mögliche Pfade
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', 'assets'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'assets'), 
            os.path.join(os.path.dirname(__file__), 'assets'),
            'assets',
            'src/assets',
            os.path.join(os.getcwd(), 'assets'),
            os.path.join(os.getcwd(), 'src', 'assets')
        ]
        
        print(f"Aktuelles Arbeitsverzeichnis: {os.getcwd()}")
        print(f"Script-Verzeichnis: {os.path.dirname(__file__)}")
        print(f"Suche in folgenden Pfaden: {possible_paths}")
        
        base_path = None
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            print(f"Prüfe Pfad: {abs_path}")
            if os.path.exists(abs_path):
                base_path = abs_path
                print(f"✅ Assets-Ordner gefunden: {base_path}")
                # Liste alle Dateien im Assets-Ordner auf
                try:
                    all_files = os.listdir(base_path)
                    print(f"Alle Dateien im Assets-Ordner: {all_files}")
                    
                    # Suche nach dem Hintergrund mit verschiedenen möglichen Namen
                    background_found = False
                    for file in all_files:
                        if 'background' in file.lower() and file.lower().endswith(('.png', '.jpg', '.jpeg')):
                            print(f"Möglicher Hintergrund gefunden: {file}")
                            background_found = True
                            
                except Exception as e:
                    print(f"Fehler beim Listen der Dateien: {e}")
                break
            else:
                print(f"❌ Pfad existiert nicht: {abs_path}")
        
        if base_path is None:
            print("❌ KRITISCHER FEHLER: Kein Assets-Ordner gefunden!")
            base_path = ""

        self.images = {}
        self.animations = {}  # Für GIF-Animationen
        
        files = {
            'background': 'SSP_battlebackground.png',   # Original name
            'heart_p1_full':    'FullHP_P1.png',
            'heart_p2_full':    'FullHP_P2.png',  
            'heart_empty':      'HP_Leer.png',
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
        
        # Spezielle Behandlung für GIFs
        gif_files = {
            'countdown_gif': 'countdown_gif.gif',
            'hand_p1_idle': 'hand_p1_idle.gif',
            'hand_p2_idle': 'hand_p2_idle.gif'
        }
        
        # Lade GIFs als Animationen
        for key, fname in gif_files.items():
            print(f"\n--- Lade GIF Animation {key} ({fname}) ---")
            try:
                if not base_path:
                    raise FileNotFoundError("No assets path found")
                
                full_path = os.path.join(base_path, fname)
                
                # Suche case-insensitive nach der Datei
                if not os.path.exists(full_path) and base_path:
                    for file in os.listdir(base_path):
                        if file.lower() == fname.lower():
                            full_path = os.path.join(base_path, file)
                            break
                
                if os.path.exists(full_path):
                    self.animations[key] = GifAnimation(full_path)
                    print(f"✅ GIF Animation geladen: {key}")
                else:
                    raise FileNotFoundError(f"GIF nicht gefunden: {full_path}")
                    
            except Exception as e:
                print(f"❌ Fehler beim Laden der GIF Animation {key}: {e}")
                # Erstelle Fallback Animation
                fallback = pygame.Surface((200, 200))
                fallback.fill(WHITE)
                text = self.small_font.render(key.replace('_', ' ').title(), True, BLACK)
                fallback.blit(text, text.get_rect(center=fallback.get_rect().center))
                self.animations[key] = type('obj', (object,), {
                    'frames': [fallback],
                    'current_frame': 0,
                    'update': lambda self, t: None,
                    'get_current_frame': lambda self: fallback,
                    'reset': lambda self: None
                })()
        
        # Lade normale Bilder
        for key, fname in files.items():
            if key in gif_files:
                continue  # Skip GIFs, already loaded as animations
                
            print(f"\n--- Lade {key} ({fname}) ---")
            try:
                if not base_path:
                    raise FileNotFoundError("No assets path found")
                
                full_path = os.path.join(base_path, fname)
                print(f"Vollständiger Pfad: {full_path}")
                
                # Normale case-insensitive Suche für alle Dateien
                if not os.path.exists(full_path) and base_path and os.path.exists(base_path):
                    for file in os.listdir(base_path):
                        if file.lower() == fname.lower():
                            full_path = os.path.join(base_path, file)
                            print(f"✅ Datei gefunden (case-insensitive): {file}")
                            break
                
                if os.path.exists(full_path):
                    print(f"✅ Lade Datei: {full_path}")
                    img = pygame.image.load(full_path)
                    self.images[key] = img.convert_alpha() if img.get_alpha() else img.convert()
                    print(f"✅ Erfolgreich geladen: {key} - Größe: {img.get_size()}")
                    if key == 'background':
                        print(f"🎯 HINTERGRUND GELADEN AUS: {os.path.basename(full_path)}")
                else:
                    raise FileNotFoundError(f"Datei nicht gefunden: {full_path}")
                    
            except Exception as e:
                print(f"❌ Fehler beim Laden von {key}: {e}")
                print(f"Erstelle Fallback für {key}")
                
                # Verbesserte Fallback-Bilder
                if key == 'background':
                    # Erstelle einen schöneren Fallback-Hintergrund
                    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    # Gradient-Effekt von dunkelgrün zu hellgrün
                    for y in range(SCREEN_HEIGHT):
                        color_val = int(40 + (y / SCREEN_HEIGHT) * 60)
                        pygame.draw.line(surf, (color_val, color_val + 40, color_val), 
                                       (0, y), (SCREEN_WIDTH, y))
                    # Füge einen Titel hinzu
                    title_text = self.font.render("ROCK PAPER SCISSORS", True, WHITE)
                    title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 50))
                    surf.blit(title_text, title_rect)
                elif 'heart_p1' in key:
                    size = (50, 50)
                    surf = pygame.Surface(size, pygame.SRCALPHA)
                    # Zeichne ein Herz-Symbol
                    pygame.draw.circle(surf, (255, 100, 100), (15, 20), 12)
                    pygame.draw.circle(surf, (255, 100, 100), (35, 20), 12)
                    pygame.draw.polygon(surf, (255, 100, 100), [(5, 25), (25, 45), (45, 25)])
                elif 'heart_p2' in key:
                    size = (50, 50)
                    surf = pygame.Surface(size, pygame.SRCALPHA)
                    # Zeichne ein Herz-Symbol
                    pygame.draw.circle(surf, (100, 100, 255), (15, 20), 12)
                    pygame.draw.circle(surf, (100, 100, 255), (35, 20), 12)
                    pygame.draw.polygon(surf, (100, 100, 255), [(5, 25), (25, 45), (45, 25)])
                elif 'heart_empty' in key:
                    size = (50, 50)
                    surf = pygame.Surface(size, pygame.SRCALPHA)
                    # Zeichne ein leeres Herz-Symbol
                    pygame.draw.circle(surf, GRAY, (15, 20), 12, 2)
                    pygame.draw.circle(surf, GRAY, (35, 20), 12, 2)
                    pygame.draw.lines(surf, GRAY, False, [(5, 25), (25, 45), (45, 25)], 2)
                elif 'hand' in key:
                    size = (180, 180)
                    color = (200, 200, 200) if 'p1' in key else (150, 150, 200)
                    surf = pygame.Surface(size)
                    surf.fill(color)
                    # Zeichne ein Hand-Symbol je nach Typ
                    if 'rock' in key:
                        pygame.draw.circle(surf, WHITE, (90, 90), 60)
                        pygame.draw.circle(surf, color, (90, 90), 50)
                    elif 'scissors' in key:
                        pygame.draw.line(surf, WHITE, (60, 60), (120, 120), 10)
                        pygame.draw.line(surf, WHITE, (120, 60), (60, 120), 10)
                    elif 'paper' in key:
                        pygame.draw.rect(surf, WHITE, (45, 45, 90, 90))
                        pygame.draw.rect(surf, color, (55, 55, 70, 70))
                    
                    text_content = key.split('_')[-1].upper()
                    text = self.small_font.render(text_content, True, BLACK)
                    text_rect = text.get_rect(center=(90, 150))
                    surf.blit(text, text_rect)
                elif 'wins' in key:
                    size = (400, 150)
                    color = (200, 200, 255) if 'player1' in key else (255, 200, 200)
                    surf = pygame.Surface(size)
                    surf.fill(color)
                    text_content = "PLAYER 1 WINS!" if 'player1' in key else "PLAYER 2 WINS!"
                    text = self.font.render(text_content, True, BLACK)
                    text_rect = text.get_rect(center=surf.get_rect().center)
                    surf.blit(text, text_rect)
                else:
                    size = (100, 100)
                    color = GRAY
                    surf = pygame.Surface(size)
                    surf.fill(color)
                    text_content = key.replace('_', ' ').title()
                    text = self.small_font.render(text_content, True, WHITE)
                    rect = text.get_rect(center=surf.get_rect().center)
                    surf.blit(text, rect)
                
                self.images[key] = surf
                print(f"✅ Fallback erstellt für {key}")
                
        # Zeige alle geladenen Assets für Debug
        print("\n=== GELADENE ASSETS DEBUG ===")
        for key, img in self.images.items():
            print(f"Image - {key}: {type(img)} - Größe: {img.get_size()}")
        for key, anim in self.animations.items():
            print(f"Animation - {key}: {len(anim.frames)} frames")
        print("=== ASSET LOADING ENDE ===\n")

    def load_sounds(self):
        """Load background music with error handling"""
        try:
            # Verschiedene mögliche Musik-Pfade
            music_files = [
                'background_battle_music.mp3',
                'assets/background_battle_music.mp3',
                'src/assets/background_battle_music.mp3',
                'background_music.mp3',
                'assets/background_music.mp3',
                'battle_music.mp3',
                'assets/battle_music.mp3'
            ]
            
            music_loaded = False
            for music_file in music_files:
                try:
                    if os.path.exists(music_file):
                        pygame.mixer.music.load(music_file)
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                        music_loaded = True
                        print(f"✅ Musik geladen: {music_file}")
                        break
                except pygame.error:
                    continue
                    
            if not music_loaded:
                print("⚠️ Warnung: Keine Hintergrundmusik gefunden")
                
        except Exception as e:
            print(f"❌ Fehler beim Laden der Musik: {e}")

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
            current_time = pygame.time.get_ticks()
            
            # Update GIF animations
            for anim in self.animations.values():
                anim.update(current_time)
            
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
        self.countdown_timer = pygame.time.get_ticks()
        # Reset countdown animation to first frame
        if 'countdown_gif' in self.animations:
            self.animations['countdown_gif'].reset()
            # Ensure the animation starts updating from now
            self.animations['countdown_gif'].last_update = pygame.time.get_ticks()
        print("Starting countdown...")

    def update_countdown(self):
        """Update countdown timer - now 4 seconds total"""
        now = pygame.time.get_ticks()
        if now - self.countdown_timer > 4000:  # 4 Sekunden für Countdown
            self.start_input_phase()

    def start_input_phase(self):
        """Start input phase"""
        self.game_state = "input_phase"
        self.input_timer = pygame.time.get_ticks()
        self.player1_choice = None
        self.player2_choice = None
        print("Input phase started")

    def update_input_phase(self):
        """Update input phase and check timeout - now only 1 second"""
        if pygame.time.get_ticks() - self.input_timer > 1000:  # Nur 1 Sekunde Eingabezeit
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
            self.manager.change_screen(ScreenNames.MAIN_MENU)

    # ——— DRAWING METHODS —————————————————————————————————

    def draw_hearts(self):
        """Draw player hearts with shake effect using new HP images"""
        heart_size = 50
        heart_spacing = 60
        
        # Player 1 hearts (left side)
        start_x = 50
        start_y = 50 + self.heart_shake_offset
        
        for i in range(3):
            x = start_x + i * heart_spacing
            if i < self.player1_lives:
                heart_key = 'heart_p1_full'
            else:
                heart_key = 'heart_empty'
                
            heart_img = self.images[heart_key]
            scaled_heart = pygame.transform.scale(heart_img, (heart_size, heart_size))
            self.screen.blit(scaled_heart, (x, start_y))
            
        # Player 2 hearts (right side)
        start_x = SCREEN_WIDTH - 50 - 3 * heart_spacing
        
        for i in range(3):
            x = start_x + i * heart_spacing
            if i < self.player2_lives:
                heart_key = 'heart_p2_full'
            else:
                heart_key = 'heart_empty'
                
            heart_img = self.images[heart_key]
            scaled_heart = pygame.transform.scale(heart_img, (heart_size, heart_size))
            self.screen.blit(scaled_heart, (x, start_y))

    def draw_timer_area(self):
        """Draw center timer/countdown area"""
        center_x = SCREEN_WIDTH // 2
        center_y = 120
        
        if self.game_state == "countdown":
            # Zeige animiertes Countdown GIF
            if 'countdown_gif' in self.animations:
                current_frame = self.animations['countdown_gif'].get_current_frame()
                scaled_frame = pygame.transform.scale(current_frame, (200, 200))
                frame_rect = scaled_frame.get_rect(center=(center_x, center_y))
                self.screen.blit(scaled_frame, frame_rect)
            else:
                # Fallback: Zeige Countdown-Text
                elapsed = pygame.time.get_ticks() - self.countdown_timer
                countdown_num = 4 - (elapsed // 1000)  # 4, 3, 2, 1
                if countdown_num > 0:
                    text = self.font.render(str(countdown_num), True, WHITE)
                else:
                    text = self.font.render("GO!", True, WHITE)
                text_rect = text.get_rect(center=(center_x, center_y))
                self.screen.blit(text, text_rect)
                
        elif self.game_state == "waiting_start":
            text = self.font.render("Press SPACE to Start", True, WHITE)
            text_rect = text.get_rect(center=(center_x, center_y))
            self.screen.blit(text, text_rect)
        elif self.game_state == "input_phase":
            # Zeige verbleibende Zeit
            remaining_time = max(0, 1000 - (pygame.time.get_ticks() - self.input_timer))
            time_text = f"Time: {(remaining_time // 100) / 10:.1f}s"
            text = self.font.render(time_text, True, WHITE)
            text_rect = text.get_rect(center=(center_x, center_y))
            self.screen.blit(text, text_rect)

    def draw_hands(self):
        """Draw player hands with GIF animations for idle state"""
        # Player 1 hand (left side)
        p1_hand_center = (200, 300)
        
        if self.game_state in ["show_result"] and self.player1_choice:
            hand_img = self.images[f'hand_p1_{self.player1_choice}']
        else:
            # Zeige animierte Idle-Hand
            if 'hand_p1_idle' in self.animations:
                hand_img = self.animations['hand_p1_idle'].get_current_frame()
            else:
                hand_img = self.images.get('hand_p1_idle', pygame.Surface((180, 180)))
            
        scaled_hand = pygame.transform.scale(hand_img, (180, 180))
        hand_rect = scaled_hand.get_rect(center=p1_hand_center)
        self.screen.blit(scaled_hand, hand_rect)
        
        # Player 2 hand (right side)
        p2_hand_center = (600, 300)
        
        if self.game_state in ["show_result"] and self.player2_choice:
            hand_img = self.images[f'hand_p2_{self.player2_choice}']
        else:
            # Zeige animierte Idle-Hand
            if 'hand_p2_idle' in self.animations:
                hand_img = self.animations['hand_p2_idle'].get_current_frame()
            else:
                hand_img = self.images.get('hand_p2_idle', pygame.Surface((180, 180)))
            
        scaled_hand = pygame.transform.scale(hand_img, (180, 180))
        hand_rect = scaled_hand.get_rect(center=p2_hand_center)
        self.screen.blit(scaled_hand, hand_rect)

    def draw_buttons(self):
        """Draw control buttons at bottom"""
        # Nur während der Input-Phase oder Waiting-Phase anzeigen
        if self.game_state not in ["input_phase", "waiting_start"]:
            return
            
        button_width = 90
        button_height = 60
        button_y = SCREEN_HEIGHT - 80
        
        # Player 1 buttons
        p1_buttons = [(120, "A\nRock"), (220, "S\nScissors"), (320, "D\nPaper")]
        
        for x, label in p1_buttons:
            button_rect = pygame.Rect(x - button_width//2, button_y - button_height//2, 
                                    button_width, button_height)
            pygame.draw.rect(self.screen, GRAY, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 3)
            
            # Bessere Textpositionierung
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
            
            # Bessere Textpositionierung
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