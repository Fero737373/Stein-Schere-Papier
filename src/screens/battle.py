import pygame
import sys
import time
import random
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (fallback if images don't load)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

class RockPaperScissorsGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rock Paper Scissors Battle")
        self.clock = pygame.time.Clock()
        
        # Game states
        self.game_state = "waiting_start"  # waiting_start, countdown, input_phase, show_result, game_over
        self.countdown_stage = 0  # 0=1, 1=2, 2=3, 3=GO
        self.countdown_timer = 0
        self.input_timer = 0
        
        # Player data
        self.player1_lives = 3
        self.player2_lives = 3
        self.player1_choice = None
        self.player2_choice = None
        
        # Heart shake animation
        self.heart_shake_timer = 0
        self.heart_shake_offset = 0
        
        # Load resources
        self.load_images()
        self.load_sounds()
        
        # Font for fallback text
        self.font = pygame.font.Font(None, 36)
        
    def load_images(self):
        """Load all game images with fallback rectangles if files don't exist"""
        self.images = {}
        
        # Define all required images
        image_files = {
            'background': 'background.png',
            'heart_full': 'heart_full.png',
            'heart_empty': 'heart_empty.png',
            'countdown_1': 'countdown_1.png',
            'countdown_2': 'countdown_2.png',
            'countdown_3': 'countdown_3.png',
            'countdown_go': 'countdown_go.png',
            'hand_p1_idle': 'hand_p1_idle.gif',
            'hand_p1_rock': 'hand_p1_rock.png',
            'hand_p1_scissors': 'hand_p1_scissors.png',
            'hand_p1_paper': 'hand_p1_paper.png',
            'hand_p2_idle': 'hand_p2_idle.gif',
            'hand_p2_rock': 'hand_p2_rock.png',
            'hand_p2_scissors': 'hand_p2_scissors.png',
            'hand_p2_paper': 'hand_p2_paper.png',
            'button': 'button.png',
            'player1_wins': 'player1_wins.png',
            'player2_wins': 'player2_wins.png'
        }
        
        for key, filename in image_files.items():
            try:
                if filename.endswith('.gif'):
                    # For GIF files, we'll create a placeholder surface
                    # In a real implementation, you'd need a GIF loader
                    self.images[key] = pygame.Surface((200, 200))
                    self.images[key].fill(GRAY)
                else:
                    self.images[key] = pygame.image.load(filename)
            except:
                # Create fallback rectangles with labels
                surf = pygame.Surface((100, 100))
                surf.fill(GRAY)
                text = self.font.render(key, True, BLACK)
                text_rect = text.get_rect(center=surf.get_rect().center)
                surf.blit(text, text_rect)
                self.images[key] = surf
                
    def load_sounds(self):
        """Load background music"""
        try:
            pygame.mixer.music.load('background_music.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # Loop forever
        except:
            print("Background music not found, continuing without sound")
            
    def handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                # Start game with spacebar
                if event.key == pygame.K_SPACE and self.game_state == "waiting_start":
                    self.start_countdown()
                    
                # Player inputs during input phase
                elif self.game_state == "input_phase":
                    # Player 1 controls (A, S, D)
                    if event.key == pygame.K_a:
                        self.player1_choice = "rock"
                    elif event.key == pygame.K_s:
                        self.player1_choice = "scissors"
                    elif event.key == pygame.K_d:
                        self.player1_choice = "paper"
                        
                    # Player 2 controls (Arrow keys)
                    elif event.key == pygame.K_LEFT:
                        self.player2_choice = "rock"
                    elif event.key == pygame.K_DOWN:
                        self.player2_choice = "scissors"
                    elif event.key == pygame.K_RIGHT:
                        self.player2_choice = "paper"
                        
        return True
        
    def start_countdown(self):
        """Start the countdown sequence"""
        self.game_state = "countdown"
        self.countdown_stage = 0
        self.countdown_timer = pygame.time.get_ticks()
        
    def update_countdown(self):
        """Update countdown animation"""
        current_time = pygame.time.get_ticks()
        
        if current_time - self.countdown_timer > 1000:  # 1 second per stage
            self.countdown_stage += 1
            self.countdown_timer = current_time
            
            if self.countdown_stage > 3:  # After GO!
                self.start_input_phase()
                
    def start_input_phase(self):
        """Start the input phase"""
        self.game_state = "input_phase"
        self.input_timer = pygame.time.get_ticks()
        self.player1_choice = None
        self.player2_choice = None
        
    def update_input_phase(self):
        """Update input phase and check for timeout"""
        current_time = pygame.time.get_ticks()
        
        # 2 seconds for input
        if current_time - self.input_timer > 2000:
            self.resolve_round()
            
    def resolve_round(self):
        """Resolve the current round and determine winner"""
        # Default to rock if no input
        if self.player1_choice is None:
            self.player1_choice = "rock"
        if self.player2_choice is None:
            self.player2_choice = "rock"
            
        winner = self.determine_winner(self.player1_choice, self.player2_choice)
        
        if winner == 1:
            self.player2_lives -= 1
            self.start_heart_shake()
        elif winner == 2:
            self.player1_lives -= 1
            self.start_heart_shake()
        # Draw - no lives lost
        
        # Check for game over
        if self.player1_lives <= 0 or self.player2_lives <= 0:
            self.game_state = "game_over"
            self.game_over_timer = pygame.time.get_ticks()
        else:
            self.game_state = "show_result"
            self.result_timer = pygame.time.get_ticks()
            
    def determine_winner(self, choice1, choice2):
        """Determine winner of rock paper scissors"""
        if choice1 == choice2:
            return 0  # Draw
        elif (choice1 == "rock" and choice2 == "scissors") or \
             (choice1 == "scissors" and choice2 == "paper") or \
             (choice1 == "paper" and choice2 == "rock"):
            return 1  # Player 1 wins
        else:
            return 2  # Player 2 wins
            
    def start_heart_shake(self):
        """Start heart container shake animation"""
        self.heart_shake_timer = pygame.time.get_ticks()
        
    def update_heart_shake(self):
        """Update heart shake animation"""
        current_time = pygame.time.get_ticks()
        if current_time - self.heart_shake_timer < 500:  # Shake for 0.5 seconds
            self.heart_shake_offset = math.sin((current_time - self.heart_shake_timer) * 0.05) * 5
        else:
            self.heart_shake_offset = 0
            
    def update_show_result(self):
        """Update result display phase"""
        current_time = pygame.time.get_ticks()
        if current_time - self.result_timer > 2000:  # Show result for 2 seconds
            self.game_state = "waiting_start"
            
    def update_game_over(self):
        """Update game over phase"""
        current_time = pygame.time.get_ticks()
        if current_time - self.game_over_timer > 5000:  # Show for 5 seconds
            self.return_to_homescreen()
            
    def return_to_homescreen(self):
        """Return to homescreen"""
        pygame.mixer.music.stop()
        pygame.quit()
        try:
            import homescreen
        except:
            # If homescreen.py doesn't exist, just quit
            sys.exit()
            
    def draw_background(self):
        """Draw the game background"""
        self.screen.blit(self.images['background'], (0, 0))
        
    def draw_hearts(self):
        """Draw player hearts with shake effect"""
        heart_size = 40
        heart_spacing = 50
        
        # Player 1 hearts (left side)
        start_x = 50
        start_y = 50 + self.heart_shake_offset
        
        for i in range(3):
            x = start_x + i * heart_spacing
            if i < self.player1_lives:
                heart_img = pygame.transform.scale(self.images['heart_full'], (heart_size, heart_size))
            else:
                heart_img = pygame.transform.scale(self.images['heart_empty'], (heart_size, heart_size))
            self.screen.blit(heart_img, (x, start_y))
            
        # Player 2 hearts (right side)
        start_x = SCREEN_WIDTH - 50 - 3 * heart_spacing
        
        for i in range(3):
            x = start_x + i * heart_spacing
            if i < self.player2_lives:
                heart_img = pygame.transform.scale(self.images['heart_full'], (heart_size, heart_size))
            else:
                heart_img = pygame.transform.scale(self.images['heart_empty'], (heart_size, heart_size))
            self.screen.blit(heart_img, (x, start_y))
            
    def draw_timer_area(self):
        """Draw the center timer/countdown area"""
        center_x = SCREEN_WIDTH // 2
        center_y = 80
        
        if self.game_state == "countdown":
            countdown_images = ['countdown_1', 'countdown_2', 'countdown_3', 'countdown_go']
            if self.countdown_stage < len(countdown_images):
                img = self.images[countdown_images[self.countdown_stage]]
                img_rect = img.get_rect(center=(center_x, center_y))
                self.screen.blit(img, img_rect)
        elif self.game_state == "waiting_start":
            # Show "Press SPACE to start" text
            text = self.font.render("Press SPACE to start", True, WHITE)
            text_rect = text.get_rect(center=(center_x, center_y))
            self.screen.blit(text, text_rect)
            
    def draw_hands(self):
        """Draw player hands"""
        # Player 1 hand (left side)
        p1_hand_center = (200, 300)
        
        if self.game_state in ["show_result", "input_phase"] and self.player1_choice:
            hand_img = self.images[f'hand_p1_{self.player1_choice}']
        else:
            hand_img = self.images['hand_p1_idle']
            
        hand_rect = hand_img.get_rect(center=p1_hand_center)
        self.screen.blit(hand_img, hand_rect)
        
        # Player 2 hand (right side)
        p2_hand_center = (600, 300)
        
        if self.game_state in ["show_result", "input_phase"] and self.player2_choice:
            hand_img = self.images[f'hand_p2_{self.player2_choice}']
        else:
            hand_img = self.images['hand_p2_idle']
            
        hand_rect = hand_img.get_rect(center=p2_hand_center)
        self.screen.blit(hand_img, hand_rect)
        
    def draw_buttons(self):
        """Draw control buttons at bottom"""
        button_width = 80
        button_height = 60
        button_y = SCREEN_HEIGHT - 80
        
        # Player 1 buttons
        p1_buttons = [(100, "A\nRock"), (200, "S\nScissors"), (300, "D\nPaper")]
        
        for x, label in p1_buttons:
            button_rect = pygame.Rect(x - button_width//2, button_y - button_height//2, 
                                    button_width, button_height)
            pygame.draw.rect(self.screen, GRAY, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            
            # Draw label
            lines = label.split('\n')
            for i, line in enumerate(lines):
                text = pygame.font.Font(None, 24).render(line, True, WHITE)
                text_rect = text.get_rect(center=(x, button_y - 10 + i * 20))
                self.screen.blit(text, text_rect)
                
        # Player 2 buttons
        p2_buttons = [(500, "←\nRock"), (600, "↓\nScissors"), (700, "→\nPaper")]
        
        for x, label in p2_buttons:
            button_rect = pygame.Rect(x - button_width//2, button_y - button_height//2, 
                                    button_width, button_height)
            pygame.draw.rect(self.screen, GRAY, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            
            # Draw label
            lines = label.split('\n')
            for i, line in enumerate(lines):
                text = pygame.font.Font(None, 24).render(line, True, WHITE)
                text_rect = text.get_rect(center=(x, button_y - 10 + i * 20))
                self.screen.blit(text, text_rect)
                
    def draw_game_over(self):
        """Draw game over screen"""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        if self.player1_lives <= 0:
            img = self.images['player2_wins']
        else:
            img = self.images['player1_wins']
            
        img_rect = img.get_rect(center=(center_x, center_y))
        self.screen.blit(img, img_rect)
        
    def update(self):
        """Update game logic"""
        if self.game_state == "countdown":
            self.update_countdown()
        elif self.game_state == "input_phase":
            self.update_input_phase()
        elif self.game_state == "show_result":
            self.update_show_result()
        elif self.game_state == "game_over":
            self.update_game_over()
            
        # Always update heart shake
        self.update_heart_shake()
        
    def draw(self):
        """Draw everything"""
        self.draw_background()
        
        if self.game_state != "game_over":
            self.draw_hearts()
            self.draw_timer_area()
            self.draw_hands()
            self.draw_buttons()
        else:
            self.draw_game_over()
            
        pygame.display.flip()
        
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()