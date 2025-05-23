import pygame, os, math
from screen_names import ScreenNames

class HomeScreen:
    def __init__(self, screen):
        self.screen = screen
        # Pfad zum assets-Ordner (zwei Ebenen über diesem File)
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets'))
        # Assets laden
        self.bg      = pygame.image.load(os.path.join(base, 'background_2.png')).convert()
        self.bg_width = self.bg.get_width()
        self.logo    = pygame.image.load(os.path.join(base, 'SSP_Hand.png')).convert_alpha()
        self.btn     = pygame.image.load(os.path.join(base, 'start_button.png')).convert_alpha()
        self.btn_hov = pygame.image.load(os.path.join(base, 'start_hover.png')).convert_alpha()

        # Hintergrund-Tiling
        self.bg_width = self.bg.get_width()
        self.bg_x = 0
        self.bg_speed = 100  # px/s

        # Button-Rechtecke
        w,h = 200,60
        self.start_rect = pygame.Rect(0,0, w,h)
        self.start_rect.center = (self.screen.get_width() // 2, 350)
        lw, lh = 64,32
        self.lang_rect = pygame.Rect(20,20, lw,lh)

        # Logo-Schwebe-Parameter
        self.float_time = 0.0
        self.float_range = 15  # Pixel
        self.float_speed = 2.0  # Zyklen pro Sekunde

        self.logo_offset = 0    # <<< --- Das ist der wichtige Fix!

    def on_enter(self):
        # Reset Scroll-Offset und Timer
        self.bg_x = 0
        self.float_time = 0.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_rect.collidepoint(event.pos):
                # Hier brauchst du Zugriff auf die App, falls du den Screen wechseln willst
                # Das musst du ggf. anders lösen, z.B. über einen Callback
                pass
            elif self.lang_rect.collidepoint(event.pos):
                pass

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
        s = self.screen
        # Hintergrund exakt einmal zeichnen, ohne Tiling und ohne Skalierung
        s.blit(self.bg, (0, 0))

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
