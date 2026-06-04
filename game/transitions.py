"""
Système de transitions fondues entre les écrans du jeu
"""


class FadeTransition:
    """Transition fondu (fade in/out) entre les écrans."""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.alpha = 0
        self.fade_in = False
        self.fade_out = False
        self.fade_speed = 3
        self.callback = None
        self.active = False

    def start_fade_out(self, callback=None, speed=3):
        """Démarre un fondu sortant (écran → noir)."""
        self.fade_out = True
        self.fade_in = False
        self.callback = callback
        self.alpha = 0
        self.fade_speed = speed
        self.active = True

    def start_fade_in(self, speed=3):
        """Démarre un fondu entrant (noir → écran)."""
        self.fade_in = True
        self.fade_out = False
        self.alpha = 255
        self.fade_speed = speed
        self.active = True

    def update(self):
        """Met à jour la transition. Retourne True si terminée."""
        if not self.active:
            return True

        if self.fade_out:
            self.alpha += self.fade_speed
            if self.alpha >= 255:
                self.alpha = 255
                self.fade_out = False
                self.active = False
                if self.callback:
                    self.callback()
                return True
        elif self.fade_in:
            self.alpha -= self.fade_speed
            if self.alpha <= 0:
                self.alpha = 0
                self.fade_in = False
                self.active = False
                return True

        return False

    def draw(self, screen):
        """Dessine le overlay de fondu sur l'écran."""
        if self.alpha > 0:
            overlay = screen.copy()
            overlay.fill((0, 0, 0))
            overlay.set_alpha(int(self.alpha))
            screen.blit(overlay, (0, 0))


class ScreenTransition:
    """Gestionnaire de transitions entre écrans (menu → jeu, jeu → pause, etc.)."""

    def __init__(self, screen_width, screen_height):
        self.fade = FadeTransition(screen_width, screen_height)
        self.current_screen = "menu"
        self.target_screen = None
        self.screen_data = {}

    def switch_to(self, target_screen, data=None):
        """Lance une transition vers un autre écran."""
        if self.fade.active:
            return

        self.target_screen = target_screen
        self.screen_data = data or {}

        def on_fade_out_done():
            self.current_screen = self.target_screen

        self.fade.start_fade_out(callback=on_fade_out_done, speed=4)
        # Fade in après le fade out
        import threading
        def delayed_fade_in():
            import time
            while self.fade.active:
                time.sleep(0.016)
            self.fade.start_fade_in(speed=4)

        t = threading.Thread(target=delayed_fade_in, daemon=True)
        t.start()

    def update(self):
        """Met à jour la transition."""
        self.fade.update()

    def draw(self, screen):
        """Dessine la transition."""
        self.fade.draw(screen)

    def is_transitioning(self):
        """Vérifie si une transition est en cours."""
        return self.fade.active
