"""
HUD amélioré pour le jeu MMO 2D
Barres gradient, ombres portées, indicateur faim animé
"""

import pygame
import math
from .constants import COLORS


class HUD:
    def __init__(self, font):
        self.font = font
        self.small_font = pygame.font.Font(None, 18)
        self.icon_font = pygame.font.Font(None, 20)
        self.time = 0.0

    def update(self, dt):
        """Met à jour les animations du HUD."""
        self.time += dt

    def _draw_panel(self, screen, x, y, width, height, title=""):
        """Dessine un panneau avec dégradé et bordure lumineuse."""
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        # Dégradé vertical
        for i in range(height):
            t = i / height
            alpha = int(210 - t * 40)
            r = int(14 + t * 6)
            g = int(20 + t * 8)
            b = int(38 + t * 12)
            pygame.draw.line(panel, (r, g, b, alpha), (0, i), (width, i))
        # Bordure
        pygame.draw.rect(panel, (80, 120, 200, 150), panel.get_rect(), 1, border_radius=10)
        screen.blit(panel, (x, y))

        if title:
            title_surf = self.small_font.render(title, True, (140, 180, 255))
            screen.blit(title_surf, (x + 12, y + 6))

    def _draw_bar(self, screen, x, y, width, height, ratio, bar_color, bg_color=(20, 20, 35)):
        """Dessine une barre avec gradient vertical et ombre."""
        ratio = max(0, min(1, ratio))

        # Fond avec ombre
        bg_surf = pygame.Surface((width, height + 2), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (10, 10, 20, 150), (0, 1, width, height), border_radius=4)
        screen.blit(bg_surf, (x, y))

        # Fond de la barre
        pygame.draw.rect(screen, bg_color, (x, y, width, height), border_radius=4)

        # Barre remplie avec gradient
        fill_width = int(width * ratio)
        if fill_width > 0:
            bar_surf = pygame.Surface((fill_width, height), pygame.SRCALPHA)
            for i in range(height):
                t = i / height
                # Gradient : couleur plus claire en haut, plus sombre en bas
                r = min(255, int(bar_color[0] * (1.1 - t * 0.3)))
                g = min(255, int(bar_color[1] * (1.1 - t * 0.3)))
                b = min(255, int(bar_color[2] * (1.1 - t * 0.3)))
                pygame.draw.line(bar_surf, (r, g, b, 220), (0, i), (fill_width, i))
            # Bordure arrondie
            pygame.draw.rect(bar_surf, (255, 255, 255, 40), (0, 0, fill_width, height), 1, border_radius=4)
            screen.blit(bar_surf, (x, y))

        # Bordure extérieure
        pygame.draw.rect(screen, (60, 70, 100), (x, y, width, height), 1, border_radius=4)

    def _draw_text_shadow(self, screen, text, pos, font=None, color=(255, 255, 255)):
        """Dessine du texte avec ombre portée."""
        if font is None:
            font = self.font
        shadow = font.render(text, True, (0, 0, 0))
        main = font.render(text, True, color)
        screen.blit(shadow, (pos[0] + 1, pos[1] + 1))
        screen.blit(main, pos)

    def draw(self, screen, player, game_instance=None):
        self.time += 0.016  # ~60fps

        bar_width = 160
        bar_height = 16

        panel_x, panel_y = 12, 12
        panel_width, panel_height = 530, 115

        self._draw_panel(screen, panel_x, panel_y, panel_width, panel_height, "STATS")

        # ── Health ────────────────────────────────────────────────────────
        health_y = panel_y + 25
        health_ratio = max(0, player.health / player.max_health)

        # Couleur dynamique avec interpolation
        if health_ratio < 0.33:
            health_color = (220, 50, 50)
        elif health_ratio < 0.66:
            health_color = (220, 180, 40)
        else:
            health_color = (50, 200, 80)

        self._draw_text_shadow(screen, f"PV {int(player.health)}/{player.max_health}",
                               (panel_x + 15, health_y), self.font, COLORS['WHITE'])
        self._draw_bar(screen, panel_x + 15, health_y + 20, bar_width, bar_height, health_ratio, health_color)

        # ── Hunger ────────────────────────────────────────────────────────
        hunger_y = panel_y + 25
        hunger_ratio = max(0, player.hunger / player.max_hunger)

        # Animation de pulsation quand la faim est basse
        hunger_warning = player.hunger < 20
        if hunger_warning:
            pulse = abs(math.sin(self.time * 4)) * 0.3 + 0.7
            hunger_color = (int(220 * pulse), int(60 * pulse), int(40 * pulse))
        elif player.hunger < 40:
            hunger_color = (220, 160, 40)
        else:
            hunger_color = (200, 140, 60)

        self._draw_text_shadow(screen, f"Faim {int(player.hunger)}/{player.max_hunger}",
                               (panel_x + 200, hunger_y), self.font, COLORS['WHITE'])
        self._draw_bar(screen, panel_x + 200, hunger_y + 20, bar_width, bar_height, hunger_ratio, hunger_color)

        # ── Level / XP ────────────────────────────────────────────────────
        level = getattr(player, 'level', 1)
        xp = getattr(player, 'xp', 0)
        xp_needed = level * 100
        xp_ratio = min(1.0, xp / xp_needed) if xp_needed > 0 else 0

        self._draw_text_shadow(screen, f"Nv.{level}",
                               (panel_x + 15, panel_y + 65), self.font, COLORS['YELLOW'])
        self._draw_text_shadow(screen, f"XP: {xp}/{xp_needed}",
                               (panel_x + 75, panel_y + 68), self.small_font, (180, 190, 220))

        # Barre XP avec couleur bleue dégradée
        self._draw_bar(screen, panel_x + 75, panel_y + 85, 120, 12, xp_ratio, (80, 140, 240))

        # ── Weapon indicator ──────────────────────────────────────────────
        weapon_name = "Mains"
        dmg = player.BARE_HANDS_DAMAGE
        for slot in player.inventory.slots:
            if slot and slot.item.type in ("weapon", "tool"):
                weapon_name = slot.item.name[:14]
                dmg = player.WEAPON_DAMAGE.get(slot.item.name, player.BARE_HANDS_DAMAGE)
                break

        self._draw_text_shadow(screen, f"{weapon_name} ({dmg})",
                               (panel_x + 320, panel_y + 35), self.small_font, COLORS['ORANGE'])

        # ── Build mode indicator ──────────────────────────────────────────
        if player.build_mode:
            build_panel_y = panel_y + panel_height + 8
            build_width = 280
            self._draw_panel(screen, panel_x, build_panel_y, build_width, 45)

            # Badge animé
            badge_pulse = int(abs(math.sin(self.time * 2)) * 30) + 225
            self._draw_text_shadow(screen, "CONSTRUCTION",
                                   (panel_x + 15, build_panel_y + 12), self.font, (255, badge_pulse, 80))
            self._draw_text_shadow(screen, f"Objet: {player.selected_building.upper()}",
                                   (panel_x + 15, build_panel_y + 28), self.small_font, (140, 180, 255))
