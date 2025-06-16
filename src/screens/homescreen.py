# screens/homescreen.py

import pygame
import os
import math
from .screen_names import ScreenNames

class HomeScreen:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        pygame.display.set_caption("Stein Schere Papier")  # Setzt den Fenster-Titel

        # Alternativer Pfad-Mechanismus
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base = os.path.join(current_dir, "..")
        assets_dir = os.path.join(base, "assets")
        
        print(f"Suche Assets in: {assets_dir}")  # Debug-Ausgabe

        try:
            # Assets laden
            self.bg      = pygame.image.load(os.path.join(assets_dir, 'background_2.png')).convert()
            print("Background geladen")  # Debug-Ausgabe
            self.bg      = pygame.transform.scale(self.bg, (screen.get_width(), screen.get_height()))
            self.bg_width= self.bg.get_width()
            self.logo    = pygame.image.load(os.path.join(assets_dir, 'SSP_Logo.png')).convert_alpha()
            self.btn     = pygame.image.load(os.path.join(assets_dir, 'start_button.png')).convert_alpha()
            self.btn_hov = pygame.image.load(os.path.join(assets_dir, 'start_hover.png')).convert_alpha()
        except Exception as e:
            print(f"Fehler beim Laden: {str(e)}")
            print(f"Aktuelles Verzeichnis: {os.getcwd()}")
            print(f"Dateiliste: {os.listdir(assets_dir)}")
            raise SystemExit()

        # Hintergrund-Tiling
        self.bg_x = 0
        self.bg_speed = 100  # px/s

        # Button-Rechtecke
        w, h = 200, 60
        self.start_rect = pygame.Rect(0, 0, w, h)
        self.start_rect.center = (self.screen.get_width() // 2, 350)
        lw, lh = 64, 32
        self.lang_rect = pygame.Rect(20, 20, lw, lh)

        # Logo-Schwebe-Parameter
        self.float_time = 0.0
        self.float_range = 15  # Pixel
        self.float_speed = 2.0  # Zyklen pro Sekunde
        self.logo_offset = 0

    def on_enter(self):
        # Reset Scroll-Offset und Timer
        self.bg_x = 0
        self.float_time = 0.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_rect.collidepoint(event.pos):
                # Wechsel zum Player-vs-Player Screen
                self.manager.change_screen(ScreenNames.PVP)
            elif self.lang_rect.collidepoint(event.pos):
                print("Sprache ändern – hier Callback einbauen")

    def update(self, dt):
        # Background scroll
        self.bg_x = (self.bg_x - self.bg_speed * dt) % self.bg_width
        # Float Timer
        self.float_time += dt * self.float_speed * math.pi * 2
        # berechne vertikalen Offset
        self.logo_offset = math.sin(self.float_time) * self.float_range

    def draw(self):
        s = self.screen
        # Nahtlos scrollender Hintergrund: zwei Blits
        x = self.bg_x
        s.blit(self.bg, (x - self.bg_width, 0))
        s.blit(self.bg, (x, 0))

        # Logo mit Schweben
        logo_r = self.logo.get_rect(center=(s.get_width() // 2, 200 + self.logo_offset))
        s.blit(self.logo, logo_r)

        # Start-Button (Hover-Effekt)
        mpos = pygame.mouse.get_pos()
        img = self.btn_hov if self.start_rect.collidepoint(mpos) else self.btn
        btn_r = img.get_rect(center=self.start_rect.center)
        s.blit(img, btn_r)

        # Sprach-Button (nur als Platzhalter)
        pygame.draw.rect(s, (255, 255, 255, 50), self.lang_rect, border_radius=5)

        pygame.display.flip()  # Wichtig: Screen aktualisieren
