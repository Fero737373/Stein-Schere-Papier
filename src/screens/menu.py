import pygame
import os
from screen_names import ScreenNames

class MenuScreen:
    def __init__(self, screen, game):  # Changed to match other screens
        self.screen = screen
        self.game = game  # Changed from app to game
        
        # Fenstergrößen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        # Farben
        self.BG_COLOR = (30, 30, 50)
        self.BUTTON_COLOR = (60, 60, 80)
        self.HOVER_COLOR = (80, 80, 100)
        self.TEXT_COLOR = (255, 255, 255)
        
        # Button-Größen und Positionen
        button_width = 200
        button_height = 50
        button_spacing = 20
        
        # Erstelle Rechtecke für Buttons
        self.btn_pvp_rect = pygame.Rect(0, 0, button_width, button_height)
        self.btn_p1p2_rect = pygame.Rect(0, 0, button_width, button_height)
        self.btn_settings_rect = pygame.Rect(0, 0, button_width, button_height)
        
        # Zentriere Buttons
        self.btn_pvp_rect.center = (self.width // 2, self.height // 2 - button_height - button_spacing)
        self.btn_p1p2_rect.center = (self.width // 2, self.height // 2)
        self.btn_settings_rect.center = (self.width // 2, self.height // 2 + button_height + button_spacing)
        
        # Font für Text
        self.font = pygame.font.Font(None, 36)
        
        # Text für Buttons
        self.text_pvp = self.font.render("Player vs Bot", True, self.TEXT_COLOR)
        self.text_p1p2 = self.font.render("Player vs Player", True, self.TEXT_COLOR)
        self.text_settings = self.font.render("Einstellungen", True, self.TEXT_COLOR)

    def on_enter(self):
        print("MenuScreen: Entered")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.btn_pvp_rect.collidepoint(pos):
                print("Player vs Bot gewählt")
                self.game.switch_screen(ScreenNames.BATTLE)  # Changed from app to game
            elif self.btn_p1p2_rect.collidepoint(pos):
                print("Player 1 vs Player 2 gewählt")
                self.game.switch_screen(ScreenNames.BATTLE)
            elif self.btn_settings_rect.collidepoint(pos):
                print("Einstellungen gewählt")
                self.game.switch_screen(ScreenNames.SETTINGS)

    def update(self, dt):
        pass

    def draw(self):
        # Hintergrund
        self.screen.fill(self.BG_COLOR)
        
        # Mausposition für Hover-Effekte
        mpos = pygame.mouse.get_pos()
        
        # Zeichne Buttons mit Hover-Effekt
        for rect, text in [
            (self.btn_pvp_rect, self.text_pvp),
            (self.btn_p1p2_rect, self.text_p1p2),
            (self.btn_settings_rect, self.text_settings)
        ]:
            color = self.HOVER_COLOR if rect.collidepoint(mpos) else self.BUTTON_COLOR
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            
            # Zentriere Text auf Button
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
