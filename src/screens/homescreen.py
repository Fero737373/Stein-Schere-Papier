import pygame, os, math
from game import ScreenNames

class HomeScreen:
    def __init__(self, app):
        self.app = app
        # Pfad zum assets-Ordner (zwei Ebenen über diesem File)
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets'))
        # Assets laden
        self.bg      = pygame.image.load(os.path.join(base, 'bg.png')).convert()
        self.logo    = pygame.image.load(os.path.join(base, 'logo.png')).convert_alpha()
        self.btn     = pygame.image.load(os.path.join(base, 'btn_start.png')).convert_alpha()
        self.btn_hov = pygame.image.load(os.path.join(base, 'btn_start_hover.png')).convert_alpha()
        self.btn_lang = pygame.image.load(os.path.join(base, 'btn_de.png')).convert_alpha()
        self.btn_lang_hov = pygame.image.load(os.path.join(base, 'btn_de_hover.png')).convert_alpha()

        # Hintergrund-Tiling
        self.bg_width = self.bg.get_width()
        self.bg_x = 0
        self.bg_speed = 100  # px/s

        # Button-Rechtecke
        w,h = 200,60
        self.start_rect = pygame.Rect(0,0, w,h)
        self.start_rect.center = (self.app.screen.get_width()//2, 350)
        lw, lh = 64,32
        self.lang_rect = pygame.Rect(20,20, lw,lh)

        # Logo-Schwebe-Parameter
        self.float_time = 0.0
        self.float_range = 15  # Pixel
        self.float_speed = 2.0  # Zyklen pro Sekunde

    def on_enter(self):
        # Reset Scroll-Offset und Timer
        self.bg_x = 0
        self.float_time = 0.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_rect.collidepoint(event.pos):
                self.app.change_screen(ScreenNames.MENU)
            elif self.lang_rect.collidepoint(event.pos):
                self.app.change_screen(ScreenNames.SETTINGS)

    def update(self, dt):
        # Background scroll
        self.bg_x -= self.bg_speed * dt
        if self.bg_x <= -self.bg_width:
            self.bg_x += self.bg_width
        # Float Timer
        self.float_time += dt * self.float_speed * math.pi * 2
        # berechne vertikalen Offset
        self.logo_offset = math.sin(self.float_time) * self.float_range

    def draw(self):
        s = self.app.screen
        # BG zweimal nebeneinander
        x = int(self.bg_x)
        s.blit(self.bg, (x, 0))
        s.blit(self.bg, (x + self.bg_width, 0))

        # Logo mit Schweben
        logo_r = self.logo.get_rect(center=(s.get_width()//2, 200 + self.logo_offset))
        s.blit(self.logo, logo_r)

        # Start-Button (Hover-Effekt)
        mpos = pygame.mouse.get_pos()
        if self.start_rect.collidepoint(mpos):
            img = self.btn_hov
        else:
            img = self.btn
        btn_r = img.get_rect(center=self.start_rect.center)
        s.blit(img, btn_r)

        # Sprach-Button (Hover-Effekt)
        if self.lang_rect.collidepoint(mpos):
            lang_img = self.btn_lang_hov
        else:
            lang_img = self.btn_lang
        s.blit(lang_img, self.lang_rect)
