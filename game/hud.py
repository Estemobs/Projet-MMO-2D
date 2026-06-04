"""
HUD Battle Royale - Grande barre de vie visible
"""

import pygame
import math
from .constants import COLORS, s


class HUD:
    def __init__(self, font):
        self.font = font
        self.time = 0.0

    def update(self, dt):
        self.time += dt

    def draw(self, screen, player, game_instance=None):
        self.time += 0.016
        w, h = screen.get_size()

        bar_w = int(w * 0.30)
        bar_h = s(28)
        x = s(20)
        y = h - bar_h - s(55)

        health_ratio = max(0, player.health / player.max_health)
        if health_ratio < 0.33:
            hc = (220, 50, 50)
        elif health_ratio < 0.66:
            hc = (220, 180, 40)
        else:
            hc = (50, 200, 80)

        big = pygame.font.Font(None, s(28))
        med = pygame.font.Font(None, s(22))

        label = big.render("VIE", True, (220, 230, 250))
        screen.blit(label, (x, y - s(30)))

        val = med.render(f"{int(player.health)} / {player.max_health}", True, (240, 242, 250))
        screen.blit(val, (x + bar_w - val.get_width(), y - s(28)))

        kills_text = med.render(f"Kills: {player.kills}", True, (255, 180, 100))
        screen.blit(kills_text, (x + bar_w + s(20), y - s(28)))

        alive = getattr(game_instance, 'alive_count', 0)
        if game_instance and hasattr(game_instance, 'gameplay_manager'):
            alive = game_instance.gameplay_manager.alive_count
        alive_text = med.render(f"En vie: {alive}", True, (180, 200, 255))
        screen.blit(alive_text, (x + bar_w + s(20), y - s(8)))

        bg = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)
        pygame.draw.rect(bg, (20, 24, 38, 220), (0, 0, bar_w, bar_h), border_radius=8)
        pygame.draw.rect(bg, (50, 60, 85, 150), (0, 0, bar_w, bar_h), 2, border_radius=8)
        screen.blit(bg, (x, y))

        fill = int(bar_w * health_ratio)
        if fill > 0:
            bar = pygame.Surface((fill, bar_h), pygame.SRCALPHA)
            for i in range(bar_h):
                t = i / max(1, bar_h)
                r = min(255, int(hc[0] * (1.1 - t * 0.3)))
                g = min(255, int(hc[1] * (1.1 - t * 0.3)))
                b = min(255, int(hc[2] * (1.1 - t * 0.3)))
                pygame.draw.line(bar, (r, g, b, 240), (0, i), (fill, i))
            screen.blit(bar, (x, y))

        if health_ratio < 0.33:
            pulse = abs(math.sin(self.time * 5)) * 0.5 + 0.5
            warn = pygame.Surface((bar_w + 10, bar_h + 10), pygame.SRCALPHA)
            pygame.draw.rect(warn, (220, 50, 50, int(pulse * 70)), (0, 0, bar_w + 10, bar_h + 10), border_radius=10)
            screen.blit(warn, (x - 5, y - 5))

        weapon_name = player.get_weapon_name()
        dmg = player.get_attack_damage()
        wy = y + bar_h + s(10)
        wf = pygame.font.Font(None, s(22))
        wt = wf.render(f"{weapon_name}  {dmg} DMG", True, (200, 180, 120))
        screen.blit(wt, (x, wy))

        weapon = player.get_weapon_name()
        if weapon != "Mains":
            ammo_count = player.inventory.get_item_count("Munitions")
            at = wf.render(f"Munitions: {ammo_count}", True, (180, 170, 140))
            screen.blit(at, (x, wy + s(22)))
