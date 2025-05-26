import pygame
import os
import math

# Dummy-ScreenNames, passt das bei euch an!
class ScreenNames:
    HOME = "home"
    MENU = "menu"
    OTHER = "other"

class HomeScreen:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        # Pfad zum assets-Ordner (zwei Ebenen über diesem File)
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets'))
        # Assets laden
        self.bg      = pygame.image.load(os.path.join(base, 'background_2.png')).convert()
        self.bg = pygame.transform.scale(self.bg, (self.screen.get_width(), self.screen.get_height()))
        self.bg_width = self.bg.get_width()
        self.logo    = pygame.image.load(os.path.join(base, 'SSP_Logo.png')).convert_alpha()
        self.btn     = pygame.image.load(os.path.join(base, 'start_button.png')).convert_alpha()
        self.btn_hov = pygame.image.load(os.path.join(base, 'start_hover.png')).convert_alpha()

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
                print("Start gedrückt – wechsele ins Menu")
                # Screen-Wechsel über den Manager
                self.manager.change_screen(ScreenNames.MENU)
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


# Beispielhafter MenuScreen, integriert in das Screen Management
class MenuScreen:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.font = pygame.font.SysFont(None, 48)

    def on_enter(self):
        pass

    def handle_event(self, event):
        # Beispiel: Mit ESC kehren wir zurück zum HomeScreen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.change_screen(ScreenNames.HOME)

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((30, 30, 30))
        text = self.font.render("Menü", True, (255, 255, 255))
        rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, rect)


# Einfacher Screen-Manager, der zwischen den Screens wechselt
class ScreenManager:
    def __init__(self, screen):
        self.screen = screen
        # Starte mit dem HomeScreen
        self.current_screen = HomeScreen(screen, self)
        self.current_screen.on_enter()

    def change_screen(self, screen_name):
        if screen_name == ScreenNames.MENU:
            self.current_screen = MenuScreen(self.screen, self)
            self.current_screen.on_enter()
        elif screen_name == ScreenNames.HOME:
            self.current_screen = HomeScreen(self.screen, self)
            self.current_screen.on_enter()
        # Weitere Screens lassen sich hier einbauen

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.current_screen.handle_event(event)
            self.current_screen.update(dt)
            self.current_screen.draw()
            pygame.display.flip()

        pygame.quit()


def main():
    pygame.init()
    # Fenster exakt 800×600
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Startscreen Beispiel")
    manager = ScreenManager(screen)
    manager.run()


if __name__ == '__main__':
    main()
