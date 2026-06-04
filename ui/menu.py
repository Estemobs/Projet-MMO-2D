import pygame
import json
import os
import math
import time as _time
from game.sound_manager import get_sound_manager
from game.constants import s, SCALE_FACTOR

class Menu:
    STAR_COUNT = 120
    STAR_X_MULTIPLIER = 37
    STAR_Y_MULTIPLIER = 91
    STAR_Y_OFFSET = 13
    STAR_GRID_SIZE = 1000
    STAR_RADIUS_BASE = 1
    STAR_RADIUS_VARIATION = 3
    STAR_SHADE_BASE = 165
    STAR_SHADE_VARIATION = 70
    VERSION_OFFSET_X = 55
    VERSION_OFFSET_Y = 38
    BUTTON_HIGHLIGHT = (240, 248, 255)
    DECORATIVE_STARS = None

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.big_font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)
        
        # Couleurs
        self.WHITE = (245, 247, 255)
        self.BLACK = (8, 12, 24)
        self.GRAY = (132, 144, 170)
        self.DARK_GRAY = (36, 44, 68)
        self.GREEN = (84, 214, 125)
        self.RED = (245, 98, 98)
        self.BLUE = (88, 138, 255)
        self.YELLOW = (255, 221, 129)
        self.PANEL = (16, 22, 40)
        self.BUTTON_DEFAULT = (62, 88, 148)
        self.BUTTON_SELECTED = (112, 165, 255)
        self.BUTTON_BORDER = (189, 214, 255)
        self.SHADOW = (0, 0, 0, 110)
        if Menu.DECORATIVE_STARS is None:
            Menu.DECORATIVE_STARS = self._generate_decorative_stars()
        self._background_stars = Menu.DECORATIVE_STARS
        self._background_cache = None
        self._background_cache_size = None
        self._menu_time = 0.0
        
        # Sound manager
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
        self.save_slots = [None, None, None]  # 3 slots de sauvegarde
        self.selected_save_slot = 0
        self.load_save_slots_info()
        
        # Options - Taille de fenêtre en pourcentage de la résolution native
        self.window_scales = [0.5, 0.75, 1.0]
        self.window_scale_labels = ["50%", "75%", "100%"]
        self.current_scale_index = 2  # 100% par défaut
        self.fullscreen = True  # Plein écran par défaut
        
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
            "move_left": "Aller à gauche",
            "move_right": "Aller à droite",
            "harvest": "Récolter/Construire",
            "build_mode": "Mode construction",
            "inventory": "Inventaire",
            "crafting": "Artisanat",
            "foundation": "Fondation",
            "wall": "Mur"
        }
        
        self.load_settings()
    
    def load_settings(self):
        """Charge les paramètres depuis un fichier"""
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    settings = json.load(f)
                    # Compatibilité: ancien format "resolution" (index 0-4) → nouveau "scale_index"
                    if "scale_index" in settings:
                        self.current_scale_index = settings["scale_index"]
                    elif "resolution" in settings:
                        # Mapper: 0→0, 1→0, 2→0, 3→1, 4→2
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
        """Sauvegarde les paramètres dans un fichier"""
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
    
    def draw_button(self, text, x, y, width, height, selected=False, font=None):
        """Dessine un bouton avec effet glow quand sélectionné."""
        if font is None:
            font = self.button_font
        rect = pygame.Rect(x, y, width, height)

        # Ombre portée
        shadow_surface = pygame.Surface((width, height + 6), pygame.SRCALPHA)
        shadow_alpha = 140 if selected else 90
        pygame.draw.rect(shadow_surface, (0, 0, 0, shadow_alpha), (0, 4, width, height), border_radius=s(12))
        self.screen.blit(shadow_surface, (x, y))

        # Effet glow pour le bouton sélectionné
        if selected:
            glow_surf = pygame.Surface((width + 16, height + 16), pygame.SRCALPHA)
            pulse = int(abs(math.sin(self._menu_time * 3)) * 30) + 50
            pygame.draw.rect(glow_surf, (112, 165, 255, pulse), (0, 0, width + 16, height + 16), border_radius=s(16))
            self.screen.blit(glow_surf, (x - 8, y - 8))

        # Fond du bouton
        color = self.BUTTON_SELECTED if selected else self.BUTTON_DEFAULT
        border_color = self.BUTTON_BORDER if selected else (80, 100, 150)

        # Dégradé subtil du bouton
        btn_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, (*color, 220), (0, 0, width, height), border_radius=s(12))
        # Ligne de highlight en haut
        highlight = tuple(min(255, c + 40) for c in color)
        pygame.draw.line(btn_surf, (*highlight, 150), (s(12), 2), (width - s(12), 2), 1)
        self.screen.blit(btn_surf, (x, y))

        # Bordure
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=s(12))

        # Texte
        text_color = (255, 255, 255) if selected else (200, 210, 235)
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
        # Ombre du texte
        if selected:
            shadow = font.render(text, True, (0, 0, 0))
            self.screen.blit(shadow, (text_rect.x + 1, text_rect.y + 1))
        self.screen.blit(text_surf, text_rect)

        return rect

    def _generate_decorative_stars(self):
        """Génère une liste déterministe de points lumineux avec phases de scintillement."""
        import random
        stars = []
        rng = random.Random(42)  # Seed fixe pour reproductibilité
        for i in range(self.STAR_COUNT):
            x_ratio = rng.random()
            y_ratio = rng.random() * 0.7  # Pas d'étoiles en bas
            radius = rng.choice([1, 1, 1, 2, 2, 3])
            base_shade = rng.randint(140, 255)
            phase = rng.uniform(0, math.pi * 2)  # Phase de scintillement
            speed = rng.uniform(0.5, 2.5)  # Vitesse de scintillement
            stars.append((x_ratio, y_ratio, radius, base_shade, phase, speed))
        return stars

    def _draw_gradient_background(self):
        """Dessine un fond dégradé avec étoiles scintillantes."""
        width, height = self.screen.get_size()
        self._menu_time += 0.016  # ~60fps

        # Cache du dégradé (pas besoin de le redessiner)
        if self._background_cache_size != (width, height) or self._background_cache is None:
            top_color = (6, 10, 30)
            bottom_color = (18, 35, 72)
            self._background_cache = pygame.Surface((width, height))

            for y in range(height):
                t = y / max(1, height - 1)
                r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
                g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
                b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
                pygame.draw.line(self._background_cache, (r, g, b), (0, y), (width, y))

            self._background_cache_size = (width, height)

        self.screen.blit(self._background_cache, (0, 0))

        # Dessiner les étoiles avec scintillement
        for x_ratio, y_ratio, radius, base_shade, phase, speed in self._background_stars:
            x = int(x_ratio * width)
            y = int(y_ratio * height)
            # Scintillement sinusoïdal
            twinkle = math.sin(self._menu_time * speed + phase) * 0.5 + 0.5  # 0.0 à 1.0
            shade = int(base_shade * (0.4 + 0.6 * twinkle))
            alpha = int(180 + 75 * twinkle)
            
            if radius <= 1:
                # Petite étoile : un simple pixel
                star_surf = pygame.Surface((2, 2), pygame.SRCALPHA)
                star_surf.fill((shade, shade, shade, alpha))
                self.screen.blit(star_surf, (x, y))
            else:
                # Grande étoile : cercle avec halo
                star_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
                # Halo extérieur
                halo_alpha = int(alpha * 0.2)
                pygame.draw.circle(star_surf, (shade, shade, shade, halo_alpha), (radius * 2, radius * 2), radius * 2)
                # Centre brillant
                pygame.draw.circle(star_surf, (shade, shade, shade, alpha), (radius * 2, radius * 2), radius)
                self.screen.blit(star_surf, (x - radius * 2, y - radius * 2))

    def _draw_title_block(self, title_text):
        """Dessine un panneau de titre moderne avec animation subtile."""
        title_width = min(s(900), self.screen.get_width() - s(80))
        title_x = self.screen.get_width() // 2 - title_width // 2
        title_rect = pygame.Rect(title_x, s(30), title_width, s(120))

        # Fond du panneau avec gradient
        panel_surface = pygame.Surface((title_rect.width, title_rect.height), pygame.SRCALPHA)
        # Dégradé vertical
        for i in range(title_rect.height):
            t = i / title_rect.height
            alpha = int(210 - t * 30)
            r = int(10 + t * 5)
            g = int(16 + t * 8)
            b = int(34 + t * 15)
            pygame.draw.line(panel_surface, (r, g, b, alpha), (0, i), (title_rect.width, i))
        # Bordure dorée subtile
        border_alpha = int(180 + math.sin(self._menu_time * 1.5) * 30)
        pygame.draw.rect(panel_surface, (150, 180, 255, border_alpha), panel_surface.get_rect(), 2, border_radius=s(18))
        self.screen.blit(panel_surface, title_rect.topleft)

        # Titre avec ombre portée
        title_font = pygame.font.Font(None, s(48))
        title_shadow = title_font.render(title_text, True, (0, 0, 0))
        title = title_font.render(title_text, True, (240, 245, 255))
        title_rect_pos = title.get_rect(center=(self.screen.get_width() // 2, s(68)))
        self.screen.blit(title_shadow, (title_rect_pos.x + 2, title_rect_pos.y + 2))
        self.screen.blit(title, title_rect_pos)

        # Sous-titre avec animation de fondu
        subtitle_alpha = int(200 + math.sin(self._menu_time * 0.8) * 55)
        subtitle_font = pygame.font.Font(None, s(24))
        subtitle = subtitle_font.render("Survie  •  Exploration  •  Construction", True, (199, 214, 248))
        subtitle.set_alpha(subtitle_alpha)
        subtitle_rect = subtitle.get_rect(center=(self.screen.get_width() // 2, s(105)))
        self.screen.blit(subtitle, subtitle_rect)

        # Version - auto-actualisée à chaque appel
        try:
            from systems.version import get_current_version
            version_label = f"v{get_current_version()}"
        except Exception:
            version_label = ""
        if version_label:
            small_font = pygame.font.Font(None, s(20))
            version_text = small_font.render(version_label, True, (140, 160, 200))
            self.screen.blit(version_text, (title_x + title_width - s(55), s(38)))
    
    def draw_main_menu(self):
        """Dessine le menu principal"""
        self._draw_gradient_background()
        self._draw_title_block("MMO 2D - Jeu de Survie")
        
        # Boutons
        button_width = s(300)
        button_height = s(60)
        start_y = s(200)
        spacing = s(80)
        button_font = pygame.font.Font(None, s(32))
        
        for i, button in enumerate(self.main_buttons):
            x = self.screen.get_width()//2 - button_width//2
            y = start_y + i * spacing
            selected = (i == self.selected_button)
            self.draw_button(button["text"], x, y, button_width, button_height, selected, button_font)
    
    def draw_options_menu(self):
        """Dessine le menu des options"""
        self._draw_gradient_background()
        
        # Titre
        title_font = pygame.font.Font(None, s(48))
        title = title_font.render("Options", True, self.WHITE)
        title_rect = title.get_rect(center=(self.screen.get_width()//2, s(50)))
        self.screen.blit(title, title_rect)
        
        option_font = pygame.font.Font(None, s(24))
        small_font = pygame.font.Font(None, s(20))
        btn_font = pygame.font.Font(None, s(32))
        
        y = s(120)
        
        # Taille de fenêtre
        scale_text = f"Taille de la fenêtre: {self.window_scale_labels[self.current_scale_index]}"
        res_surf = option_font.render(scale_text, True, self.WHITE)
        self.screen.blit(res_surf, (s(50), y))
        
        # Boutons taille
        self.draw_button("<", s(450), y-s(5), s(40), s(30), self.selected_button == 0, btn_font)
        self.draw_button(">", s(500), y-s(5), s(40), s(30), self.selected_button == 1, btn_font)
        y += s(50)
        
        # Mode plein écran
        fs_text = f"Plein écran: {'Oui' if self.fullscreen else 'Non'}"
        fs_surf = option_font.render(fs_text, True, self.WHITE)
        self.screen.blit(fs_surf, (s(50), y))
        self.draw_button("Basculer", s(450), y-s(5), s(100), s(30), self.selected_button == 2, btn_font)
        y += s(50)
        
        # Contrôles
        controls_text = "Contrôles"
        controls_surf = option_font.render(controls_text, True, self.WHITE)
        self.screen.blit(controls_surf, (s(50), y))
        self.draw_button("Modifier", s(450), y-s(5), s(100), s(30), self.selected_button == 3, btn_font)
        y += s(80)
        
        # Instructions
        instr1 = small_font.render("Utilisez ↑↓ pour naviguer, ←→ pour changer la taille", True, self.GRAY)
        self.screen.blit(instr1, (s(50), y))
        y += s(20)
        instr2 = small_font.render("Entrée pour sélectionner", True, self.GRAY)
        self.screen.blit(instr2, (s(50), y))
        
        # Bouton retour
        self.draw_button("Retour", s(50), self.screen.get_height() - s(80), s(100), s(50), 
                        self.selected_button == 4, btn_font)
    
    def draw_controls_menu(self):
        """Dessine le menu dédié aux contrôles"""
        self._draw_gradient_background()
        
        # Titre
        title_font = pygame.font.Font(None, s(48))
        title = title_font.render("Configuration des Contrôles", True, self.WHITE)
        title_rect = title.get_rect(center=(self.screen.get_width()//2, s(50)))
        self.screen.blit(title, title_rect)
        
        # Instructions
        option_font = pygame.font.Font(None, s(24))
        small_font = pygame.font.Font(None, s(20))
        btn_font = pygame.font.Font(None, s(32))
        
        instr = option_font.render("Cliquez sur un bouton pour modifier la touche correspondante", True, self.GRAY)
        instr_rect = instr.get_rect(center=(self.screen.get_width()//2, s(100)))
        self.screen.blit(instr, instr_rect)
        
        # Filtrer les contrôles modifiables (exclure la souris)
        modifiable_controls = [(k, v) for k, v in self.control_names.items() if k != "harvest"]
        
        # Afficher les contrôles avec de vrais boutons
        y = s(150)
        button_width = s(200)
        button_height = s(40)
        
        for i, (key, name) in enumerate(modifiable_controls):
            # Nom du contrôle
            name_surf = option_font.render(f"{name}:", True, self.WHITE)
            self.screen.blit(name_surf, (s(100), y + s(10)))
            
            # Touche actuelle
            key_name = pygame.key.name(self.controls[key]).upper()
            
            # Bouton pour modifier
            is_selected = self.controls_menu_selected == i
            button_color = self.BLUE if is_selected else self.GRAY
            border_color = self.WHITE if is_selected else self.DARK_GRAY
            
            button_x = s(400)
            button_rect = pygame.Rect(button_x, y, button_width, button_height)
            
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=s(6))
            pygame.draw.rect(self.screen, border_color, button_rect, 2, border_radius=s(6))
            
            # Texte du bouton
            button_text = f"{key_name} (Cliquer)"
            text_surf = small_font.render(button_text, True, self.WHITE)
            text_rect = text_surf.get_rect(center=button_rect.center)
            self.screen.blit(text_surf, text_rect)
            
            y += s(60)
        
        # Bouton pour retourner aux options
        retour_button_index = len(modifiable_controls)
        self.draw_button("Retour aux Options", self.screen.get_width()//2 - s(100), 
                        self.screen.get_height() - s(100), s(200), s(50), 
                        self.controls_menu_selected == retour_button_index, btn_font)
        
        # Instructions de navigation
        y = self.screen.get_height() - s(50)
        nav_text = "↑↓: Naviguer • Entrée/Clic: Modifier • Échap: Retour"
        nav_surf = small_font.render(nav_text, True, self.GRAY)
        nav_rect = nav_surf.get_rect(center=(self.screen.get_width()//2, y))
        self.screen.blit(nav_surf, nav_rect)
    
    def load_save_slots_info(self):
        """Charge les informations des slots de sauvegarde"""
        # Utiliser le même répertoire que SaveSystem
        if os.getenv('FLATPAK_ID') == 'io.github.Estemobs.ProjetMMO2D':
            save_dir = os.path.expanduser('~/.var/app/io.github.Estemobs.ProjetMMO2D/data/saves')
        else:
            save_dir = os.path.expanduser('~/ProjetMMO2D_saves')

        for i in range(3):
            save_file = os.path.join(save_dir, f"save_slot_{i}.json")
            if os.path.exists(save_file):
                try:
                    with open(save_file, "r") as f:
                        save_data = json.load(f)
                    
                    # Récupérer les informations de la sauvegarde
                    timestamp = save_data.get("timestamp", "Date inconnue")
                    playtime = save_data.get("playtime", "00:00:00")
                    level_name = save_data.get("level_name", "Monde généré")
                    player_health = save_data.get("player", {}).get("health", 100)
                    
                    self.save_slots[i] = {
                        "timestamp": timestamp,
                        "playtime": playtime,
                        "level_name": level_name,
                        "player_health": player_health,
                        "exists": True
                    }
                except Exception:
                    self.save_slots[i] = None
            else:
                self.save_slots[i] = None
    
    def format_date(self, timestamp_str):
        """Formate une date pour l'affichage"""
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(timestamp_str)
            return dt.strftime("%d/%m/%Y %H:%M")
        except Exception:
            return timestamp_str
    
    def draw_save_load_menu(self, menu_type):
        """Dessine le menu de sauvegarde ou de chargement"""
        self._draw_gradient_background()
        
        title_font = pygame.font.Font(None, s(48))
        option_font = pygame.font.Font(None, s(24))
        small_font = pygame.font.Font(None, s(20))
        btn_font = pygame.font.Font(None, s(32))
        
        # Titre
        title_text = "Charger une partie" if menu_type == "load" else "Sauvegarder la partie"
        title = title_font.render(title_text, True, self.WHITE)
        title_rect = title.get_rect(center=(self.screen.get_width()//2, s(50)))
        self.screen.blit(title, title_rect)
        
        # Instructions
        instruction = "Sélectionnez un slot de sauvegarde" if menu_type == "save" else "Sélectionnez une sauvegarde à charger"
        instr_surf = option_font.render(instruction, True, self.GRAY)
        instr_rect = instr_surf.get_rect(center=(self.screen.get_width()//2, s(100)))
        self.screen.blit(instr_surf, instr_rect)
        
        # Dessiner les slots de sauvegarde
        slot_width = s(700)
        slot_height = s(120)
        start_y = s(150)
        spacing = s(140)
        
        for i in range(3):
            x = self.screen.get_width()//2 - slot_width//2
            y = start_y + i * spacing
            selected = (i == self.selected_save_slot)
            
            # Couleur du slot
            if selected:
                slot_color = self.BLUE
                border_color = self.WHITE
            else:
                slot_color = self.DARK_GRAY
                border_color = self.GRAY
            
            # Dessiner le slot
            slot_surf = pygame.Surface((slot_width, slot_height), pygame.SRCALPHA)
            pygame.draw.rect(slot_surf, (*slot_color, 200), (0, 0, slot_width, slot_height), border_radius=s(8))
            self.screen.blit(slot_surf, (x, y))
            pygame.draw.rect(self.screen, border_color, (x, y, slot_width, slot_height), 2, border_radius=s(8))
            
            # Titre du slot
            slot_title = btn_font.render(f"Slot {i+1}", True, self.WHITE)
            self.screen.blit(slot_title, (x + s(20), y + s(10)))
            
            if self.save_slots[i] and self.save_slots[i]["exists"]:
                save_info = self.save_slots[i]
                
                date_text = self.format_date(save_info["timestamp"])
                date_surf = small_font.render(f"Sauvegardé le: {date_text}", True, self.WHITE)
                self.screen.blit(date_surf, (x + s(20), y + s(40)))
                
                playtime_surf = small_font.render(f"Temps de jeu: {save_info['playtime']}", True, self.WHITE)
                self.screen.blit(playtime_surf, (x + s(20), y + s(60)))
                
                world_surf = small_font.render(f"Monde: {save_info['level_name']}", True, self.WHITE)
                self.screen.blit(world_surf, (x + s(20), y + s(80)))
                
                health_surf = small_font.render(f"Santé: {save_info['player_health']}/100", True, self.GREEN)
                self.screen.blit(health_surf, (x + s(400), y + s(40)))
                
                if menu_type == "load":
                    action_surf = small_font.render("Entrée: Charger", True, self.YELLOW)
                    self.screen.blit(action_surf, (x + s(400), y + s(65)))
                    delete_surf = small_font.render("Suppr: Effacer", True, self.RED)
                    self.screen.blit(delete_surf, (x + s(400), y + s(85)))
                else:
                    action_surf = small_font.render("Entrée: Écraser", True, self.YELLOW)
                    self.screen.blit(action_surf, (x + s(400), y + s(80)))
                
                if menu_type == "load":
                    delete_button_x = x + slot_width - s(100)
                    delete_button_y = y + s(10)
                    delete_selected = selected and hasattr(self, 'delete_mode') and self.delete_mode
                    self.draw_button("Supprimer", delete_button_x, delete_button_y, s(80), s(30), delete_selected, btn_font)
                
            else:
                empty_text = option_font.render("Slot vide", True, self.GRAY)
                self.screen.blit(empty_text, (x + s(20), y + s(50)))
                
                if menu_type == "save":
                    create_text = small_font.render("Entrée: Créer nouvelle sauvegarde", True, self.YELLOW)
                    self.screen.blit(create_text, (x + s(200), y + s(80)))
                elif menu_type == "load":
                    unavailable_text = small_font.render("Aucune sauvegarde disponible", True, self.RED)
                    self.screen.blit(unavailable_text, (x + s(200), y + s(80)))
        
        # Bouton retour
        button_y = start_y + 3 * spacing + s(20)
        self.draw_button("Retour", s(50), button_y, s(120), s(50), 
                        self.selected_save_slot == 3, btn_font)
        
        # Instructions de navigation
        if menu_type == "load":
            nav_text = "↑↓: Naviguer • Entrée: Charger • Suppr: Effacer • Échap: Retour"
        else:
            nav_text = "↑↓: Naviguer • Entrée: Sauvegarder • Échap: Retour"
        nav_surf = small_font.render(nav_text, True, self.GRAY)
        nav_rect = nav_surf.get_rect(center=(self.screen.get_width()//2, self.screen.get_height() - s(30)))
        self.screen.blit(nav_surf, nav_rect)
    
    def handle_event(self, event):
        """Gère les événements du menu"""
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
        """Gère les événements du menu principal"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_button = (self.selected_button - 1) % len(self.main_buttons)
            elif event.key == pygame.K_DOWN:
                self.selected_button = (self.selected_button + 1) % len(self.main_buttons)
            elif event.key == pygame.K_RETURN:
                return self.main_buttons[self.selected_button]["action"]
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            button_width = s(300)
            button_height = s(60)
            start_y = s(200)
            spacing = s(80)
            
            for i, button in enumerate(self.main_buttons):
                x = self.screen.get_width()//2 - button_width//2
                y = start_y + i * spacing
                button_rect = pygame.Rect(x, y, button_width, button_height)
                
                if button_rect.collidepoint(mouse_pos):
                    self.sound_manager.play('menu_click')
                    return button["action"]
        
        return None
    
    def handle_options_event(self, event):
        """Gère les événements du menu des options"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_menu = "main"
                self.selected_button = 0
                self.save_settings()
            elif event.key == pygame.K_UP:
                self.selected_button = max(0, self.selected_button - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_button = min(4, self.selected_button + 1)
            elif event.key == pygame.K_LEFT:
                if self.selected_button <= 1:  # Taille de fenêtre
                    self.current_scale_index = (self.current_scale_index - 1) % len(self.window_scales)
                    self.save_settings()
                    return "toggle_fullscreen"  # Forcer le redémarrage de l'affichage
            elif event.key == pygame.K_RIGHT:
                if self.selected_button <= 1:  # Taille de fenêtre
                    self.current_scale_index = (self.current_scale_index + 1) % len(self.window_scales)
                    self.save_settings()
                    return "toggle_fullscreen"
            elif event.key == pygame.K_RETURN:
                if self.selected_button == 0:  # Taille précédente
                    self.current_scale_index = (self.current_scale_index - 1) % len(self.window_scales)
                    self.save_settings()
                    return "toggle_fullscreen"
                elif self.selected_button == 1:  # Taille suivante
                    self.current_scale_index = (self.current_scale_index + 1) % len(self.window_scales)
                    self.save_settings()
                    return "toggle_fullscreen"
                elif self.selected_button == 2:  # Basculer plein écran
                    self.fullscreen = not self.fullscreen
                    self.save_settings()
                    return "toggle_fullscreen"
                elif self.selected_button == 3:  # Menu contrôles
                    self.current_menu = "controls"
                    self.controls_menu_selected = 0
                elif self.selected_button == 4:  # Retour
                    self.current_menu = "main"
                    self.selected_button = 0
                    self.save_settings()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Clic sur les boutons de taille
            if pygame.Rect(s(450), s(115), s(40), s(30)).collidepoint(mouse_pos):
                self.current_scale_index = (self.current_scale_index - 1) % len(self.window_scales)
                self.save_settings()
                return "toggle_fullscreen"
            elif pygame.Rect(s(500), s(115), s(40), s(30)).collidepoint(mouse_pos):
                self.current_scale_index = (self.current_scale_index + 1) % len(self.window_scales)
                self.save_settings()
                return "toggle_fullscreen"
            # Clic sur le bouton fullscreen
            elif pygame.Rect(s(450), s(165), s(100), s(30)).collidepoint(mouse_pos):
                self.fullscreen = not self.fullscreen
                self.save_settings()
                return "toggle_fullscreen"
            # Clic sur le bouton contrôles
            elif pygame.Rect(s(450), s(215), s(100), s(30)).collidepoint(mouse_pos):
                self.current_menu = "controls"
                self.controls_menu_selected = 0
            # Clic sur le bouton retour
            elif pygame.Rect(s(50), self.screen.get_height() - s(80), s(100), s(50)).collidepoint(mouse_pos):
                self.current_menu = "main"
                self.selected_button = 0
                self.save_settings()
        
        return None
    
    def handle_controls_event(self, event):
        """Gère les événements du menu des contrôles"""
        modifiable_controls = [k for k in self.control_names.keys() if k != "harvest"]
        max_selection = len(modifiable_controls)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_menu = "options"
                self.selected_button = 3
                self.save_settings()
            elif event.key == pygame.K_UP:
                self.controls_menu_selected = max(0, self.controls_menu_selected - 1)
            elif event.key == pygame.K_DOWN:
                self.controls_menu_selected = min(max_selection, self.controls_menu_selected + 1)
            elif event.key == pygame.K_RETURN:
                if self.controls_menu_selected < max_selection:
                    control_key = modifiable_controls[self.controls_menu_selected]
                    return f"remap_control_{control_key}"
                else:
                    self.current_menu = "options"
                    self.selected_button = 3
                    self.save_settings()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            y = s(150)
            button_height = s(40)
            button_width = s(200)
            button_x = s(400)
            
            for i, control_key in enumerate(modifiable_controls):
                button_rect = pygame.Rect(button_x, y + i * s(60), button_width, button_height)
                if button_rect.collidepoint(mouse_pos):
                    return f"remap_control_{control_key}"
            
            retour_rect = pygame.Rect(self.screen.get_width()//2 - s(100), 
                                    self.screen.get_height() - s(100), s(200), s(50))
            if retour_rect.collidepoint(mouse_pos):
                self.current_menu = "options"
                self.selected_button = 3
                self.save_settings()
        
        return None
    
    def handle_save_load_event(self, event, menu_type):
        """Gère les événements du menu de sauvegarde/chargement"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_menu = "main"
                self.selected_save_slot = 0
            elif event.key == pygame.K_UP:
                self.selected_save_slot = max(0, self.selected_save_slot - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_save_slot = min(3, self.selected_save_slot + 1)
            elif event.key == pygame.K_DELETE and menu_type == "load":
                if (self.selected_save_slot < 3 and 
                    self.save_slots[self.selected_save_slot] and 
                    self.save_slots[self.selected_save_slot]["exists"]):
                    return f"delete_slot_{self.selected_save_slot}"
            elif event.key == pygame.K_RETURN:
                if self.selected_save_slot == 3:
                    self.current_menu = "main"
                    self.selected_save_slot = 0
                else:
                    if menu_type == "load":
                        if (self.save_slots[self.selected_save_slot] and 
                            self.save_slots[self.selected_save_slot]["exists"]):
                            return f"load_slot_{self.selected_save_slot}"
                    else:
                        return f"save_slot_{self.selected_save_slot}"
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            slot_width = s(700)
            slot_height = s(120)
            start_y = s(150)
            spacing = s(140)
            
            for i in range(3):
                x = self.screen.get_width()//2 - slot_width//2
                y = start_y + i * spacing
                slot_rect = pygame.Rect(x, y, slot_width, slot_height)
                
                if slot_rect.collidepoint(mouse_pos):
                    self.selected_save_slot = i
                    
                    if menu_type == "load" and self.save_slots[i] and self.save_slots[i]["exists"]:
                        delete_button_x = x + slot_width - s(100)
                        delete_button_y = y + s(10)
                        delete_rect = pygame.Rect(delete_button_x, delete_button_y, s(80), s(30))
                        
                        if delete_rect.collidepoint(mouse_pos):
                            return f"delete_slot_{i}"
                    
                    if menu_type == "load":
                        if (self.save_slots[i] and self.save_slots[i]["exists"]):
                            return f"load_slot_{i}"
                    else:
                        return f"save_slot_{i}"
            
            button_y = start_y + 3 * spacing + s(20)
            retour_rect = pygame.Rect(s(50), button_y, s(120), s(50))
            if retour_rect.collidepoint(mouse_pos):
                self.current_menu = "main"
                self.selected_save_slot = 0
        
        return None
    
    def delete_save_slot(self, slot_number):
        """Supprime une sauvegarde"""
        import os
        # Utiliser le même répertoire que SaveSystem
        if os.getenv('FLATPAK_ID') == 'io.github.Estemobs.ProjetMMO2D':
            save_dir = os.path.expanduser('~/.var/app/io.github.Estemobs.ProjetMMO2D/data/saves')
        else:
            save_dir = os.path.expanduser('~/ProjetMMO2D_saves')

        try:
            save_file = os.path.join(save_dir, f"save_slot_{slot_number}.json")
            if os.path.exists(save_file):
                os.remove(save_file)
                self.save_slots[slot_number] = None
                print(f"✅ Sauvegarde du slot {slot_number + 1} supprimée")
                return True
            else:
                print(f"❌ Aucune sauvegarde trouvée dans le slot {slot_number + 1}")
                return False
        except Exception as e:
            print(f"❌ Erreur lors de la suppression : {e}")
            return False
    
    def draw(self):
        """Dessine le menu actuel"""
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
        """Retourne la résolution calculée selon le scale sélectionné"""
        info = pygame.display.Info()
        native_w, native_h = info.current_w, info.current_h
        scale = self.window_scales[self.current_scale_index]
        return (int(native_w * scale), int(native_h * scale))
    
    def is_fullscreen(self):
        """Retourne si le mode plein écran est activé"""
        return self.fullscreen
    
    def refresh_save_slots(self):
        """Rafraîchit les informations des slots de sauvegarde"""
        self.load_save_slots_info()
    
    def get_save_slot_info(self, slot_number):
        """Retourne les informations d'un slot de sauvegarde"""
        if 0 <= slot_number <= 2:
            return self.save_slots[slot_number]
        return None
