"""
Menu de pause - gros, lisible, moderne
"""

import pygame
import math


class PauseMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.visible = False
        self._time = 0.0

        self.WHITE = (245, 247, 255)
        self.BLACK = (8, 12, 24)
        self.GRAY = (132, 144, 170)
        self.BLUE = (88, 138, 255)
        self.GREEN = (84, 214, 125)
        self.RED = (245, 98, 98)
        self.BUTTON_DEFAULT = (62, 88, 148)
        self.BUTTON_SELECTED = (112, 165, 255)
        self.BUTTON_BORDER = (189, 214, 255)

        self.selected_button = 0
        self.buttons = [
            {"text": "Reprendre", "action": "resume"},
            {"text": "Menu principal", "action": "menu"},
            {"text": "Quitter", "action": "quit"}
        ]

    def _W(self):
        return self.screen.get_width()

    def _H(self):
        return self.screen.get_height()

    def _font(self, pct):
        return max(14, int(self._H() * pct / 100))

    def draw(self):
        if not self.visible:
            return

        self._time += 0.016
        w, h = self._W(), self._H()

        # Fond semi-transparent
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Panneau central - GRAND
        panel_w = int(w * 0.35)
        panel_h = int(h * 0.65)
        panel_x = (w - panel_w) // 2
        panel_y = (h - panel_h) // 2

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        for i in range(panel_h):
            t = i / panel_h
            alpha = int(235 - t * 15)
            r = int(18 + t * 5)
            g = int(25 + t * 5)
            b = int(45 + t * 8)
            pygame.draw.line(panel, (r, g, b, alpha), (0, i), (panel_w, i))
        border_alpha = int(120 + math.sin(self._time * 2) * 30)
        pygame.draw.rect(panel, (88, 138, 255, border_alpha), (0, 0, panel_w, panel_h), 3, border_radius=16)
        self.screen.blit(panel, (panel_x, panel_y))

        # Titre PAUSE - TRÈS GROS
        title_font = pygame.font.Font(None, self._font(8))
        title = title_font.render("PAUSE", True, self.WHITE)
        title_rect = title.get_rect(center=(w // 2, panel_y + int(panel_h * 0.12)))
        shadow = title_font.render("PAUSE", True, (0, 0, 0))
        self.screen.blit(shadow, (title_rect.x + 3, title_rect.y + 3))
        self.screen.blit(title, title_rect)

        # Ligne séparatrice
        sep_y = panel_y + int(panel_h * 0.2)
        pygame.draw.line(self.screen, (88, 138, 255, 150), (panel_x + 30, sep_y), (panel_x + panel_w - 30, sep_y), 2)

        # Boutons - GRANDS
        btn_w = int(panel_w * 0.7)
        btn_h = int(panel_h * 0.1)
        btn_cx = w // 2
        start_y = panel_y + int(panel_h * 0.28)
        spacing = int(panel_h * 0.13)

        for i, button in enumerate(self.buttons):
            cy = start_y + i * spacing
            selected = (i == self.selected_button)
            self._draw_button(button["text"], btn_cx, cy, btn_w, btn_h, selected)

        # Instructions en bas
        inst_font = pygame.font.Font(None, self._font(2))
        inst = inst_font.render("Echap: Reprendre  |  Haut/Bas: Naviguer  |  Entree: Selectionner", True, self.GRAY)
        inst_rect = inst.get_rect(center=(w // 2, panel_y + panel_h - int(panel_h * 0.08)))
        self.screen.blit(inst, inst_rect)

    def _draw_button(self, text, cx, cy, w, h, selected=False):
        x = cx - w // 2
        y = cy - h // 2
        rect = pygame.Rect(x, y, w, h)
        br = max(6, h // 5)

        # Ombre
        shadow = pygame.Surface((w, h + 8), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 140 if selected else 80), (0, 4, w, h), border_radius=br)
        self.screen.blit(shadow, (x, y))

        # Glow
        if selected:
            glow = pygame.Surface((w + 16, h + 16), pygame.SRCALPHA)
            pulse = int(abs(math.sin(self._time * 3)) * 25) + 45
            pygame.draw.rect(glow, (112, 165, 255, pulse), (0, 0, w + 16, h + 16), border_radius=br + 4)
            self.screen.blit(glow, (x - 8, y - 8))

        # Fond
        color = self.BUTTON_SELECTED if selected else self.BUTTON_DEFAULT
        border_c = self.BUTTON_BORDER if selected else (80, 100, 150)
        btn_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, (*color, 230), (0, 0, w, h), border_radius=br)
        highlight = tuple(min(255, c + 40) for c in color)
        pygame.draw.line(btn_surf, (*highlight, 150), (10, 2), (w - 10, 2), 1)
        self.screen.blit(btn_surf, (x, y))
        pygame.draw.rect(self.screen, border_c, rect, 2, border_radius=br)

        # Texte
        font = pygame.font.Font(None, self._font(3))
        text_color = (255, 255, 255) if selected else (200, 210, 235)
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=(cx, cy))
        if selected:
            shadow_t = font.render(text, True, (0, 0, 0))
            self.screen.blit(shadow_t, (text_rect.x + 2, text_rect.y + 2))
        self.screen.blit(text_surf, text_rect)

        return rect

    def handle_event(self, event):
        if not self.visible:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            w, h = self._W(), self._H()
            panel_w = int(w * 0.35)
            panel_h = int(h * 0.65)
            btn_w = int(panel_w * 0.7)
            btn_h = int(panel_h * 0.1)
            btn_cx = w // 2
            start_y = (h - panel_h) // 2 + int(panel_h * 0.28)
            spacing = int(panel_h * 0.13)

            for i, button in enumerate(self.buttons):
                cy = start_y + i * spacing
                rect = pygame.Rect(btn_cx - btn_w // 2, cy - btn_h // 2, btn_w, btn_h)
                if rect.collidepoint(mouse_pos):
                    self.selected_button = i
                    return button["action"]

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "resume"
            elif event.key == pygame.K_UP:
                self.selected_button = (self.selected_button - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected_button = (self.selected_button + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                return self.buttons[self.selected_button]["action"]

        return None

    def show(self):
        self.visible = True
        self.selected_button = 0

    def hide(self):
        self.visible = False
