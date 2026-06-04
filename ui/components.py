"""
Composants UI réutilisables pour les menus modernes du jeu MMO 2D
Style moderne/épuré avec animations fluides
"""

import pygame
import math
from game.constants import s


class Panel:
    """Panneau avec gradient, bordure et coins arrondis."""

    def __init__(self, x, y, width, height, border_color=(88, 138, 255), bg_alpha=220):
        self.rect = pygame.Rect(x, y, width, height)
        self.border_color = border_color
        self.bg_alpha = bg_alpha
        self.surface = None

    def draw(self, screen, time=0.0):
        """Dessine le panneau avec gradient vertical."""
        w, h = self.rect.width, self.rect.height
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)

        for i in range(h):
            t = i / max(1, h - 1)
            alpha = int(self.bg_alpha - t * 30)
            r = int(16 + t * 6)
            g = int(22 + t * 8)
            b = int(40 + t * 12)
            pygame.draw.line(self.surface, (r, g, b, alpha), (0, i), (w, i))

        border_alpha = int(140 + math.sin(time * 1.5) * 30) if time else 140
        pygame.draw.rect(self.surface, (*self.border_color, border_alpha), (0, 0, w, h), 2, border_radius=s(12))
        screen.blit(self.surface, self.rect.topleft)


class Button:
    """Bouton moderne avec hover/press animation."""

    def __init__(self, x, y, width, height, text, font=None, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font or pygame.font.Font(None, s(28))
        self.action = action
        self.hovered = False
        self.pressed = False
        self._anim_time = 0.0

    def update(self, mouse_pos, dt):
        """Met à jour l'animation du bouton."""
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered:
            self._anim_time += dt

    def draw(self, screen, selected=False, time=0.0):
        """Dessine le bouton."""
        w, h = self.rect.width, self.rect.height
        x, y = self.rect.x, self.rect.y

        is_active = selected or self.hovered

        # Ombre
        shadow = pygame.Surface((w, h + s(6)), pygame.SRCALPHA)
        shadow_alpha = 140 if is_active else 80
        pygame.draw.rect(shadow, (0, 0, 0, shadow_alpha), (0, s(4), w, h), border_radius=s(10))
        screen.blit(shadow, (x, y))

        # Glow pour sélectionné
        if is_active:
            glow = pygame.Surface((w + s(14), h + s(14)), pygame.SRCALPHA)
            pulse = int(abs(math.sin(time * 3)) * 25) + 45
            pygame.draw.rect(glow, (112, 165, 255, pulse), (0, 0, w + s(14), h + s(14)), border_radius=s(14))
            screen.blit(glow, (x - s(7), y - s(7)))

        # Fond
        color = (112, 165, 255) if is_active else (62, 88, 148)
        border_c = (189, 214, 255) if is_active else (80, 100, 150)

        btn_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, (*color, 220), (0, 0, w, h), border_radius=s(10))
        highlight = tuple(min(255, c + 40) for c in color)
        pygame.draw.line(btn_surf, (*highlight, 140), (s(10), 2), (w - s(10), 2), 1)
        screen.blit(btn_surf, (x, y))

        # Bordure
        pygame.draw.rect(screen, border_c, self.rect, 2, border_radius=s(10))

        # Texte
        text_color = (255, 255, 255) if is_active else (200, 210, 235)
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        if is_active:
            shadow_t = self.font.render(self.text, True, (0, 0, 0))
            screen.blit(shadow_t, (text_rect.x + 1, text_rect.y + 1))
        screen.blit(text_surf, text_rect)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)


class Slider:
    """Curseur slider pour les options."""

    def __init__(self, x, y, width, label, values, current_index=0):
        self.rect = pygame.Rect(x, y, width, s(30))
        self.label = label
        self.values = values
        self.current_index = current_index
        self.font = pygame.font.Font(None, s(24))
        self.small_font = pygame.font.Font(None, s(18))

    def draw(self, screen, selected=False):
        """Dessine le slider."""
        # Label
        label_surf = self.font.render(self.label, True, (245, 247, 255))
        screen.blit(label_surf, (self.rect.x, self.rect.y + s(4)))

        # Track
        track_x = self.rect.x + s(180)
        track_w = self.rect.width - s(180)
        track_y = self.rect.y + s(8)

        pygame.draw.rect(screen, (40, 50, 80), (track_x, track_y, track_w, s(6)), border_radius=s(3))

        # Thumb
        thumb_x = track_x + int(track_w * self.current_index / max(1, len(self.values) - 1))
        thumb_color = (112, 165, 255) if selected else (88, 138, 255)
        pygame.draw.circle(screen, thumb_color, (thumb_x, track_y + s(3)), s(8))
        pygame.draw.circle(screen, (189, 214, 255), (thumb_x, track_y + s(3)), s(8), 2)

        # Value
        if 0 <= self.current_index < len(self.values):
            val = self.values[self.current_index]
            val_text = self.small_font.render(str(val), True, (200, 210, 235))
            screen.blit(val_text, (thumb_x - s(10), track_y - s(16)))

    def click(self, pos):
        """Gère un clic sur le slider. Retourne True si changé."""
        track_x = self.rect.x + s(180)
        track_w = self.rect.width - s(180)
        track_y = self.rect.y + s(4)
        track_rect = pygame.Rect(track_x, track_y - s(4), track_w, s(20))

        if track_rect.collidepoint(pos):
            ratio = (pos[0] - track_x) / max(1, track_w)
            self.current_index = int(ratio * (len(self.values) - 1) + 0.5)
            self.current_index = max(0, min(len(self.values) - 1, self.current_index))
            return True
        return False


class Toggle:
    """Interrupteur animé on/off."""

    def __init__(self, x, y, label, value=False):
        self.x = x
        self.y = y
        self.label = label
        self.value = value
        self.font = pygame.font.Font(None, s(24))
        self.width = s(50)
        self.height = s(26)

    def draw(self, screen, selected=False):
        """Dessine le toggle."""
        # Label
        label_surf = self.font.render(self.label, True, (245, 247, 255))
        screen.blit(label_surf, (self.x, self.y + s(3)))

        # Track
        track_x = self.x + s(200)
        track_color = (80, 180, 120) if self.value else (60, 70, 100)
        pygame.draw.rect(screen, track_color, (track_x, self.y, self.width, self.height), border_radius=s(13))

        # Thumb
        thumb_x = track_x + self.width - s(22) if self.value else track_x + s(4)
        thumb_color = (255, 255, 255) if self.value else (150, 160, 180)
        pygame.draw.circle(screen, thumb_color, (thumb_x + s(10), self.y + s(13)), s(9))

        # Bordure
        border_color = (112, 165, 255) if selected else (80, 100, 150)
        pygame.draw.rect(screen, border_color, (track_x, self.y, self.width, self.height), 2, border_radius=s(13))

    def click(self, pos):
        """Gère un clic. Retourne True si changé."""
        track_x = self.x + s(200)
        track_rect = pygame.Rect(track_x, self.y, self.width, self.height)
        if track_rect.collidepoint(pos):
            self.value = not self.value
            return True
        return False


class ScrollableList:
    """Liste scrollable pour les contrôles."""

    def __init__(self, x, y, width, height, items):
        self.rect = pygame.Rect(x, y, width, height)
        self.items = items  # [(label, value), ...]
        self.scroll_y = 0
        self.selected_index = 0
        self.item_height = s(50)
        self.font = pygame.font.Font(None, s(22))
        self.small_font = pygame.font.Font(None, s(18))

    def draw(self, screen, time=0.0):
        """Dessine la liste scrollable."""
        # Fond
        bg = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg, (16, 22, 40, 200), (0, 0, self.rect.width, self.rect.height), border_radius=s(8))
        pygame.draw.rect(bg, (60, 80, 130, 150), (0, 0, self.rect.width, self.rect.height), 1, border_radius=s(8))
        screen.blit(bg, self.rect.topleft)

        # Clip region
        screen.set_clip(self.rect)

        visible_items = self.rect.height // self.item_height
        start = self.scroll_y // self.item_height
        end = min(len(self.items), start + visible_items + 2)

        for i in range(start, end):
            item_y = self.rect.y + (i - start) * self.item_height - (self.scroll_y % self.item_height)
            label, value = self.items[i]
            is_selected = (i == self.selected_index)

            if is_selected:
                sel_bg = pygame.Surface((self.rect.width - s(8), self.item_height - s(4)), pygame.SRCALPHA)
                pulse = int(abs(math.sin(time * 2)) * 20) + 40
                pygame.draw.rect(sel_bg, (112, 165, 255, pulse), (0, 0, self.rect.width - s(8), self.item_height - s(4)), border_radius=s(6))
                screen.blit(sel_bg, (self.rect.x + s(4), item_y + s(2)))

            # Label
            label_surf = self.font.render(label, True, (245, 247, 255) if is_selected else (180, 190, 220))
            screen.blit(label_surf, (self.rect.x + s(12), item_y + s(6)))

            # Value
            value_surf = self.small_font.render(str(value), True, (140, 160, 200))
            screen.blit(value_surf, (self.rect.x + s(12), item_y + s(28)))

        screen.set_clip(None)

    def scroll(self, dy):
        """Scroll la liste."""
        max_scroll = max(0, len(self.items) * self.item_height - self.rect.height)
        self.scroll_y = max(0, min(max_scroll, self.scroll_y + dy))

    def select(self, index):
        """Sélectionne un élément."""
        self.selected_index = max(0, min(len(self.items) - 1, index))
        # Auto-scroll
        item_y = self.selected_index * self.item_height
        if item_y < self.scroll_y:
            self.scroll_y = item_y
        elif item_y + self.item_height > self.scroll_y + self.rect.height:
            self.scroll_y = item_y + self.item_height - self.rect.height
