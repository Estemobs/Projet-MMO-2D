"""
Cycle jour/nuit avec assombrissement progressif
"""

import pygame
import math


class DayNightCycle:
    """Gère le cycle jour/nuit du jeu."""

    def __init__(self):
        self.time_of_day = 0.0  # 0.0 = minuit, 0.5 = midi, 1.0 = minuit
        self.day_duration = 300.0  # Durée d'un jour complet en secondes (5 min)
        self.day_progress = 0.0

        # Couleurs d'ambiance par période
        self.colors = {
            'night': (10, 15, 40),        # Nuit profonde
            'dawn': (40, 30, 60),          # Aube
            'day': (0, 0, 0),             # Jour (pas de filtre)
            'dusk': (50, 30, 40),          # Crépuscule
        }

        # Alpha max pour l'assombrissement (0-255)
        self.max_darkness = 160

    def update(self, dt):
        """Met à jour le cycle jour/nuit."""
        self.time_of_day += dt / self.day_duration
        if self.time_of_day >= 1.0:
            self.time_of_day -= 1.0

        # Calculer la couleur d'ambiance
        self.day_progress = self.time_of_day

    def get_darkness(self):
        """Retourne le niveau d'obscurité (0-255) selon l'heure."""
        t = self.time_of_day

        # Nuit : 0.0-0.25 et 0.75-1.0
        # Aube : 0.25-0.35
        # Jour : 0.35-0.65
        # Crépuscule : 0.65-0.75
        if t < 0.2 or t > 0.8:
            return self.max_darkness
        elif t < 0.3:
            # Aube (nuit → jour)
            progress = (t - 0.2) / 0.1
            return int(self.max_darkness * (1.0 - progress))
        elif t < 0.7:
            return 0
        else:
            # Crépuscule (jour → nuit)
            progress = (t - 0.7) / 0.1
            return int(self.max_darkness * progress)

    def get_ambient_color(self):
        """Retourne la couleur d'ambiance RGB."""
        t = self.time_of_day

        if t < 0.2 or t > 0.8:
            return self.colors['night']
        elif t < 0.3:
            progress = (t - 0.2) / 0.1
            return self._lerp_color(self.colors['night'], self.colors['day'], progress)
        elif t < 0.65:
            return self.colors['day']
        else:
            progress = (t - 0.65) / 0.15
            return self._lerp_color(self.colors['day'], self.colors['night'], min(1.0, progress))

    def _lerp_color(self, color1, color2, t):
        """Interpolation linéaire entre deux couleurs."""
        t = max(0.0, min(1.0, t))
        return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

    def is_night(self):
        """Vérifie si c'est la nuit."""
        return self.get_darkness() > 50

    def get_time_string(self):
        """Retourne l'heure formatée."""
        hours = int(self.time_of_day * 24)
        minutes = int((self.time_of_day * 24 - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"

    def get_period_name(self):
        """Retourne le nom de la période actuelle."""
        t = self.time_of_day
        if t < 0.2 or t > 0.8:
            return "Nuit"
        elif t < 0.3:
            return "Aube"
        elif t < 0.65:
            return "Jour"
        else:
            return "Crépuscule"

    def draw_overlay(self, screen):
        """Dessine le filtre d'ambiance sur l'écran."""
        darkness = self.get_darkness()
        if darkness <= 0:
            return

        ambient_color = self.get_ambient_color()
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((*ambient_color, darkness))
        screen.blit(overlay, (0, 0))

    def draw_hud_indicator(self, screen, x, y):
        """Affiche un indicateur de l'heure en haut de l'écran."""
        font = pygame.font.Font(None, 22)
        time_str = self.get_time_string()
        period = self.get_period_name()

        # Couleur selon la période
        period_colors = {
            "Nuit": (100, 120, 200),
            "Aube": (255, 180, 100),
            "Jour": (255, 255, 200),
            "Crépuscule": (200, 150, 100),
        }
        color = period_colors.get(period, (200, 200, 200))

        # Fond
        text = font.render(f"  {time_str}  {period}", True, color)
        bg_rect = pygame.Rect(x - 5, y - 2, text.get_width() + 10, text.get_height() + 4)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((20, 25, 40, 180))
        screen.blit(bg_surface, bg_rect)
        screen.blit(text, (x, y))
