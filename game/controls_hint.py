"""
Controls Hint - Battle Royale
"""

import pygame
from .constants import s


class ControlsHint:
    def __init__(self, screen_width, screen_height):
        self.opacity = 0.0
        self.fading_in = True
        self.hints = [
            "ZQSD / Fleches: Se deplacer",
            "Souris: Viser et attaquer",
            "E: Ramasser objet",
            "F: Boire / Soigner",
            "TAB: Inventaire",
            "M: Minimap",
        ]

    def update(self, dt, mouse_x, mouse_y, screen_width, screen_height):
        if self.fading_in:
            self.opacity = min(1.0, self.opacity + dt * 2.0)
        if self.opacity >= 1.0:
            self.fading_in = False

    def draw(self, screen, player=None, controls=None):
        if self.opacity <= 0:
            return

        w, h = screen.get_size()
        alpha = int(180 * self.opacity)
        panel_w = s(280)
        panel_h = s(200)
        px = w - panel_w - s(20)
        py = h - panel_h - s(20)

        font = pygame.font.Font(None, s(22))

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (15, 20, 35, alpha), (0, 0, panel_w, panel_h), border_radius=8)
        pygame.draw.rect(panel, (55, 100, 190, alpha), (0, 0, panel_w, panel_h), 2, border_radius=8)

        title = font.render("Commandes", True, (170, 200, 255))
        panel.blit(title, (s(15), s(12)))

        for i, hint in enumerate(self.hints):
            txt = font.render(hint, True, (200, 210, 230))
            panel.blit(txt, (s(15), s(35) + i * s(26)))

        screen.blit(panel, (px, py))
