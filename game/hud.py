import pygame
from .constants import COLORS

class HUD:
    def __init__(self, font):
        self.font = font
        self.small_font = pygame.font.Font(None, 18)
        self.icon_font = pygame.font.Font(None, 20)

    def _draw_bar(self, screen, x, y, width, height, ratio, bar_color, bg_color=(20, 20, 35)):
        """Dessine une barre avec fond et bordure."""
        pygame.draw.rect(screen, bg_color, (x, y, width, height), border_radius=4)
        pygame.draw.rect(screen, bar_color, (x, y, int(width * ratio), height), border_radius=4)
        pygame.draw.rect(screen, COLORS['LIGHT_GRAY'], (x, y, width, height), 2, border_radius=4)

    def _draw_panel(self, screen, x, y, width, height, title=""):
        """Dessine un panneau avec titre."""
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(panel, (16, 22, 40, 200), panel.get_rect(), border_radius=8)
        pygame.draw.rect(panel, (117, 171, 255, 200), panel.get_rect(), 2, border_radius=8)
        screen.blit(panel, (x, y))

        if title:
            title_surf = self.small_font.render(title, True, COLORS['LIGHT_BLUE'])
            screen.blit(title_surf, (x + 10, y + 5))

    def draw(self, screen, player, game_instance=None):
        bar_width = 160
        bar_height = 18

        panel_x, panel_y = 12, 12
        panel_width, panel_height = 520, 110

        self._draw_panel(screen, panel_x, panel_y, panel_width, panel_height, "⚔ STATS")

        # ── Health ────────────────────────────────────────────────────────
        health_y = panel_y + 28
        health_text = self.font.render(
            f"❤ {int(player.health)}/{player.max_health}", True, COLORS['WHITE'])
        screen.blit(health_text, (panel_x + 15, health_y))

        health_ratio = max(0, player.health / player.max_health)
        health_color = COLORS['RED'] if health_ratio < 0.33 else (COLORS['YELLOW'] if health_ratio < 0.66 else COLORS['GREEN'])
        self._draw_bar(screen, panel_x + 15, health_y + 20, bar_width, bar_height, health_ratio, health_color)

        # ── Hunger ────────────────────────────────────────────────────────
        hunger_y = panel_y + 28
        hunger_text = self.font.render(
            f"🍗 {int(player.hunger)}/{player.max_hunger}", True, COLORS['WHITE'])
        screen.blit(hunger_text, (panel_x + 200, hunger_y))

        hunger_ratio = max(0, player.hunger / player.max_hunger)
        hunger_color = COLORS['RED'] if player.hunger < 10 else (COLORS['YELLOW'] if player.hunger < 30 else COLORS['GREEN'])
        self._draw_bar(screen, panel_x + 200, hunger_y + 20, bar_width, bar_height, hunger_ratio, hunger_color)

        # ── Level / XP ────────────────────────────────────────────────────
        level = getattr(player, 'level', 1)
        xp = getattr(player, 'xp', 0)
        xp_needed = level * 100
        xp_ratio = min(1.0, xp / xp_needed)

        level_text = self.font.render(f"⭐ Lv.{level}", True, COLORS['YELLOW'])
        screen.blit(level_text, (panel_x + 15, panel_y + 65))

        xp_label = self.small_font.render(f"XP: {xp}/{xp_needed}", True, COLORS['LIGHT_GRAY'])
        screen.blit(xp_label, (panel_x + 85, panel_y + 68))

        self._draw_bar(screen, panel_x + 85, panel_y + 82, 110, 14, xp_ratio, COLORS['BLUE'])

        # ── Weapon indicator ──────────────────────────────────────────────
        weapon_name = "Mains"
        dmg = player.BARE_HANDS_DAMAGE
        for slot in player.inventory.slots:
            if slot and slot.item.type in ("weapon", "tool"):
                weapon_name = slot.item.name[:12]
                dmg = player.WEAPON_DAMAGE.get(slot.item.name, player.BARE_HANDS_DAMAGE)
                break

        weapon_text = self.small_font.render(f"⚔ {weapon_name} ({dmg})", True, COLORS['ORANGE'])
        screen.blit(weapon_text, (panel_x + 320, panel_y + 35))

        # ── Build mode indicator ──────────────────────────────────────────
        if player.build_mode:
            build_panel_y = panel_y + panel_height + 8
            build_width = 280
            self._draw_panel(screen, panel_x, build_panel_y, build_width, 45)

            mode_text = self.font.render(
                "🏗 CONSTRUCTION", True, COLORS['YELLOW'])
            screen.blit(mode_text, (panel_x + 15, build_panel_y + 12))

            building_text = self.small_font.render(
                f"Objet: {player.selected_building.upper()}", True, COLORS['LIGHT_BLUE'])
            screen.blit(building_text, (panel_x + 15, build_panel_y + 28))

