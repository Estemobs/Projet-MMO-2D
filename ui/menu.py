"""
Menu principal - Battle Royale
"""

import pygame
import json
import os
import math
import random
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
            {"text": "Options", "action": "options"},
            {"text": "Quitter", "action": "quit"}
        ]

        self.window_scales = [0.5, 0.75, 1.0]
        self.window_scale_labels = ["50%", "75%", "100%"]
        self.current_scale_index = 2
        self.fullscreen = True

        self.controls = {
            "move_up": pygame.K_w, "move_down": pygame.K_s,
            "move_left": pygame.K_a, "move_right": pygame.K_d,
            "inventory": pygame.K_i,
        }
        self.control_names = {
            "move_up": "Monter", "move_down": "Descendre",
            "move_left": "Gauche", "move_right": "Droite",
            "inventory": "Inventaire",
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
        for _ in range(20):
            pts.append({
                "x": rng.random(), "y": rng.random(),
                "vx": rng.uniform(-0.005, 0.005),
                "vy": rng.uniform(-0.003, -0.01),
                "size": rng.uniform(1.0, 2.0),
                "alpha": rng.randint(25, 60),
                "phase": rng.uniform(0, math.pi * 2),
            })
        return pts

    def _draw_bg(self):
        w, h = self._W(), self._H()
        self._menu_time += 0.016

        if Menu._BG_SIZE != (w, h) or Menu._BG_CACHE is None:
            surf = pygame.Surface((w, h))
            c1, c2 = (10, 12, 22), (16, 20, 35)
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
        pulse = int(abs(math.sin(self._menu_time * 0.4)) * 6) + 10
        pygame.draw.circle(glow, (50, 80, 160, pulse), (w // 2, int(h * 0.3)), int(w * 0.3))
        self.screen.blit(glow, (0, 0))

        for p in self._particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["y"] < -0.05:
                p["y"] = 1.05
                p["x"] = random.random()
            px = int(p["x"] * w)
            py = int(p["y"] * h)
            a = int(p["alpha"] * (0.5 + 0.5 * math.sin(self._menu_time * 1.5 + p["phase"])))
            sz = p["size"]
            s = pygame.Surface((int(sz * 4), int(sz * 4)), pygame.SRCALPHA)
            pygame.draw.circle(s, (160, 180, 240, a // 3), (int(sz * 2), int(sz * 2)), int(sz * 2))
            pygame.draw.circle(s, (180, 200, 255, a), (int(sz * 2), int(sz * 2)), int(sz))
            self.screen.blit(s, (px - int(sz * 2), py - int(sz * 2)))

    def _draw_button(self, text, cx, cy, w, h, selected=False, font_size_pct=2.5):
        x = cx - w // 2
        y = cy - h // 2
        rect = pygame.Rect(x, y, w, h)
        br = 10

        if selected:
            glow = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)
            gp = int(abs(math.sin(self._menu_time * 2.5)) * 15) + 25
            pygame.draw.rect(glow, (60, 100, 200, gp), (0, 0, w + 20, h + 20), border_radius=br + 6)
            self.screen.blit(glow, (x - 10, y - 10))

        bg = self.BUTTON_HOVER if selected else self.BUTTON_DEFAULT
        btn = pygame.Surface((w, h), pygame.SRCALPHA)
        for i in range(h):
            t = i / max(1, h - 1)
            r = int(bg[0] * (1 - t * 0.12))
            g = int(bg[1] * (1 - t * 0.12))
            b = int(bg[2] + t * 3)
            pygame.draw.line(btn, (r, g, b, 220), (0, i), (w, i))
        self.screen.blit(btn, (x, y))

        bc = self.ACCENT if selected else (50, 58, 80)
        ba = 180 if selected else 100
        bs = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(bs, (*bc, ba), (0, 0, w, h), 1, border_radius=br)
        self.screen.blit(bs, (x, y))

        font = pygame.font.Font(None, self._font(font_size_pct))
        tc = (255, 255, 255) if selected else (165, 175, 200)
        ts = font.render(text, True, tc)
        tr = ts.get_rect(center=(cx, cy))
        if selected:
            sh = font.render(text, True, (0, 0, 0))
            self.screen.blit(sh, (tr.x + 1, tr.y + 2))
        self.screen.blit(ts, tr)

        if selected:
            ax = x - 18
            ap = int(abs(math.sin(self._menu_time * 3)) * 3) + 2
            pygame.draw.polygon(self.screen, self.ACCENT, [
                (ax + ap, cy), (ax, cy - 5), (ax, cy + 5)
            ])

        return rect

    def _draw_text(self, text, cx, cy, size_pct, color, alpha=255):
        font = pygame.font.Font(None, self._font(size_pct))
        ts = font.render(text, True, color)
        ts.set_alpha(alpha)
        self.screen.blit(ts, ts.get_rect(center=(cx, cy)))

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
        pw = int(h * 0.20)
        ph = int(pw * 48 / 32)
        s = pygame.transform.smoothscale(sprite, (pw, ph))
        fy = math.sin(self._menu_time * 1.2) * 3
        px = int(w * 0.72)
        py = int(h * 0.38 + fy)
        sh = pygame.Surface((int(pw * 0.6), 5), pygame.SRCALPHA)
        pygame.draw.ellipse(sh, (0, 0, 0, 35), (0, 0, int(pw * 0.6), 5))
        self.screen.blit(sh, (px + pw // 2 - int(pw * 0.3), py + ph - 3))
        halo = pygame.Surface((pw + 16, ph + 16), pygame.SRCALPHA)
        ha = int(18 + math.sin(self._menu_time * 1.5) * 8)
        pygame.draw.ellipse(halo, (50, 90, 180, ha), (0, 0, pw + 16, ph + 16))
        self.screen.blit(halo, (px - 8, py - 8))
        self.screen.blit(s, (px, py))

    def draw_main_menu(self):
        self._draw_bg()
        w, h = self._W(), self._H()

        title_y = int(h * 0.10)
        self._draw_text("BATTLE", w // 2, title_y, 10, (230, 238, 255))
        self._draw_text("ROYALE", w // 2, title_y + int(h * 0.09), 5.5, self.ACCENT, 200)

        line_y = title_y + int(h * 0.15)
        lw = int(w * 0.06)
        ls = pygame.Surface((lw * 2 + 30, 1), pygame.SRCALPHA)
        la = int(50 + math.sin(self._menu_time) * 20)
        pygame.draw.line(ls, (*self.ACCENT, la), (0, 0), (lw, 0))
        pygame.draw.line(ls, (*self.ACCENT, la), (lw + 30, 0), (lw * 2 + 30, 0))
        self.screen.blit(ls, (w // 2 - lw - 15, line_y))

        self._draw_text("Dernier en vie", w // 2, line_y + 18, 2.2, (130, 145, 180), int(160 + math.sin(self._menu_time * 0.7) * 40))

        btn_w = int(w * 0.20)
        btn_h = int(h * 0.055)
        start_y = int(h * 0.44)
        spacing = int(h * 0.085)

        for i, button in enumerate(self.main_buttons):
            self._draw_button(button["text"], w // 2, start_y + i * spacing, btn_w, btn_h, i == self.selected_button, 2.4)

        self._draw_character(w, h)

        try:
            from systems.version import get_current_version
            vf = pygame.font.Font(None, self._font(1.6))
            vs = vf.render(f"v{get_current_version()}", True, (70, 80, 110))
            self.screen.blit(vs, (15, h - 25))
        except Exception:
            pass

        ta = int(90 + math.sin(self._menu_time * 0.5) * 35)
        self._draw_text("ENTREE pour commencer", w // 2, int(h * 0.93), 1.8, (90, 100, 140), ta)

    def draw_options_menu(self):
        self._draw_bg()
        w, h = self._W(), self._H()
        self._draw_text("Options", w // 2, int(h * 0.08), 5, self.WHITE)

        pw = int(w * 0.45)
        ph = int(h * 0.45)
        px = (w - pw) // 2
        py = int(h * 0.16)

        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.rect(panel, (20, 24, 40, 200), (0, 0, pw, ph), border_radius=14)
        pygame.draw.rect(panel, (50, 60, 90, 120), (0, 0, pw, ph), 1, border_radius=14)
        self.screen.blit(panel, (px, py))

        cx = px + pw // 2
        row_h = int(ph * 0.18)
        opt = pygame.font.Font(None, self._font(2.4))
        bh = int(row_h * 0.55)

        y = py + int(ph * 0.15)
        self.screen.blit(opt.render(f"Taille: {self.window_scale_labels[self.current_scale_index]}", True, self.WHITE), (cx - 90, y))
        self._draw_button("<", cx - 110, y + int(row_h * 0.45), 36, bh, self.selected_button == 0, 2.0)
        self._draw_button(">", cx + 110, y + int(row_h * 0.45), 36, bh, self.selected_button == 1, 2.0)

        y += row_h
        self.screen.blit(opt.render(f"Plein ecran: {'Oui' if self.fullscreen else 'Non'}", True, self.WHITE), (cx - 90, y))
        self._draw_button("Basculer", cx, y + int(row_h * 0.45), 110, bh, self.selected_button == 2, 2.0)

        y += row_h
        self.screen.blit(opt.render("Controles", True, self.WHITE), (cx - 90, y))
        self._draw_button("Modifier", cx, y + int(row_h * 0.45), 110, bh, self.selected_button == 3, 2.0)

        self._draw_button("Retour", cx, py + ph - int(ph * 0.12), 120, bh, self.selected_button == 4, 2.0)

    def draw_controls_menu(self):
        self._draw_bg()
        w, h = self._W(), self._H()
        self._draw_text("Controles", w // 2, int(h * 0.06), 4.5, self.WHITE)

        modifiable = [(k, v) for k, v in self.control_names.items()]

        pw = int(w * 0.50)
        ph = int(h * 0.55)
        ppx = (w - pw) // 2
        ppy = int(h * 0.14)

        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.rect(panel, (20, 24, 40, 200), (0, 0, pw, ph), border_radius=14)
        pygame.draw.rect(panel, (50, 60, 90, 120), (0, 0, pw, ph), 1, border_radius=14)
        self.screen.blit(panel, (ppx, ppy))

        row_h = int(ph / (len(modifiable) + 1.5))
        opt = pygame.font.Font(None, self._font(2.0))
        key_f = pygame.font.Font(None, self._font(1.8))

        for i, (key, name) in enumerate(modifiable):
            y = ppy + int(ph * 0.10) + i * row_h
            is_sel = (i == self.controls_menu_selected)

            if is_sel:
                sb = pygame.Surface((pw - 14, row_h - 4), pygame.SRCALPHA)
                pulse = int(abs(math.sin(self._menu_time * 2)) * 12) + 30
                pygame.draw.rect(sb, (60, 90, 160, pulse), (0, 0, pw - 14, row_h - 4), border_radius=6)
                self.screen.blit(sb, (ppx + 7, y))

            self.screen.blit(opt.render(name, True, (230, 235, 250) if is_sel else (140, 150, 175)), (ppx + 16, y + row_h // 4))

            kn = pygame.key.name(self.controls[key]).upper()
            kc = (255, 210, 70) if is_sel else (100, 115, 155)
            ks = key_f.render(kn, True, kc)
            kkw = ks.get_width() + 18
            kkh = row_h - 10
            kkx = ppx + pw - kkw - 16
            kky = y + 5
            kb = pygame.Surface((kkw, kkh), pygame.SRCALPHA)
            pygame.draw.rect(kb, (30, 40, 65, 150), (0, 0, kkw, kkh), border_radius=5)
            pygame.draw.rect(kb, (*kc, 70), (0, 0, kkw, kkh), 1, border_radius=5)
            self.screen.blit(kb, (kkx, kky))
            self.screen.blit(ks, (kkx + 9, kky + kkh // 2 - ks.get_height() // 2))

        back_y = ppy + ph - int(row_h * 0.8)
        self._draw_button("Retour", w // 2, back_y, 140, int(row_h * 0.65), self.controls_menu_selected >= len(modifiable), 2.0)

    def handle_event(self, event):
        if self.current_menu == "main":
            return self.handle_main_menu_event(event)
        elif self.current_menu == "options":
            return self.handle_options_event(event)
        elif self.current_menu == "controls":
            return self.handle_controls_event(event)
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
            bw = int(w * 0.20)
            bh = int(h * 0.055)
            sy = int(h * 0.44)
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
        ph = int(h * 0.45)
        px = (w - pw) // 2
        py = int(h * 0.16)
        cx = px + pw // 2
        row_h = int(ph * 0.18)
        bh = int(row_h * 0.55)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_menu = "main"; self.selected_button = 0; self.save_settings()
            elif event.key == pygame.K_UP:
                self.selected_button = max(0, self.selected_button - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_button = min(4, self.selected_button + 1)
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT) and self.selected_button <= 1:
                d = 1 if event.key == pygame.K_RIGHT else -1
                self.current_scale_index = (self.current_scale_index + d) % len(self.window_scales)
                self.save_settings(); return "toggle_fullscreen"
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
            if pygame.Rect(cx - 128, y0 + int(row_h * 0.2), 36, bh).collidepoint(mp):
                self.current_scale_index = (self.current_scale_index - 1) % len(self.window_scales)
                self.save_settings(); return "toggle_fullscreen"
            if pygame.Rect(cx + 74, y0 + int(row_h * 0.2), 36, bh).collidepoint(mp):
                self.current_scale_index = (self.current_scale_index + 1) % len(self.window_scales)
                self.save_settings(); return "toggle_fullscreen"
            y1 = y0 + row_h
            if pygame.Rect(cx - 55, y1 + int(row_h * 0.2), 110, bh).collidepoint(mp):
                self.fullscreen = not self.fullscreen; self.save_settings(); return "toggle_fullscreen"
            y2 = y1 + row_h
            if pygame.Rect(cx - 55, y2 + int(row_h * 0.2), 110, bh).collidepoint(mp):
                self.current_menu = "controls"; self.controls_menu_selected = 0
            back_y = py + ph - int(ph * 0.12)
            if pygame.Rect(cx - 60, back_y - bh // 2, 120, bh).collidepoint(mp):
                self.current_menu = "main"; self.selected_button = 0; self.save_settings()
        return None

    def handle_controls_event(self, event):
        modifiable = list(self.control_names.keys())
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

    def draw(self):
        if self.current_menu == "main":
            self.draw_main_menu()
        elif self.current_menu == "options":
            self.draw_options_menu()
        elif self.current_menu == "controls":
            self.draw_controls_menu()
        pygame.display.flip()

    def get_resolution(self):
        info = pygame.display.Info()
        scale = self.window_scales[self.current_scale_index]
        return (int(info.current_w * scale), int(info.current_h * scale))

    def is_fullscreen(self):
        return self.fullscreen
