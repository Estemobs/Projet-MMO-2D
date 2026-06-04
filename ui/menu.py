"""
Menu principal et sous-menus du jeu MMO 2D
Layout 100% basé sur pourcentages de l'écran - pas de taille fixe
"""

import pygame
import json
import os
import math
import random
import time as _time
from game.sound_manager import get_sound_manager


class Menu:
    DECORATIVE_STARS = None
    AURORA_POINTS = None
    PARTICLES = None
    LANDSCAPE = None

    def __init__(self, screen, font):
        self.screen = screen
        self._menu_time = 0.0

        # Couleurs
        self.WHITE = (245, 247, 255)
        self.BLACK = (8, 12, 24)
        self.GRAY = (132, 144, 170)
        self.DARK_GRAY = (36, 44, 68)
        self.GREEN = (84, 214, 125)
        self.RED = (245, 98, 98)
        self.BLUE = (88, 138, 255)
        self.YELLOW = (255, 221, 129)
        self.BUTTON_DEFAULT = (62, 88, 148)
        self.BUTTON_SELECTED = (112, 165, 255)
        self.BUTTON_BORDER = (189, 214, 255)

        # Étoiles décoratives
        if Menu.DECORATIVE_STARS is None:
            Menu.DECORATIVE_STARS = self._generate_decorative_stars()
        self._background_stars = Menu.DECORATIVE_STARS
        self._background_cache = None
        self._background_cache_size = None

        # Aurore boréale
        if Menu.AURORA_POINTS is None:
            Menu.AURORA_POINTS = self._generate_aurora_points()
        self._aurora_points = Menu.AURORA_POINTS

        # Particules flottantes (lucioles)
        if Menu.PARTICLES is None:
            Menu.PARTICLES = self._generate_particles()
        self._particles = Menu.PARTICLES

        # Silhouette de paysage
        if Menu.LANDSCAPE is None:
            Menu.LANDSCAPE = self._generate_landscape()
        self._landscape = Menu.LANDSCAPE

        self.sound_manager = get_sound_manager()

        # État du menu
        self.current_menu = "main"
        self.selected_button = 0
        self.controls_menu_selected = 0

        # Boutons du menu principal
        self.main_buttons = [
            {"text": "Nouvelle Partie", "action": "new_game"},
            {"text": "Charger Partie", "action": "load_menu"},
            {"text": "Sauvegarder", "action": "save_menu"},
            {"text": "Options", "action": "options"},
            {"text": "Quitter", "action": "quit"}
        ]

        # Système de sauvegarde
        self.save_slots = [None, None, None]
        self.selected_save_slot = 0
        self.load_save_slots_info()

        # Options
        self.window_scales = [0.5, 0.75, 1.0]
        self.window_scale_labels = ["50%", "75%", "100%"]
        self.current_scale_index = 2
        self.fullscreen = True

        # Contrôles
        self.controls = {
            "move_up": pygame.K_w,
            "move_down": pygame.K_s,
            "move_left": pygame.K_a,
            "move_right": pygame.K_d,
            "harvest": pygame.MOUSEBUTTONDOWN,
            "build_mode": pygame.K_b,
            "inventory": pygame.K_i,
            "crafting": pygame.K_c,
            "foundation": pygame.K_1,
            "wall": pygame.K_2
        }
        self.control_names = {
            "move_up": "Monter",
            "move_down": "Descendre",
            "move_left": "Aller a gauche",
            "move_right": "Aller a droite",
            "harvest": "Recolter/Construire",
            "build_mode": "Mode construction",
            "inventory": "Inventaire",
            "crafting": "Artisanat",
            "foundation": "Fondation",
            "wall": "Mur"
        }

        self.load_settings()

    def _W(self):
        return self.screen.get_width()

    def _H(self):
        return self.screen.get_height()

    def _font(self, pct):
        """Taille de police en pourcentage de la hauteur d'écran."""
        return max(12, int(self._H() * pct / 100))

    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    settings = json.load(f)
                    if "scale_index" in settings:
                        self.current_scale_index = settings["scale_index"]
                    elif "resolution" in settings:
                        old_res = settings["resolution"]
                        if old_res <= 1:
                            self.current_scale_index = 0
                        elif old_res <= 3:
                            self.current_scale_index = 1
                        else:
                            self.current_scale_index = 2
                    self.fullscreen = settings.get("fullscreen", True)
                    self.controls.update(settings.get("controls", {}))
        except Exception:
            pass

    def save_settings(self):
        settings = {
            "scale_index": self.current_scale_index,
            "fullscreen": self.fullscreen,
            "controls": self.controls
        }
        try:
            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=4)
        except Exception:
            pass

    # ─── Drawing helpers ─────────────────────────────────────

    def _generate_decorative_stars(self):
        rng = random.Random(42)
        stars = []
        for _ in range(200):
            x_ratio = rng.random()
            y_ratio = rng.random() * 0.75
            radius = rng.choice([1, 1, 1, 1, 2, 2, 3])
            base_shade = rng.randint(160, 255)
            phase = rng.uniform(0, math.pi * 2)
            speed = rng.uniform(0.3, 2.0)
            stars.append((x_ratio, y_ratio, radius, base_shade, phase, speed))
        return stars

    def _generate_aurora_points(self):
        rng = random.Random(77)
        auroras = []
        for _ in range(5):
            base_x = rng.uniform(0.0, 1.0)
            base_y = rng.uniform(0.05, 0.35)
            width = rng.uniform(0.15, 0.4)
            height = rng.uniform(0.08, 0.2)
            color = rng.choice([
                (40, 180, 120), (60, 140, 220), (100, 80, 200),
                (30, 200, 160), (80, 120, 240)
            ])
            speed = rng.uniform(0.2, 0.6)
            phase = rng.uniform(0, math.pi * 2)
            auroras.append((base_x, base_y, width, height, color, speed, phase))
        return auroras

    def _generate_particles(self):
        rng = random.Random(99)
        particles = []
        for _ in range(40):
            x_ratio = rng.random()
            y_ratio = rng.uniform(0.2, 0.85)
            size = rng.uniform(1.5, 4.0)
            speed = rng.uniform(0.15, 0.5)
            phase = rng.uniform(0, math.pi * 2)
            drift = rng.uniform(-0.3, 0.3)
            color_type = rng.choice(["warm", "cool", "white"])
            particles.append((x_ratio, y_ratio, size, speed, phase, drift, color_type))
        return particles

    def _generate_landscape(self):
        rng = random.Random(55)
        points = []
        num_hills = 12
        for i in range(num_hills + 1):
            x_ratio = i / num_hills
            y_base = 0.82 + rng.uniform(-0.04, 0.04)
            points.append((x_ratio, y_base))
        tree_positions = []
        for _ in range(15):
            tx = rng.uniform(0.02, 0.98)
            ty = rng.uniform(0.72, 0.82)
            tsize = rng.uniform(0.03, 0.07)
            tree_positions.append((tx, ty, tsize))
        return {"hills": points, "trees": tree_positions}

    def _draw_gradient_background(self):
        """Fond dégradé étoilé avec aurore boréale."""
        w, h = self._W(), self._H()
        self._menu_time += 0.016

        # Cache du fond dégradé
        if self._background_cache_size != (w, h) or self._background_cache is None:
            self._background_cache = pygame.Surface((w, h))
            top = (4, 6, 20)
            mid = (8, 16, 45)
            bot = (14, 28, 60)
            for y in range(h):
                t = y / max(1, h - 1)
                if t < 0.5:
                    tt = t * 2
                    r = int(top[0] * (1 - tt) + mid[0] * tt)
                    g = int(top[1] * (1 - tt) + mid[1] * tt)
                    b = int(top[2] * (1 - tt) + mid[2] * tt)
                else:
                    tt = (t - 0.5) * 2
                    r = int(mid[0] * (1 - tt) + bot[0] * tt)
                    g = int(mid[1] * (1 - tt) + bot[1] * tt)
                    b = int(mid[2] * (1 - tt) + bot[2] * tt)
                pygame.draw.line(self._background_cache, (r, g, b), (0, y), (w, y))
            self._background_cache_size = (w, h)

        self.screen.blit(self._background_cache, (0, 0))

        # Aurore boréale
        self._draw_aurora(w, h)

        # Étoiles scintillantes
        for x_ratio, y_ratio, radius, base_shade, phase, speed in self._background_stars:
            x = int(x_ratio * w)
            y = int(y_ratio * h)
            twinkle = math.sin(self._menu_time * speed + phase) * 0.5 + 0.5
            shade = int(base_shade * (0.3 + 0.7 * twinkle))
            alpha = int(160 + 95 * twinkle)
            if radius <= 1:
                star_surf = pygame.Surface((2, 2), pygame.SRCALPHA)
                star_surf.fill((shade, shade, shade, alpha))
                self.screen.blit(star_surf, (x, y))
            else:
                size = radius * 5
                star_surf = pygame.Surface((size, size), pygame.SRCALPHA)
                cx, cy = size // 2, size // 2
                halo_alpha = int(alpha * 0.15)
                pygame.draw.circle(star_surf, (shade, shade, shade, halo_alpha), (cx, cy), radius * 3)
                core_alpha = min(255, int(alpha * 1.2))
                pygame.draw.circle(star_surf, (min(255, shade + 40), min(255, shade + 40), min(255, shade + 40), core_alpha), (cx, cy), radius)
                self.screen.blit(star_surf, (x - cx, y - cy))

        # Particules flottantes (lucioles)
        self._draw_particles(w, h)

        # Silhouette de paysage en bas
        self._draw_landscape(w, h)

    def _draw_aurora(self, w, h):
        """Dessine l'aurore boréale animée."""
        aurora_surf = pygame.Surface((w, int(h * 0.5)), pygame.SRCALPHA)
        for bx, by, bw, bh, color, speed, phase in self._aurora_points:
            wave = math.sin(self._menu_time * speed + phase)
            wave2 = math.sin(self._menu_time * speed * 0.7 + phase + 1.5)
            offset_x = wave * w * 0.03
            offset_y = wave2 * h * 0.02
            cx = int(bx * w + offset_x)
            cy = int(by * h + offset_y)
            rw = int(bw * w)
            rh = int(bh * h)
            alpha_base = 35 + int(wave * 15)
            for i in range(8):
                t = i / 8
                a = max(0, alpha_base - int(t * alpha_base * 0.8))
                stretch = 1.0 + t * 0.6
                r = int(rw * stretch)
                rh_i = int(rh * (1.0 - t * 0.4))
                local_color = (
                    min(255, color[0] + int(wave * 20)),
                    min(255, color[1] + int(wave2 * 15)),
                    min(255, color[2] + int(wave * 10))
                )
                pygame.draw.ellipse(aurora_surf, (*local_color, a), (cx - r, cy - rh_i // 2, r * 2, rh_i))
        self.screen.blit(aurora_surf, (0, 0))

    def _draw_particles(self, w, h):
        """Dessine les particules flottantes (lucioles)."""
        for x_ratio, y_ratio, size, speed, phase, drift, color_type in self._particles:
            px = (x_ratio + math.sin(self._menu_time * speed + phase) * 0.02 + self._menu_time * drift * 0.01) % 1.0
            py = y_ratio + math.sin(self._menu_time * speed * 0.5 + phase * 2) * 0.015
            x = int(px * w)
            y = int(py * h)
            glow_pulse = math.sin(self._menu_time * speed * 2 + phase) * 0.5 + 0.5
            if color_type == "warm":
                base_r, base_g, base_b = 255, 200, 80
            elif color_type == "cool":
                base_r, base_g, base_b = 100, 200, 255
            else:
                base_r, base_g, base_b = 220, 220, 255
            alpha = int(120 + glow_pulse * 135)
            glow_size = int(size * 3)
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            glow_a = int(alpha * 0.25)
            pygame.draw.circle(glow_surf, (base_r, base_g, base_b, glow_a), (glow_size, glow_size), glow_size)
            core_a = min(255, int(alpha * 1.5))
            pygame.draw.circle(glow_surf, (min(255, base_r + 30), min(255, base_g + 30), min(255, base_b + 30), core_a), (glow_size, glow_size), int(size))
            self.screen.blit(glow_surf, (x - glow_size, y - glow_size))

    def _draw_landscape(self, w, h):
        """Dessine la silhouette du paysage en bas de l'écran."""
        hills = self._landscape["hills"]
        trees = self._landscape["trees"]
        landscape_h = int(h * 0.25)
        landscape_y = h - landscape_h

        # Couche arrière (montagnes lointaines, plus sombres)
        back_surf = pygame.Surface((w, landscape_h + 4), pygame.SRCALPHA)
        back_points = []
        for i, (xr, yr) in enumerate(hills):
            x = int(xr * w)
            y_offset = math.sin(self._menu_time * 0.15 + xr * 3) * 3
            y = int((yr - 0.82 + 0.82) * landscape_h + y_offset + 15)
            back_points.append((x, y))
        if len(back_points) > 1:
            back_points.append((w, landscape_h + 4))
            back_points.append((0, landscape_h + 4))
            pygame.draw.polygon(back_surf, (6, 10, 22, 200), back_points)
        self.screen.blit(back_surf, (0, landscape_y))

        # Couche avant (collines, légèrement plus claires)
        front_surf = pygame.Surface((w, landscape_h + 4), pygame.SRCALPHA)
        front_points = []
        rng = random.Random(55)
        for i, (xr, yr) in enumerate(hills):
            x = int(xr * w)
            offset = math.sin(self._menu_time * 0.1 + xr * 2.5) * 2
            y = int((yr - 0.82 + 0.82) * landscape_h + offset)
            front_points.append((x, y))
        if len(front_points) > 1:
            front_points.append((w, landscape_h + 4))
            front_points.append((0, landscape_h + 4))
            pygame.draw.polygon(front_surf, (4, 8, 18, 230), front_points)
        self.screen.blit(front_surf, (0, landscape_y))

        # Arbres en silhouette
        for tx, ty, tsize in trees:
            tree_x = int(tx * w)
            tree_y_base = int((ty - 0.82 + 0.82) * landscape_h)
            tree_h = int(tsize * h * 0.6)
            tree_w = int(tsize * w * 0.15)
            trunk_w = max(2, tree_w // 4)
            trunk_h = tree_h // 3
            trunk_x = tree_x - trunk_w // 2
            trunk_y = landscape_y + tree_y_base - trunk_h
            pygame.draw.rect(self.screen, (3, 6, 14), (trunk_x, trunk_y, trunk_w, trunk_h))
            canopy_y = trunk_y - tree_h * 2 // 3
            pygame.draw.polygon(self.screen, (4, 8, 18), [
                (tree_x, canopy_y),
                (tree_x - tree_w, canopy_y + tree_h * 2 // 3),
                (tree_x + tree_w, canopy_y + tree_h * 2 // 3)
            ])

    def _draw_button(self, text, cx, cy, w, h, selected=False, font_size_pct=2.5):
        """Dessine un bouton centré sur (cx, cy)."""
        x = cx - w // 2
        y = cy - h // 2
        rect = pygame.Rect(x, y, w, h)
        br = max(4, h // 5)

        # Ombre
        shadow = pygame.Surface((w, h + 8), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 130 if selected else 80), (0, 4, w, h), border_radius=br)
        self.screen.blit(shadow, (x, y))

        # Glow
        if selected:
            glow = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)
            pulse = int(abs(math.sin(self._menu_time * 3)) * 30) + 50
            pygame.draw.rect(glow, (112, 165, 255, pulse), (0, 0, w + 20, h + 20), border_radius=br + 6)
            self.screen.blit(glow, (x - 10, y - 10))

        # Fond
        color = self.BUTTON_SELECTED if selected else self.BUTTON_DEFAULT
        border_c = self.BUTTON_BORDER if selected else (80, 100, 150)
        btn_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, (*color, 230), (0, 0, w, h), border_radius=br)
        highlight = tuple(min(255, c + 40) for c in color)
        pygame.draw.line(btn_surf, (*highlight, 150), (12, 2), (w - 12, 2), 1)
        self.screen.blit(btn_surf, (x, y))
        pygame.draw.rect(self.screen, border_c, rect, 2, border_radius=br)

        # Texte
        font = pygame.font.Font(None, self._font(font_size_pct))
        text_color = (255, 255, 255) if selected else (200, 210, 235)
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=(cx, cy))
        if selected:
            shadow_t = font.render(text, True, (0, 0, 0))
            self.screen.blit(shadow_t, (text_rect.x + 2, text_rect.y + 2))
        self.screen.blit(text_surf, text_rect)

        return rect

    # ─── Main Menu ───────────────────────────────────────────

    def draw_main_menu(self):
        self._draw_gradient_background()
        w, h = self._W(), self._H()

        # Panneau titre
        title_w = int(w * 0.6)
        title_h = int(h * 0.16)
        title_x = (w - title_w) // 2
        title_y = int(h * 0.04)

        panel = pygame.Surface((title_w, title_h), pygame.SRCALPHA)
        for i in range(title_h):
            t = i / title_h
            alpha = int(210 - t * 30)
            r, g, b = int(10 + t * 5), int(16 + t * 8), int(34 + t * 15)
            pygame.draw.line(panel, (r, g, b, alpha), (0, i), (title_w, i))
        border_alpha = int(180 + math.sin(self._menu_time * 1.5) * 30)
        pygame.draw.rect(panel, (150, 180, 255, border_alpha), (0, 0, title_w, title_h), 3, border_radius=18)
        self.screen.blit(panel, (title_x, title_y))

        # Titre
        title_font = pygame.font.Font(None, self._font(6))
        shadow = title_font.render("MMO 2D", True, (0, 0, 0))
        title = title_font.render("MMO 2D", True, (240, 245, 255))
        tr = title.get_rect(center=(w // 2, title_y + title_h * 0.4))
        self.screen.blit(shadow, (tr.x + 3, tr.y + 3))
        self.screen.blit(title, tr)

        # Sous-titre
        sub_alpha = int(200 + math.sin(self._menu_time * 0.8) * 55)
        sub_font = pygame.font.Font(None, self._font(3))
        sub = sub_font.render("Survie  |  Exploration  |  Construction", True, (199, 214, 248))
        sub.set_alpha(sub_alpha)
        sr = sub.get_rect(center=(w // 2, title_y + title_h * 0.75))
        self.screen.blit(sub, sr)

        # Version
        try:
            from systems.version import get_current_version
            ver = f"v{get_current_version()}"
        except Exception:
            ver = ""
        if ver:
            vf = pygame.font.Font(None, self._font(1.8))
            vs = vf.render(ver, True, (100, 120, 160))
            self.screen.blit(vs, (title_x + title_w - vs.get_width() - 15, title_y + 10))

        # Boutons
        btn_w = int(w * 0.28)
        btn_h = int(h * 0.065)
        start_y = int(h * 0.30)
        spacing = int(h * 0.095)

        for i, button in enumerate(self.main_buttons):
            cx = w // 2
            cy = start_y + i * spacing
            selected = (i == self.selected_button)
            self._draw_button(button["text"], cx, cy, btn_w, btn_h, selected, font_size_pct=2.8)

        # Personnage pixel art à droite
        try:
            sprite_manager = None
            from game.sprite_manager import get_sprite_manager
            sprite_manager = get_sprite_manager()
            player_sprite = sprite_manager.get_entity_sprite("player")
            if player_sprite:
                pw = int(h * 0.25)
                ph = int(pw * 48 / 32)
                scaled = pygame.transform.smoothscale(player_sprite, (pw, ph))
                px = int(w * 0.72)
                py = int(h * 0.35)
                self.screen.blit(scaled, (px, py))
        except Exception:
            pass

    def draw_options_menu(self):
        self._draw_gradient_background()
        w, h = self._W(), self._H()

        # Titre
        title_font = pygame.font.Font(None, self._font(5))
        title = title_font.render("Options", True, self.WHITE)
        self.screen.blit(title, title.get_rect(center=(w // 2, int(h * 0.08))))

        # Panneau options
        panel_w = int(w * 0.5)
        panel_h = int(h * 0.6)
        panel_x = (w - panel_w) // 2
        panel_y = int(h * 0.15)
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (16, 22, 40, 210), (0, 0, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(panel, (60, 80, 130, 150), (0, 0, panel_w, panel_h), 2, border_radius=12)
        self.screen.blit(panel, (panel_x, panel_y))

        opt_font = pygame.font.Font(None, self._font(2.8))
        btn_font = pygame.font.Font(None, self._font(2.4))

        row_h = int(panel_h * 0.12)
        cx = panel_x + panel_w // 2

        # Taille fenêtre
        y = panel_y + int(panel_h * 0.12)
        txt = opt_font.render(f"Taille de la fenetre: {self.window_scale_labels[self.current_scale_index]}", True, self.WHITE)
        self.screen.blit(txt, txt.get_rect(center=(cx, y)))
        btn_w = int(panel_w * 0.15)
        btn_h = int(row_h * 0.7)
        self._draw_button("<", cx - int(panel_w * 0.15), y + int(row_h * 0.5), btn_w, btn_h, self.selected_button == 0, 2.2)
        self._draw_button(">", cx + int(panel_w * 0.15), y + int(row_h * 0.5), btn_w, btn_h, self.selected_button == 1, 2.2)

        # Fullscreen
        y += row_h
        fs = opt_font.render(f"Plein ecran: {'Oui' if self.fullscreen else 'Non'}", True, self.WHITE)
        self.screen.blit(fs, fs.get_rect(center=(cx, y)))
        self._draw_button("Basculer", cx, y + int(row_h * 0.55), int(panel_w * 0.22), btn_h, self.selected_button == 2, 2.2)

        # Controles
        y += row_h
        ct = opt_font.render("Controles", True, self.WHITE)
        self.screen.blit(ct, ct.get_rect(center=(cx, y)))
        self._draw_button("Modifier", cx, y + int(row_h * 0.55), int(panel_w * 0.22), btn_h, self.selected_button == 3, 2.2)

        # Retour
        back_y = panel_y + panel_h - int(panel_h * 0.15)
        self._draw_button("Retour", cx, back_y, int(panel_w * 0.2), int(row_h * 0.8), self.selected_button == 4, 2.2)

    def draw_controls_menu(self):
        self._draw_gradient_background()
        w, h = self._W(), self._H()

        title_font = pygame.font.Font(None, self._font(4.5))
        title = title_font.render("Configuration des Controles", True, self.WHITE)
        self.screen.blit(title, title.get_rect(center=(w // 2, int(h * 0.06))))

        instr_font = pygame.font.Font(None, self._font(2.2))
        instr = instr_font.render("Cliquez sur une ligne pour modifier la touche", True, self.GRAY)
        self.screen.blit(instr, instr.get_rect(center=(w // 2, int(h * 0.11))))

        modifiable = [(k, v) for k, v in self.control_names.items() if k != "harvest"]

        panel_w = int(w * 0.65)
        panel_h = int(h * 0.7)
        panel_x = (w - panel_w) // 2
        panel_y = int(h * 0.14)
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (16, 22, 40, 210), (0, 0, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(panel, (60, 80, 130, 150), (0, 0, panel_w, panel_h), 2, border_radius=12)
        self.screen.blit(panel, (panel_x, panel_y))

        row_h = int(panel_h / (len(modifiable) + 1.5))
        opt_font = pygame.font.Font(None, self._font(2.4))
        key_font = pygame.font.Font(None, self._font(2.2))

        for i, (key, name) in enumerate(modifiable):
            y = panel_y + int(panel_h * 0.08) + i * row_h
            is_sel = (i == self.controls_menu_selected)

            if is_sel:
                sel_bg = pygame.Surface((panel_w - 20, row_h - 6), pygame.SRCALPHA)
                pulse = int(abs(math.sin(self._menu_time * 2)) * 20) + 40
                pygame.draw.rect(sel_bg, (112, 165, 255, pulse), (0, 0, panel_w - 20, row_h - 6), border_radius=8)
                self.screen.blit(sel_bg, (panel_x + 10, y))

            name_surf = opt_font.render(name, True, self.WHITE if is_sel else (180, 190, 220))
            self.screen.blit(name_surf, (panel_x + 20, y + row_h // 4))

            key_name = pygame.key.name(self.controls[key]).upper()
            key_color = (255, 220, 80) if is_sel else (140, 160, 200)
            key_surf = key_font.render(key_name, True, key_color)
            kw = key_surf.get_width() + 24
            kh = row_h - 12
            kx = panel_x + panel_w - kw - 20
            ky = y + 6
            kb = pygame.Surface((kw, kh), pygame.SRCALPHA)
            pygame.draw.rect(kb, (50, 70, 120, 180), (0, 0, kw, kh), border_radius=6)
            pygame.draw.rect(kb, (*key_color, 100), (0, 0, kw, kh), 1, border_radius=6)
            self.screen.blit(kb, (kx, ky))
            self.screen.blit(key_surf, (kx + 12, ky + kh // 2 - key_surf.get_height() // 2))

        # Retour
        back_y = panel_y + panel_h - int(row_h * 0.8)
        self._draw_button("Retour aux Options", w // 2, back_y, int(w * 0.22), int(row_h * 0.8), self.controls_menu_selected >= len(modifiable), 2.2)

    # ─── Save/Load ───────────────────────────────────────────

    def draw_save_load_menu(self, menu_type):
        self._draw_gradient_background()
        w, h = self._W(), self._H()

        title_font = pygame.font.Font(None, self._font(4.5))
        title_text = "Charger une partie" if menu_type == "load" else "Sauvegarder la partie"
        title = title_font.render(title_text, True, self.WHITE)
        self.screen.blit(title, title.get_rect(center=(w // 2, int(h * 0.06))))

        opt_font = pygame.font.Font(None, self._font(2.4))
        small_font = pygame.font.Font(None, self._font(2))
        btn_font = pygame.font.Font(None, self._font(2.2))

        slot_w = int(w * 0.55)
        slot_h = int(h * 0.13)
        start_y = int(h * 0.16)
        spacing = int(h * 0.17)

        for i in range(3):
            x = (w - slot_w) // 2
            y = start_y + i * spacing
            selected = (i == self.selected_save_slot)

            # Slot background
            slot_bg = pygame.Surface((slot_w, slot_h), pygame.SRCALPHA)
            if selected:
                slot_color = (88, 138, 255, 200)
                border_color = self.WHITE
            else:
                slot_color = (36, 44, 68, 200)
                border_color = self.GRAY
            pygame.draw.rect(slot_bg, slot_color, (0, 0, slot_w, slot_h), border_radius=10)
            self.screen.blit(slot_bg, (x, y))
            pygame.draw.rect(self.screen, border_color, (x, y, slot_w, slot_h), 2, border_radius=10)

            # Slot title
            slot_title = btn_font.render(f"Slot {i+1}", True, self.WHITE)
            self.screen.blit(slot_title, (x + 20, y + 10))

            if self.save_slots[i] and self.save_slots[i]["exists"]:
                info = self.save_slots[i]
                date_text = self.format_date(info["timestamp"])
                self.screen.blit(small_font.render(f"Sauvegarde: {date_text}", True, self.WHITE), (x + 20, y + int(slot_h * 0.3)))
                self.screen.blit(small_font.render(f"Temps: {info['playtime']}", True, self.WHITE), (x + 20, y + int(slot_h * 0.5)))
                self.screen.blit(small_font.render(f"Sante: {info['player_health']}/100", True, self.GREEN), (x + int(slot_w * 0.5), y + int(slot_h * 0.3)))
                action = "Entree: Charger" if menu_type == "load" else "Entree: Ecraser"
                self.screen.blit(small_font.render(action, True, self.YELLOW), (x + int(slot_w * 0.5), y + int(slot_h * 0.5)))
            else:
                self.screen.blit(opt_font.render("Slot vide", True, self.GRAY), (x + 20, y + int(slot_h * 0.35)))

        # Retour
        self._draw_button("Retour", w // 2, start_y + 3 * spacing + int(h * 0.03), int(w * 0.15), int(h * 0.055), self.selected_save_slot == 3, 2.2)

    # ─── Events ──────────────────────────────────────────────

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
            elif event.key == pygame.K_DOWN:
                self.selected_button = (self.selected_button + 1) % len(self.main_buttons)
            elif event.key == pygame.K_RETURN:
                return self.main_buttons[self.selected_button]["action"]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            w, h = self._W(), self._H()
            btn_w = int(w * 0.28)
            btn_h = int(h * 0.065)
            start_y = int(h * 0.30)
            spacing = int(h * 0.095)
            for i, button in enumerate(self.main_buttons):
                cx = w // 2
                cy = start_y + i * spacing
                rect = pygame.Rect(cx - btn_w // 2, cy - btn_h // 2, btn_w, btn_h)
                if rect.collidepoint(mouse_pos):
                    self.sound_manager.play('menu_click')
                    return button["action"]
        return None

    def handle_options_event(self, event):
        w, h = self._W(), self._H()
        panel_w = int(w * 0.5)
        panel_h = int(h * 0.6)
        panel_x = (w - panel_w) // 2
        panel_y = int(h * 0.15)
        cx = panel_x + panel_w // 2
        row_h = int(panel_h * 0.12)
        btn_h = int(row_h * 0.7)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_menu = "main"
                self.selected_button = 0
                self.save_settings()
            elif event.key == pygame.K_UP:
                self.selected_button = max(0, self.selected_button - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_button = min(4, self.selected_button + 1)
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                if self.selected_button <= 1:
                    direction = 1 if event.key == pygame.K_RIGHT else -1
                    self.current_scale_index = (self.current_scale_index + direction) % len(self.window_scales)
                    self.save_settings()
                    return "toggle_fullscreen"
            elif event.key == pygame.K_RETURN:
                if self.selected_button == 0:
                    self.current_scale_index = (self.current_scale_index - 1) % len(self.window_scales)
                    self.save_settings()
                    return "toggle_fullscreen"
                elif self.selected_button == 1:
                    self.current_scale_index = (self.current_scale_index + 1) % len(self.window_scales)
                    self.save_settings()
                    return "toggle_fullscreen"
                elif self.selected_button == 2:
                    self.fullscreen = not self.fullscreen
                    self.save_settings()
                    return "toggle_fullscreen"
                elif self.selected_button == 3:
                    self.current_menu = "controls"
                    self.controls_menu_selected = 0
                elif self.selected_button == 4:
                    self.current_menu = "main"
                    self.selected_button = 0
                    self.save_settings()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # < button
            if pygame.Rect(cx - int(panel_w * 0.15) - int(panel_w * 0.075), panel_y + int(panel_h * 0.12) + int(row_h * 0.15), int(panel_w * 0.15), btn_h).collidepoint(mouse_pos):
                self.current_scale_index = (self.current_scale_index - 1) % len(self.window_scales)
                self.save_settings()
                return "toggle_fullscreen"
            # > button
            if pygame.Rect(cx + int(panel_w * 0.075), panel_y + int(panel_h * 0.12) + int(row_h * 0.15), int(panel_w * 0.15), btn_h).collidepoint(mouse_pos):
                self.current_scale_index = (self.current_scale_index + 1) % len(self.window_scales)
                self.save_settings()
                return "toggle_fullscreen"
            # Fullscreen
            fs_y = panel_y + int(panel_h * 0.12) + row_h
            if pygame.Rect(cx - int(panel_w * 0.11), fs_y + int(row_h * 0.25), int(panel_w * 0.22), btn_h).collidepoint(mouse_pos):
                self.fullscreen = not self.fullscreen
                self.save_settings()
                return "toggle_fullscreen"
            # Controls
            ct_y = fs_y + row_h
            if pygame.Rect(cx - int(panel_w * 0.11), ct_y + int(row_h * 0.25), int(panel_w * 0.22), btn_h).collidepoint(mouse_pos):
                self.current_menu = "controls"
                self.controls_menu_selected = 0
            # Back
            back_y = panel_y + panel_h - int(panel_h * 0.15)
            if pygame.Rect(cx - int(panel_w * 0.1), back_y - int(row_h * 0.4), int(panel_w * 0.2), int(row_h * 0.8)).collidepoint(mouse_pos):
                self.current_menu = "main"
                self.selected_button = 0
                self.save_settings()
        return None

    def handle_controls_event(self, event):
        modifiable = [k for k in self.control_names.keys() if k != "harvest"]
        max_sel = len(modifiable)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_menu = "options"
                self.selected_button = 3
                self.save_settings()
            elif event.key == pygame.K_UP:
                self.controls_menu_selected = max(0, self.controls_menu_selected - 1)
            elif event.key == pygame.K_DOWN:
                self.controls_menu_selected = min(max_sel, self.controls_menu_selected + 1)
            elif event.key == pygame.K_RETURN:
                if self.controls_menu_selected < max_sel:
                    return f"remap_control_{modifiable[self.controls_menu_selected]}"
                else:
                    self.current_menu = "options"
                    self.selected_button = 3
                    self.save_settings()
        return None

    def handle_save_load_event(self, event, menu_type):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_menu = "main"
                self.selected_save_slot = 0
            elif event.key == pygame.K_UP:
                self.selected_save_slot = max(0, self.selected_save_slot - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_save_slot = min(3, self.selected_save_slot + 1)
            elif event.key == pygame.K_DELETE and menu_type == "load":
                if self.selected_save_slot < 3 and self.save_slots[self.selected_save_slot] and self.save_slots[self.selected_save_slot]["exists"]:
                    return f"delete_slot_{self.selected_save_slot}"
            elif event.key == pygame.K_RETURN:
                if self.selected_save_slot == 3:
                    self.current_menu = "main"
                    self.selected_save_slot = 0
                else:
                    if menu_type == "load":
                        if self.save_slots[self.selected_save_slot] and self.save_slots[self.selected_save_slot]["exists"]:
                            return f"load_slot_{self.selected_save_slot}"
                    else:
                        return f"save_slot_{self.selected_save_slot}"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            w, h = self._W(), self._H()
            slot_w = int(w * 0.55)
            slot_h = int(h * 0.13)
            start_y = int(h * 0.16)
            spacing = int(h * 0.17)
            for i in range(3):
                x = (w - slot_w) // 2
                y = start_y + i * spacing
                if pygame.Rect(x, y, slot_w, slot_h).collidepoint(mouse_pos):
                    self.selected_save_slot = i
                    if menu_type == "load" and self.save_slots[i] and self.save_slots[i]["exists"]:
                        return f"load_slot_{i}"
                    elif menu_type == "save":
                        return f"save_slot_{i}"
        return None

    # ─── Utils ───────────────────────────────────────────────

    def load_save_slots_info(self):
        if os.getenv('FLATPAK_ID') == 'io.github.Estemobs.ProjetMMO2D':
            save_dir = os.path.expanduser('~/.var/app/io.github.Estemobs.ProjetMMO2D/data/saves')
        else:
            save_dir = os.path.expanduser('~/ProjetMMO2D_saves')
        for i in range(3):
            save_file = os.path.join(save_dir, f"save_slot_{i}.json")
            if os.path.exists(save_file):
                try:
                    with open(save_file, "r") as f:
                        sd = json.load(f)
                    self.save_slots[i] = {
                        "timestamp": sd.get("timestamp", ""),
                        "playtime": sd.get("playtime", "00:00:00"),
                        "level_name": sd.get("level_name", "Monde"),
                        "player_health": sd.get("player", {}).get("health", 100),
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
        if 0 <= n <= 2:
            return self.save_slots[n]
        return None

    def delete_save_slot(self, slot_number):
        if os.getenv('FLATPAK_ID') == 'io.github.Estemobs.ProjetMMO2D':
            save_dir = os.path.expanduser('~/.var/app/io.github.Estemobs.ProjetMMO2D/data/saves')
        else:
            save_dir = os.path.expanduser('~/ProjetMMO2D_saves')
        try:
            save_file = os.path.join(save_dir, f"save_slot_{slot_number}.json")
            if os.path.exists(save_file):
                os.remove(save_file)
                self.save_slots[slot_number] = None
                return True
        except Exception:
            pass
        return False
