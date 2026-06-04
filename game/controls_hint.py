"""
Affichage dynamique des raccourcis clavier en bas de l'ecran
"""

import pygame


class ControlsHint:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 20)
        self.visible = True
        self.alpha = 180
        self.target_alpha = 180

    def update_screen_size(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, dt):
        pass

    def draw(self, screen, context="normal"):
        if not self.visible:
            return

        if context == "inventory":
            hints = [("I", "Fermer"), ("Clic", "Utiliser"), ("Clic droit", "Manger")]
        else:
            hints = [
                ("ZQSD", "Deplacer"),
                ("I", "Inventaire"),
                ("Clic", "Attaquer/Recolter"),
                ("H", "Manger"),
                ("Echap", "Pause"),
            ]

        panel_height = 30
        panel_y = self.screen_height - panel_height - 5

        bg = pygame.Surface((self.screen_width, panel_height), pygame.SRCALPHA)
        bg.fill((10, 15, 30, int(self.alpha * 0.6)))
        screen.blit(bg, (0, panel_y))

        x_off = 20
        for key, label in hints:
            kt = self.font.render(key, True, (200, 220, 255))
            kb = pygame.Surface((kt.get_width() + 10, 20), pygame.SRCALPHA)
            kb.fill((50, 70, 120, int(self.alpha * 0.8)))
            screen.blit(kb, (x_off - 5, panel_y + 5))
            screen.blit(kt, (x_off, panel_y + 6))
            x_off += kt.get_width() + 15
            lt = self.font.render(label, True, (160, 170, 190))
            lt.set_alpha(int(self.alpha))
            screen.blit(lt, (x_off, panel_y + 6))
            x_off += lt.get_width() + 25
