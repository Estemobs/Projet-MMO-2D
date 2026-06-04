"""
Menu principal et sous-menus du jeu MMO 2D
Style moderne et épuré
"""

import pygame
import json
import os
import math
import random
import time as _time
from game.sound_manager import get_sound_manager


class Menu:
    _BG_CACHE = None
    _BG_SIZE = None
    _PARTICLES_CACHE = None

    def __init__(self, screen, font):
        self.screen = screen
        self._menu_time = 0.0

        self.WHITE = (240, 242, 250)
        self.BLACK = (12, 14, 20)
        self.GRAY = (120, 130, 155)
        self.DARK_GRAY = (30, 35, 50)
        self.GREEN = (80, 210, 120)
        self.RED = (240, 85, 85)
        self.BLUE = (90, 140, 255)
        self.YELLOW = (255, 215, 110)
        self.ACCENT = (100, 150, 255)
        self.BUTTON_DEFAULT = (35, 42, 65)
        self.BUTTON_HOVER = (50, 60, 95)

        if Menu._PARTICLES_CACHE is None:
            Menu._PARTICLES_CACHE = self._gen_particles()
        self._particles = Menu._PARTICLES_CACHE

        self.sound_manager = get_sound_manager()

        self.current_menu = "main"
        self.selected_button = 0
        self.controls_menu_selected = 0

        self.main_buttons = [
            {"text": "Jouer", "action": "new_game"},
            {"text": "Charger", "action": "load_menu"},
            {"text": "Options", "action": "options"},
            {"text": "Quitter", "action": "quit"}
        ]

        self.save_slots = [None, None, None]
        self.selected_save_slot = 0
        self.load_save_slots_info()

        self.window_scales = [0.5, 0.75, 1.0]
        self.window_scale_labels = ["50%", "75%", "100%"]
        self.current_scale_index = 2
        self.fullscreen = True

        self.controls = {
            "move_up": pygame.K_w, "move_down": pygame.K_s,
            "move_left": pygame.K_a, "move_right": pygame.K_d,
            "harvest": pygame.MOUSEBUTTONDOWN, "build_mode": pygame.K_b,
            "inventory": pygame.K_i, "crafting": pygame.K_c,
            "foundation": pygame.K_1, "wall": pygame.K_2
        }
        self.control_names = {
            "move_up": "Monter", "move_down": "Descendre",
            "move_left": "Gauche", "move_right": "Droite",
            "harvest": "Recolter", "build_mode": "Construire",
            "inventory": "Inventaire", "crafting": "Artisanat",
            "foundation": "Fondation", "wall": "Mur"
        }

        self.load_settings()

    def _W(self):
        return self.screen.get_width()

    def _H(self):
        return self.screen.get_height()

    def _font(self, pct):
        return max(12, int(self._H() * pct / 100))

    def _gen_particles(self):
        rng = random.Random(42)
        pts = []
        for _ in range(25):
            pts.append({
                "x": rng.random(), "y": rng.random(),
                "vx": rng.uniform(-0.008, 0.008),
                "vy": rng.uniform(-0.005, -0.015),
                "size": rng.uniform(1.0, 2.5),
                "alpha": rng.randint(30, 80),
                "phase": rng.uniform(0, math.pi * 2),
            })
        return pts

    # ─── Background ───────────────────────────────────────

    def _draw_bg(self):
        w, h = self._W(), self._H()
        self._menu_time += 0.016

        if Menu._BG_SIZE != (w, h) or Menu._BG_CACHE is None:
            surf = pygame.Surface((w, h))
            c1, c2 = (10, 12, 22), (18, 22, 38)
            for y in range(h):
                t = y / max(1, h - 1)
                r = int(c1[0] + (c2[0] - c1[0]) * t)
                g = int(c1[1] + (c2[1] - c1[1]) * t)
                b = int(c1[2] + (c2[2] - c1[2]) * t)
                pygame.draw.line(surf, (r, g, b), (0, y), (w, y))
            Menu._BG_CACHE = surf
            Menu._BG_SIZE = (w, h)

        self.screen.blit(Menu._BG_CACHE, (0, 0))

        glow = pygame.Surface((w, h), pygame.SRCALPHA)
        pulse = int(abs(math.sin(self._menu_time * 0.4)) * 8) + 12
        pygame.draw.circle(glow, (60, 90, 180, pulse), (w // 2, int(h * 0.25)), int(w * 0.35))
        pygame.draw.circle(glow, (40, 60, 140, pulse // 2), (w // 2, int(h * 0.25)), int(w * 0.5))
        self.screen.blit(glow, (0, 0))

        for p in self._particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["y"] < -0.05:
                p["y"] = 1.05
                p["x"] = random.random()
            if p["x"] < -0.05 or p["x"] > 1.05:
                p["x"] = random.random()
                p["y"] = 1.05
            px = int(p["x"] * w)
            py = int(p["y"] * h)
            a = int(p["alpha"] * (0.5 + 0.5 * math.sin(self._menu_time * 1.5 + p["phase"])))
            sz = p["size"]
            s = pygame.Surface((int(sz * 4), int(sz * 4)), pygame.SRCALPHA)
            pygame.draw.circle(s, (180, 200, 255, a // 3), (int(sz * 2), int(sz * 2)), int(sz * 2))
            pygame.draw.circle(s, (200, 215, 255, a), (int(sz * 2), int(sz * 2)), int(sz))
            self.screen.blit(s, (px - int(sz * 2), py - int(sz * 2)))

    # ─── Button ───────────────────────────────────────────

    def _draw_button(self, text, cx, cy, w, h, selected=False, font_size_pct=2.5):
        x = cx - w // 2
        y = cy - h // 2
        rect = pygame.Rect(x, y, w, h)
        br = 10

        if selected:
            glow = pygame.Surface((w + 24, h + 24), pygame.SRCALPHA)
            gp = int(abs(math.sin(self._menu_time * 2.5)) * 20) + 30
            pygame.draw.rect(glow, (70, 120, 220, gp), (0, 0, w + 24, h + 24), border_radius=br + 8)
            self.screen.blit(glow, (x - 12, y - 12))

        bg = self.BUTTON_HOVER if selected else self.BUTTON_DEFAULT
        btn = pygame.Surface((w, h), pygame.SRCALPHA)
        for i in range(h):
            t = i / max(1, h - 1)
            r = int(bg[0] * (1 - t * 0.15))
            g = int(bg[1] * (1 - t * 0.15))
            b = int(bg[2] + t * 5)
            pygame.draw.line(btn, (r, g, b, 230), (0, i), (w, i))
        self.screen.blit(btn, (x, y))

        bc = self.ACCENT if selected else (55, 65, 100)
        ba = 200 if selected else 120
        bs = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(bs, (*bc, ba), (0, 0, w, h), 1, border_radius=br)
        self.screen.blit(bs, (x, y))

        font = pygame.font.Font(None, self._font(font_size_pct))
        tc = (255, 255, 255) if selected else (175, 185, 210)
        ts = font.render(text, True, tc)
        tr = ts.get_rect(center=(cx, cy))
        if selected:
            sh = font.render(text, True, (0, 0, 0))
            self.screen.blit(sh, (tr.x + 1, tr.y + 2))
        self.screen.blit(ts, tr)

        if selected:
            arrow_x = x - 20
            ap = int(abs(math.sin(self._menu_time * 3)) * 4) + 3
            pygame.draw.polygon(self.screen, self.ACCENT, [
                (arrow_x + ap, cy), (arrow_x, cy - 5), (arrow_x, cy + 5)
            ])

        return rect

    def _draw_text(self, text, cx, cy, size_pct, color, alpha=255):
        font = pygame.font.Font(None, self._font(size_pct))
        ts = font.render(text, True, color)
        ts.set_alpha(alpha)
        self.screen.blit(ts, ts.get_rect(center=(cx, cy)))

    # ─── Main Menu ───────────────────────────────────────

    def draw_main_menu(self):
        self._draw_bg()
        w, h = self._W(), self._H()

        self._draw_showcase(w, h)

        title_y = int(h * 0.10)
        self._draw_text("MMO", w // 2, title_y, 9, (230, 238, 255))
        self._draw_text("2D", w // 2, title_y + int(h * 0.085), 5, self.ACCENT, 200)

        line_y = title_y + int(h * 0.14)
        lw = int(w * 0.08)
        ls = pygame.Surface((lw * 2 + 30, 1), pygame.SRCALPHA)
        la = int(60 + math.sin(self._menu_time) * 20)
        pygame.draw.line(ls, (*self.ACCENT, la), (0, 0), (lw, 0))
        pygame.draw.line(ls, (*self.ACCENT, la), (lw + 30, 0), (lw * 2 + 30, 0))
        self.screen.blit(ls, (w // 2 - lw - 15, line_y))

        self._draw_text("Survie \u2022 Exploration \u2022 Construction", w // 2, line_y + 18, 2.0, (130, 145, 180), int(160 + math.sin(self._menu_time * 0.7) * 40))

        btn_w = int(w * 0.22)
        btn_h = int(h * 0.055)
        start_y = int(h * 0.42)
        spacing = int(h * 0.085)

        for i, button in enumerate(self.main_buttons):
            self._draw_button(button["text"], w // 2, start_y + i * spacing, btn_w, btn_h, i == self.selected_button, 2.4)

        self._draw_character(w, h)

        self._draw_items_row(w, h)

        try:
            from systems.version import get_current_version
            vf = pygame.font.Font(None, self._font(1.6))
            vs = vf.render(f"v{get_current_version()}", True, (80, 90, 120))
            self.screen.blit(vs, (15, h - 25))
        except Exception:
            pass

        ta = int(100 + math.sin(self._menu_time * 0.5) * 40)
        self._draw_text("ENTREE pour commencer", w // 2, int(h * 0.93), 1.8, (100, 115, 155), ta)

    def _draw_showcase(self, w, h):
        try:
            from game.sprite_manager import get_sprite_manager
            sm = get_sprite_manager()
        except Exception:
            return

        items = [
            ("iron_sword", 0.08, 0.38, 32),
            ("diamond_pickaxe", 0.91, 0.34, 28),
            ("apple", 0.10, 0.72, 22),
            ("iron_armor", 0.89, 0.58, 28),
            ("diamond", 0.93, 0.75, 20),
            ("wood", 0.07, 0.55, 22),
        ]

        for name, xr, yr, sz in items:
            sprite = sm.get_item_sprite(name)
            if not sprite:
                continue
            fy = math.sin(self._menu_time * 0.8 + xr * 10) * 4
            fx = math.sin(self._menu_time * 0.3 + yr * 8) * 3
            ix, iy = int(xr * w + fx), int(yr * h + fy)
            s = pygame.transform.smoothscale(sprite, (sz, sz))
            a = int(50 + math.sin(self._menu_time + xr * 5) * 25)
            ha = pygame.Surface((sz + 8, sz + 8), pygame.SRCALPHA)
            pygame.draw.circle(ha, (70, 110, 200, a), (sz // 2 + 4, sz // 2 + 4), sz // 2 + 4)
            self.screen.blit(ha, (ix - 4, iy - 4))
            self.screen.blit(s, (ix, iy))

    def _draw_character(self, w, h):
        try:
            from game.sprite_manager import get_sprite_manager
            sm = get_sprite_manager()
        except Exception:
            return

        cycle = int(self._menu_time * 3) % 3
        names = ["player", "player_walk1", "player_walk2"]
        sprite = sm.get_entity_sprite(names[cycle]) or sm.get_entity_sprite("player")
        if not sprite:
            return

        pw = int(h * 0.18)
        ph = int(pw * 48 / 32)
        s = pygame.transform.smoothscale(sprite, (pw, ph))
        fy = math.sin(self._menu_time * 1.2) * 4
        px = int(w * 0.72)
        py = int(h * 0.40 + fy)

        sh = pygame.Surface((int(pw * 0.7), 6), pygame.SRCALPHA)
        pygame.draw.ellipse(sh, (0, 0, 0, 40), (0, 0, int(pw * 0.7), 6))
        self.screen.blit(sh, (px + pw // 2 - int(pw * 0.35), py + ph - 4))

        halo = pygame.Surface((pw + 20, ph + 20), pygame.SRCALPHA)
        ha = int(20 + math.sin(self._menu_time * 1.5) * 10)
        pygame.draw.ellipse(halo, (60, 100, 200, ha), (0, 0, pw + 20, ph + 20))
        self.screen.blit(halo, (px - 10, py - 10))

        self.screen.blit(s, (px, py))

    def _draw_items_row(self, w, h):
        try:
            from game.sprite_manager import get_sprite_manager
            sm = get_sprite_manager()
        except Exception:
            return

        items = ["wooden_sword", "iron_sword", "diamond_sword", "apple", "bread", "meat"]
        row_y = int(h * 0.85)
        total_w = len(items) * 36
        start_x = (w - total_w) // 2

        bg = pygame.Surface((total_w + 20, 40), pygame.SRCALPHA)
        pygame.draw.rect(bg, (20, 25, 40, 100), (0, 0, total_w + 20, 40), border_radius=8)
        self.screen.blit(bg, (start_x - 10, row_y - 4))

        for i, name in enumerate(items):
            sprite = sm.get_item_sprite(name)
            if not sprite:
                continue
            s = pygame.transform.smoothscale(sprite, (28, 28))
            ix = start_x + i * 36
            self.screen.blit(s, (ix, row_y))

    # ─── Options ─────────────────────────────────────────

    def draw_options_menu(self):
        self._draw_bg()
        w, h = self._W(), self._H()

        self._draw_text("Options", w // 2, int(h * 0.08), 5, self.WHITE)

        pw = int(w * 0.45)
        ph = int(h * 0.55)
        px = (w - pw) // 2
        py = int(h * 0.16)

        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.rect(panel, (20, 24, 40, 200), (0, 0, pw, ph), border_radius=14)
        pygame.draw.rect(panel, (50, 60, 90, 150), (0, 0, pw, ph), 1, border_radius=14)
        self.screen.blit(panel, (px, py))

        cx = px + pw // 2
        row_h = int(ph * 0.13)
        opt = pygame.font.Font(None, self._font(2.6))

        y = py + int(ph * 0.15)
        self.screen.blit(opt.render(f"Taille: {self.window_scale_labels[self.current_scale_index]}", True, self.WHITE), (cx - 100, y))
        bh = int(row_h * 0.6)
        self._draw_button("<", cx - 120, y + int(row_h * 0.45), 40, bh, self.selected_button == 0, 2.2)
        self._draw_button(">", cx + 120, y + int(row_h * 0.45), 40, bh, self.selected_button == 1, 2.2)

        y += row_h
        self.screen.blit(opt.render(f"Plein ecran: {'Oui' if self.fullscreen else 'Non'}", True, self.WHITE), (cx - 100, y))
        self._draw_button("Basculer", cx, y + int(row_h * 0.5), 120, bh, self.selected_button == 2, 2.2)

        y += row_h
        self.screen.blit(opt.render("Controles", True, self.WHITE), (cx - 100, y))
        self._draw_button("Modifier", cx, y + int(row_h * 0.5), 120, bh, self.selected_button == 3, 2.2)

        self._draw_button("Retour", cx, py + ph - int(ph * 0.12), 130, bh, self.selected_button == 4, 2.2)

    # ─── Controls ─────────────────────────────────────────

    def draw_controls_menu(self):
        self._draw_bg()
        w, h = self._W(), self._H()

        self._draw_text("Controles", w // 2, int(h * 0.06), 4.5, self.WHITE)
        self._draw_text("Cliquez pour modifier", w // 2, int(h * 0.11), 2.0, self.GRAY)

        modifiable = [(k, v) for k, v in self.control_names.items() if k != "harvest"]

        pw = int(w * 0.55)
        ph = int(h * 0.65)
        ppx = (w - pw) // 2
        ppy = int(h * 0.15)

        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.rect(panel, (20, 24, 40, 200), (0, 0, pw, ph), border_radius=14)
        pygame.draw.rect(panel, (50, 60, 90, 150), (0, 0, pw, ph), 1, border_radius=14)
        self.screen.blit(panel, (ppx, ppy))

        row_h = int(ph / (len(modifiable) + 1.5))
        opt = pygame.font.Font(None, self._font(2.2))
        key_f = pygame.font.Font(None, self._font(2.0))

        for i, (key, name) in enumerate(modifiable):
            y = ppy + int(ph * 0.08) + i * row_h
            is_sel = (i == self.controls_menu_selected)

            if is_sel:
                sb = pygame.Surface((pw - 16, row_h - 4), pygame.SRCALPHA)
                pulse = int(abs(math.sin(self._menu_time * 2)) * 15) + 35
                pygame.draw.rect(sb, (70, 100, 180, pulse), (0, 0, pw - 16, row_h - 4), border_radius=6)
                self.screen.blit(sb, (ppx + 8, y))

            self.screen.blit(opt.render(name, True, (230, 235, 250) if is_sel else (150, 160, 185)), (ppx + 18, y + row_h // 4))

            kn = pygame.key.name(self.controls[key]).upper()
            kc = (255, 210, 70) if is_sel else (110, 125, 165)
            ks = key_f.render(kn, True, kc)
            kkw = ks.get_width() + 20
            kkh = row_h - 10
            kkx = ppx + pw - kkw - 18
            kky = y + 5
            kb = pygame.Surface((kkw, kkh), pygame.SRCALPHA)
            pygame.draw.rect(kb, (35, 45, 70, 160), (0, 0, kkw, kkh), border_radius=5)
            pygame.draw.rect(kb, (*kc, 80), (0, 0, kkw, kkh), 1, border_radius=5)
            self.screen.blit(kb, (kkx, kky))
            self.screen.blit(ks, (kkx + 10, kky + kkh // 2 - ks.get_height() // 2))

        back_y = ppy + ph - int(row_h * 0.8)
        self._draw_button("Retour", w // 2, back_y, 160, int(row_h * 0.7), self.controls_menu_selected >= len(modifiable), 2.2)

    # ─── Save / Load ──────────────────────────────────────

    def draw_save_load_menu(self, menu_type):
        self._draw_bg()
        w, h = self._W(), self._H()

        title = "Charger une partie" if menu_type == "load" else "Sauvegarder"
        self._draw_text(title, w // 2, int(h * 0.07), 4.5, self.WHITE)

        slot_w = int(w * 0.5)
        slot_h = int(h * 0.12)
        start_y = int(h * 0.17)
        spacing = int(h * 0.16)

        opt = pygame.font.Font(None, self._font(2.2))
        sml = pygame.font.Font(None, self._font(1.8))

        for i in range(3):
            x = (w - slot_w) // 2
            y = start_y + i * spacing
            sel = (i == self.selected_save_slot)

            bg = pygame.Surface((slot_w, slot_h), pygame.SRCALPHA)
            if sel:
                for row in range(slot_h):
                    t = row / max(1, slot_h - 1)
                    r, g, b = int(35 + t * 10), int(45 + t * 15), int(75 + t * 25)
                    pygame.draw.line(bg, (r, g, b, 210), (0, row), (slot_w, row))
            else:
                for row in range(slot_h):
                    t = row / max(1, slot_h - 1)
                    r, g, b = int(20 + t * 5), int(24 + t * 6), int(38 + t * 8)
                    pygame.draw.line(bg, (r, g, b, 200), (0, row), (slot_w, row))
            self.screen.blit(bg, (x, y))

            bc = self.ACCENT if sel else (45, 55, 80)
            bs = pygame.Surface((slot_w, slot_h), pygame.SRCALPHA)
            pygame.draw.rect(bs, (*bc, 180 if sel else 100), (0, 0, slot_w, slot_h), 1, border_radius=10)
            self.screen.blit(bs, (x, y))

            self.screen.blit(opt.render(f"Slot {i + 1}", True, (230, 235, 250) if sel else (140, 150, 175)), (x + 18, y + 10))

            if self.save_slots[i] and self.save_slots[i]["exists"]:
                info = self.save_slots[i]
                dt = self.format_date(info["timestamp"])
                self.screen.blit(sml.render(dt, True, (180, 190, 215)), (x + 18, y + int(slot_h * 0.35)))
                self.screen.blit(sml.render(info["playtime"], True, (180, 190, 215)), (x + 18, y + int(slot_h * 0.55)))
                self.screen.blit(sml.render(f"{info['player_health']}/100", True, self.GREEN), (x + int(slot_w * 0.5), y + int(slot_h * 0.35)))
                act = "Entree: Charger" if menu_type == "load" else "Entree: Ecraser"
                self.screen.blit(sml.render(act, True, self.YELLOW if sel else (130, 140, 170)), (x + int(slot_w * 0.5), y + int(slot_h * 0.55)))
            else:
                self.screen.blit(opt.render("Vide", True, (80, 90, 115)), (x + 18, y + int(slot_h * 0.4)))

        self._draw_button("Retour", w // 2, start_y + 3 * spacing + int(h * 0.02), 120, int(h * 0.05), self.selected_save_slot == 3, 2.2)

    # ─── Events ───────────────────────────────────────────

    def handle_event(self, event):
        if self.current_menu == "main":
            return self.handle_main_menu_event(event)
        elif self.current_menu == "options":
            return self.handle_options_event(event)
        elif self.current_menu == "controls":
            return self.handle_controls_event(event)
        elif self.current_menu == "load_menu":
            return self.handle_save_load_event(event, "load")
        elif self.current_menu == "save_menu":
            return self.handle_save_load_event(event, "save")
        return None

    def handle_main_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_button = (self.selected_button - 1) % len(self.main_buttons)
                self.sound_manager.play('menu_click')
            elif event.key == pygame.K_DOWN:
                self.selected_button = (self.selected_button + 1) % len(self.main_buttons)
                self.sound_manager.play('menu_click')
            elif event.key == pygame.K_RETURN:
                self.sound_manager.play('menu_select')
                return self.main_buttons[self.selected_button]["action"]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            w, h = self._W(), self._H()
            bw = int(w * 0.22)
            bh = int(h * 0.055)
            sy = int(h * 0.42)
            sp = int(h * 0.085)
            for i, btn in enumerate(self.main_buttons):
                cx, cy = w // 2, sy + i * sp
                r = pygame.Rect(cx - bw // 2, cy - bh // 2, bw, bh)
                if r.collidepoint((mx, my)):
                    self.sound_manager.play('menu_click')
                    return btn["action"]
        return None

    def handle_options_event(self, event):
        w, h = self._W(), self._H()
        pw = int(w * 0.45)
        ph = int(h * 0.55)
        px = (w - pw) // 2
        py = int(h * 0.16)
        cx = px + pw // 2
        row_h = int(ph * 0.13)
        bh = int(row_h * 0.6)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_menu = "main"
                self.selected_button = 0
                self.save_settings()
            elif event.key == pygame.K_UP:
                self.selected_button = max(0, self.selected_button - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_button = min(4, self.selected_button + 1)
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT) and self.selected_button <= 1:
                d = 1 if event.key == pygame.K_RIGHT else -1
                self.current_scale_index = (self.current_scale_index + d) % len(self.window_scales)
                self.save_settings()
                return "toggle_fullscreen"
            elif event.key == pygame.K_RETURN:
                if self.selected_button == 0:
                    self.current_scale_index = (self.current_scale_index - 1) % len(self.window_scales)
                    self.save_settings(); return "toggle_fullscreen"
                elif self.selected_button == 1:
                    self.current_scale_index = (self.current_scale_index + 1) % len(self.window_scales)
                    self.save_settings(); return "toggle_fullscreen"
                elif self.selected_button == 2:
                    self.fullscreen = not self.fullscreen
                    self.save_settings(); return "toggle_fullscreen"
                elif self.selected_button == 3:
                    self.current_menu = "controls"; self.controls_menu_selected = 0
                elif self.selected_button == 4:
                    self.current_menu = "main"; self.selected_button = 0; self.save_settings()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mp = event.pos
            y0 = py + int(ph * 0.15)
            if pygame.Rect(cx - 140, y0 + int(row_h * 0.2), 40, bh).collidepoint(mp):
                self.current_scale_index = (self.current_scale_index - 1) % len(self.window_scales)
                self.save_settings(); return "toggle_fullscreen"
            if pygame.Rect(cx + 80, y0 + int(row_h * 0.2), 40, bh).collidepoint(mp):
                self.current_scale_index = (self.current_scale_index + 1) % len(self.window_scales)
                self.save_settings(); return "toggle_fullscreen"
            y1 = y0 + row_h
            if pygame.Rect(cx - 60, y1 + int(row_h * 0.2), 120, bh).collidepoint(mp):
                self.fullscreen = not self.fullscreen; self.save_settings(); return "toggle_fullscreen"
            y2 = y1 + row_h
            if pygame.Rect(cx - 60, y2 + int(row_h * 0.2), 120, bh).collidepoint(mp):
                self.current_menu = "controls"; self.controls_menu_selected = 0
            back_y = py + ph - int(ph * 0.12)
            if pygame.Rect(cx - 65, back_y - bh // 2, 130, bh).collidepoint(mp):
                self.current_menu = "main"; self.selected_button = 0; self.save_settings()
        return None

    def handle_controls_event(self, event):
        modifiable = [k for k in self.control_names.keys() if k != "harvest"]
        mx = len(modifiable)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_menu = "options"; self.selected_button = 3; self.save_settings()
            elif event.key == pygame.K_UP:
                self.controls_menu_selected = max(0, self.controls_menu_selected - 1)
            elif event.key == pygame.K_DOWN:
                self.controls_menu_selected = min(mx, self.controls_menu_selected + 1)
            elif event.key == pygame.K_RETURN:
                if self.controls_menu_selected < mx:
                    return f"remap_control_{modifiable[self.controls_menu_selected]}"
                else:
                    self.current_menu = "options"; self.selected_button = 3; self.save_settings()
        return None

    def handle_save_load_event(self, event, menu_type):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_menu = "main"; self.selected_save_slot = 0
            elif event.key == pygame.K_UP:
                self.selected_save_slot = max(0, self.selected_save_slot - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_save_slot = min(3, self.selected_save_slot + 1)
            elif event.key == pygame.K_DELETE and menu_type == "load":
                if self.selected_save_slot < 3 and self.save_slots[self.selected_save_slot] and self.save_slots[self.selected_save_slot]["exists"]:
                    return f"delete_slot_{self.selected_save_slot}"
            elif event.key == pygame.K_RETURN:
                if self.selected_save_slot == 3:
                    self.current_menu = "main"; self.selected_save_slot = 0
                else:
                    if menu_type == "load":
                        if self.save_slots[self.selected_save_slot] and self.save_slots[self.selected_save_slot]["exists"]:
                            return f"load_slot_{self.selected_save_slot}"
                    else:
                        return f"save_slot_{self.selected_save_slot}"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            w, h = self._W(), self._H()
            sw = int(w * 0.5)
            sh = int(h * 0.12)
            sy = int(h * 0.17)
            sp = int(h * 0.16)
            for i in range(3):
                x = (w - sw) // 2
                y = sy + i * sp
                if pygame.Rect(x, y, sw, sh).collidepoint((mx, my)):
                    self.selected_save_slot = i
                    if menu_type == "load" and self.save_slots[i] and self.save_slots[i]["exists"]:
                        return f"load_slot_{i}"
                    elif menu_type == "save":
                        return f"save_slot_{i}"
        return None

    # ─── Utils ────────────────────────────────────────────

    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    s = json.load(f)
                    if "scale_index" in s:
                        self.current_scale_index = s["scale_index"]
                    elif "resolution" in s:
                        old = s["resolution"]
                        self.current_scale_index = 0 if old <= 1 else (1 if old <= 3 else 2)
                    self.fullscreen = s.get("fullscreen", True)
                    self.controls.update(s.get("controls", {}))
        except Exception:
            pass

    def save_settings(self):
        try:
            with open("settings.json", "w") as f:
                json.dump({
                    "scale_index": self.current_scale_index,
                    "fullscreen": self.fullscreen,
                    "controls": self.controls
                }, f, indent=4)
        except Exception:
            pass

    def load_save_slots_info(self):
        if os.getenv('FLATPAK_ID') == 'io.github.Estemobs.ProjetMMO2D':
            sd = os.path.expanduser('~/.var/app/io.github.Estemobs.ProjetMMO2D/data/saves')
        else:
            sd = os.path.expanduser('~/ProjetMMO2D_saves')
        for i in range(3):
            sf = os.path.join(sd, f"save_slot_{i}.json")
            if os.path.exists(sf):
                try:
                    with open(sf, "r") as f:
                        d = json.load(f)
                    self.save_slots[i] = {
                        "timestamp": d.get("timestamp", ""),
                        "playtime": d.get("playtime", "00:00:00"),
                        "level_name": d.get("level_name", "Monde"),
                        "player_health": d.get("player", {}).get("health", 100),
                        "exists": True
                    }
                except Exception:
                    self.save_slots[i] = None
            else:
                self.save_slots[i] = None

    def format_date(self, ts):
        try:
            from datetime import datetime
            return datetime.fromisoformat(ts).strftime("%d/%m/%Y %H:%M")
        except Exception:
            return ts

    def draw(self):
        if self.current_menu == "main":
            self.draw_main_menu()
        elif self.current_menu == "options":
            self.draw_options_menu()
        elif self.current_menu == "controls":
            self.draw_controls_menu()
        elif self.current_menu == "load_menu":
            self.draw_save_load_menu("load")
        elif self.current_menu == "save_menu":
            self.draw_save_load_menu("save")
        pygame.display.flip()

    def get_resolution(self):
        info = pygame.display.Info()
        scale = self.window_scales[self.current_scale_index]
        return (int(info.current_w * scale), int(info.current_h * scale))

    def is_fullscreen(self):
        return self.fullscreen

    def refresh_save_slots(self):
        self.load_save_slots_info()

    def get_save_slot_info(self, n):
        return self.save_slots[n] if 0 <= n <= 2 else None

    def delete_save_slot(self, slot_number):
        if os.getenv('FLATPAK_ID') == 'io.github.Estemobs.ProjetMMO2D':
            sd = os.path.expanduser('~/.var/app/io.github.Estemobs.ProjetMMO2D/data/saves')
        else:
            sd = os.path.expanduser('~/ProjetMMO2D_saves')
        try:
            sf = os.path.join(sd, f"save_slot_{slot_number}.json")
            if os.path.exists(sf):
                os.remove(sf)
                self.save_slots[slot_number] = None
                return True
        except Exception:
            pass
        return False
