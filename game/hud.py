"""
HUD moderne - Barre de vie grosse et visible
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

        bar_w = int(w * 0.25)
        bar_h = s(22)
        x = s(16)
        y = h - bar_h - s(50)

        health_ratio = max(0, player.health / player.max_health)
        if health_ratio < 0.33:
            hc = (220, 50, 50)
        elif health_ratio < 0.66:
            hc = (220, 180, 40)
        else:
            hc = (50, 200, 80)

        label_font = pygame.font.Font(None, s(20))
        val_font = pygame.font.Font(None, s(18))

        label = label_font.render("VIE", True, (180, 190, 215))
        screen.blit(label, (x, y - s(18)))

        val = val_font.render(f"{int(player.health)}/{player.max_health}", True, self.WHITE())
        screen.blit(val, (x + bar_w - val.get_width(), y - s(18)))

        bg = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)
        pygame.draw.rect(bg, (20, 24, 38, 200), (0, 0, bar_w, bar_h), border_radius=6)
        pygame.draw.rect(bg, (40, 48, 70, 120), (0, 0, bar_w, bar_h), 1, border_radius=6)
        screen.blit(bg, (x, y))

        fill = int(bar_w * health_ratio)
        if fill > 0:
            bar = pygame.Surface((fill, bar_h), pygame.SRCALPHA)
            for i in range(bar_h):
                t = i / max(1, bar_h)
                r = min(255, int(hc[0] * (1.1 - t * 0.3)))
                g = min(255, int(hc[1] * (1.1 - t * 0.3)))
                b = min(255, int(hc[2] * (1.1 - t * 0.3)))
                pygame.draw.line(bar, (r, g, b, 230), (0, i), (fill, i))
            screen.blit(bar, (x, y))

        if health_ratio < 0.33:
            pulse = abs(math.sin(self.time * 5)) * 0.4 + 0.6
            warn = pygame.Surface((bar_w + 8, bar_h + 8), pygame.SRCALPHA)
            pygame.draw.rect(warn, (220, 50, 50, int(pulse * 60)), (0, 0, bar_w + 8, bar_h + 8), border_radius=8)
            screen.blit(warn, (x - 4, y - 4))

        hunger_ratio = max(0, player.hunger / player.max_hunger)
        hy = y + bar_h + s(8)
        hh = s(14)

        hlabel = label_font.render("FAIM", True, (180, 190, 215))
        screen.blit(hlabel, (x, hy - s(16)))

        hval = val_font.render(f"{int(player.hunger)}", True, self.WHITE())
        screen.blit(hval, (x + bar_w - hval.get_width(), hy - s(16)))

        hbg = pygame.Surface((bar_w, hh), pygame.SRCALPHA)
        pygame.draw.rect(hbg, (20, 24, 38, 180), (0, 0, bar_w, hh), border_radius=4)
        screen.blit(hbg, (x, hy))

        hfill = int(bar_w * hunger_ratio)
        if hfill > 0:
            if hunger_ratio < 0.25:
                hcolor = (220, 60, 40)
            elif hunger_ratio < 0.5:
                hcolor = (220, 160, 40)
            else:
                hcolor = (180, 130, 60)
            hbar = pygame.Surface((hfill, hh), pygame.SRCALPHA)
            pygame.draw.rect(hbar, (*hcolor, 200), (0, 0, hfill, hh), border_radius=4)
            screen.blit(hbar, (x, hy))

        weapon_name = "Mains"
        dmg = player.BARE_HANDS_DAMAGE
        for slot in player.inventory.slots:
            if slot and slot.item.type in ("weapon", "tool"):
                weapon_name = slot.item.name[:16]
                dmg = player.WEAPON_DAMAGE.get(slot.item.name, player.BARE_HANDS_DAMAGE)
                break

        wy = hy + hh + s(10)
        wf = pygame.font.Font(None, s(18))
        wt = wf.render(f"{weapon_name}  {dmg} DMG", True, (200, 170, 100))
        screen.blit(wt, (x, wy))

        level = getattr(player, 'level', 1)
        xp = getattr(player, 'xp', 0)
        xp_needed = level * 100
        xp_ratio = min(1.0, xp / xp_needed) if xp_needed > 0 else 0

        lf = pygame.font.Font(None, s(16))
        screen.blit(lf.render(f"Nv.{level}", True, (140, 160, 220)), (x, wy + s(18)))

        xp_w = int(bar_w * 0.5)
        xp_h = s(6)
        xp_x = x + s(40)
        xp_y = wy + s(20)
        pygame.draw.rect(screen, (20, 24, 38), (xp_x, xp_y, xp_w, xp_h), border_radius=3)
        xp_fill = int(xp_w * xp_ratio)
        if xp_fill > 0:
            pygame.draw.rect(screen, (80, 120, 220), (xp_x, xp_y, xp_fill, xp_h), border_radius=3)

    def WHITE(self):
        return (240, 242, 250)
