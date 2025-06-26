import pygame
import json
import os

class Menu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.big_font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (64, 64, 64)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 100, 255)
        
        # État du menu
        self.current_menu = "main"
        self.selected_button = 0
        
        # Boutons du menu principal
        self.main_buttons = [
            {"text": "Nouvelle Partie", "action": "new_game"},
            {"text": "Charger Partie", "action": "load_game"},
            {"text": "Options", "action": "options"},
            {"text": "Quitter", "action": "quit"}
        ]
        
        # Options
        self.resolutions = [
            (800, 600),
            (1024, 768),
            (1280, 720),
            (1366, 768),
            (1920, 1080)
        ]
        self.current_resolution = 1  # 1024x768 par défaut
        self.fullscreen = False
        
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
                    self.current_resolution = settings.get("resolution", 1)
                    self.fullscreen = settings.get("fullscreen", False)
                    self.controls.update(settings.get("controls", {}))
        except:
            pass
    
    def save_settings(self):
        """Sauvegarde les paramètres dans un fichier"""
        settings = {
            "resolution": self.current_resolution,
            "fullscreen": self.fullscreen,
            "controls": self.controls
        }
        try:
            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=4)
        except:
            pass
    
    def draw_button(self, text, x, y, width, height, selected=False):
        """Dessine un bouton"""
        color = self.BLUE if selected else self.GRAY
        border_color = self.WHITE if selected else self.DARK_GRAY
        
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 2)
        
        text_surf = self.button_font.render(text, True, self.WHITE)
        text_rect = text_surf.get_rect(center=(x + width//2, y + height//2))
        self.screen.blit(text_surf, text_rect)
        
        return pygame.Rect(x, y, width, height)
    
    def draw_main_menu(self):
        """Dessine le menu principal"""
        self.screen.fill(self.BLACK)
        
        # Titre
        title = self.big_font.render("MMO 2D - Jeu de Survie", True, self.WHITE)
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 100))
        self.screen.blit(title, title_rect)
        
        # Boutons
        button_width = 300
        button_height = 60
        start_y = 200
        spacing = 80
        
        for i, button in enumerate(self.main_buttons):
            x = self.screen.get_width()//2 - button_width//2
            y = start_y + i * spacing
            selected = (i == self.selected_button)
            self.draw_button(button["text"], x, y, button_width, button_height, selected)
    
    def draw_options_menu(self):
        """Dessine le menu des options"""
        self.screen.fill(self.BLACK)
        
        # Titre
        title = self.big_font.render("Options", True, self.WHITE)
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 50))
        self.screen.blit(title, title_rect)
        
        y = 120
        
        # Résolution
        res_text = f"Résolution: {self.resolutions[self.current_resolution][0]}x{self.resolutions[self.current_resolution][1]}"
        res_surf = self.font.render(res_text, True, self.WHITE)
        self.screen.blit(res_surf, (50, y))
        
        # Boutons résolution
        self.draw_button("<", 400, y-5, 40, 30, self.selected_button == 0)
        self.draw_button(">", 450, y-5, 40, 30, self.selected_button == 1)
        y += 50
        
        # Mode plein écran
        fs_text = f"Plein écran: {'Oui' if self.fullscreen else 'Non'}"
        fs_surf = self.font.render(fs_text, True, self.WHITE)
        self.screen.blit(fs_surf, (50, y))
        self.draw_button("Basculer", 400, y-5, 100, 30, self.selected_button == 2)
        y += 80
        
        # Contrôles
        controls_title = self.font.render("Contrôles:", True, self.WHITE)
        self.screen.blit(controls_title, (50, y))
        y += 40
        
        for i, (key, name) in enumerate(self.control_names.items()):
            if key != "harvest":  # Skip mouse controls
                key_name = pygame.key.name(self.controls[key]).upper()
                text = f"{name}: {key_name}"
                color = self.GREEN if self.selected_button == 3 + i else self.WHITE
                control_surf = self.small_font.render(text, True, color)
                self.screen.blit(control_surf, (70, y))
                y += 25
        
        # Bouton retour
        self.draw_button("Retour", 50, self.screen.get_height() - 80, 100, 50, 
                        self.selected_button == len(self.control_names) + 2)
    
    def handle_event(self, event):
        """Gère les événements du menu"""
        if self.current_menu == "main":
            return self.handle_main_menu_event(event)
        elif self.current_menu == "options":
            return self.handle_options_event(event)
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
            button_width = 300
            button_height = 60
            start_y = 200
            spacing = 80
            
            for i, button in enumerate(self.main_buttons):
                x = self.screen.get_width()//2 - button_width//2
                y = start_y + i * spacing
                button_rect = pygame.Rect(x, y, button_width, button_height)
                
                if button_rect.collidepoint(mouse_pos):
                    return button["action"]
        
        return None
    
    def handle_options_event(self, event):
        """Gère les événements du menu des options"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_menu = "main"
                self.selected_button = 0
            elif event.key == pygame.K_UP:
                self.selected_button = max(0, self.selected_button - 1)
            elif event.key == pygame.K_DOWN:
                max_selection = len(self.control_names) + 2
                self.selected_button = min(max_selection, self.selected_button + 1)
            elif event.key == pygame.K_RETURN:
                if self.selected_button == 0:  # Résolution précédente
                    self.current_resolution = (self.current_resolution - 1) % len(self.resolutions)
                elif self.selected_button == 1:  # Résolution suivante
                    self.current_resolution = (self.current_resolution + 1) % len(self.resolutions)
                elif self.selected_button == 2:  # Basculer plein écran
                    self.fullscreen = not self.fullscreen
                elif self.selected_button == len(self.control_names) + 2:  # Retour
                    self.current_menu = "main"
                    self.selected_button = 0
                    self.save_settings()
        
        return None
    
    def draw(self):
        """Dessine le menu actuel"""
        if self.current_menu == "main":
            self.draw_main_menu()
        elif self.current_menu == "options":
            self.draw_options_menu()
        
        pygame.display.flip()
    
    def get_resolution(self):
        """Retourne la résolution actuelle"""
        return self.resolutions[self.current_resolution]
    
    def is_fullscreen(self):
        """Retourne si le mode plein écran est activé"""
        return self.fullscreen
