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
        self.YELLOW = (255, 255, 0)
        
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
        y += 50
        
        # Contrôles - Bouton pour accéder au menu des contrôles
        controls_text = "Contrôles"
        controls_surf = self.font.render(controls_text, True, self.WHITE)
        self.screen.blit(controls_surf, (50, y))
        self.draw_button("Modifier", 400, y-5, 100, 30, self.selected_button == 3)
        y += 80
        
        # Instructions
        instr1 = self.small_font.render("Utilisez ↑↓ pour naviguer, ←→ pour changer la résolution", True, self.GRAY)
        self.screen.blit(instr1, (50, y))
        y += 20
        instr2 = self.small_font.render("Entrée pour sélectionner", True, self.GRAY)
        self.screen.blit(instr2, (50, y))
        
        # Bouton retour
        self.draw_button("Retour", 50, self.screen.get_height() - 80, 100, 50, 
                        self.selected_button == 4)
    
    def draw_controls_menu(self):
        """Dessine le menu dédié aux contrôles"""
        self.screen.fill(self.BLACK)
        
        # Titre
        title = self.big_font.render("Configuration des Contrôles", True, self.WHITE)
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 50))
        self.screen.blit(title, title_rect)
        
        # Instructions
        instr = self.font.render("Cliquez sur un bouton pour modifier la touche correspondante", True, self.GRAY)
        instr_rect = instr.get_rect(center=(self.screen.get_width()//2, 100))
        self.screen.blit(instr, instr_rect)
        
        # Filtrer les contrôles modifiables (exclure la souris)
        modifiable_controls = [(k, v) for k, v in self.control_names.items() if k != "harvest"]
        
        # Afficher les contrôles avec de vrais boutons
        y = 150
        button_width = 200
        button_height = 40
        
        for i, (key, name) in enumerate(modifiable_controls):
            # Nom du contrôle
            name_surf = self.font.render(f"{name}:", True, self.WHITE)
            self.screen.blit(name_surf, (100, y + 10))
            
            # Touche actuelle
            key_name = pygame.key.name(self.controls[key]).upper()
            
            # Bouton pour modifier
            is_selected = self.controls_menu_selected == i
            button_color = self.BLUE if is_selected else self.GRAY
            border_color = self.WHITE if is_selected else self.DARK_GRAY
            
            button_x = 350
            button_rect = pygame.Rect(button_x, y, button_width, button_height)
            
            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, border_color, button_rect, 2)
            
            # Texte du bouton
            button_text = f"{key_name} (Cliquer pour modifier)"
            text_surf = self.button_font.render(button_text, True, self.WHITE)
            text_rect = text_surf.get_rect(center=button_rect.center)
            self.screen.blit(text_surf, text_rect)
            
            y += 60
        
        # Bouton pour retourner aux options
        retour_button_index = len(modifiable_controls)
        self.draw_button("Retour aux Options", self.screen.get_width()//2 - 100, 
                        self.screen.get_height() - 100, 200, 50, 
                        self.controls_menu_selected == retour_button_index)
        
        # Instructions de navigation
        y = self.screen.get_height() - 50
        nav_text = "↑↓: Naviguer • Entrée/Clic: Modifier • Échap: Retour"
        nav_surf = self.small_font.render(nav_text, True, self.GRAY)
        nav_rect = nav_surf.get_rect(center=(self.screen.get_width()//2, y))
        self.screen.blit(nav_surf, nav_rect)
    
    def load_save_slots_info(self):
        """Charge les informations des slots de sauvegarde"""
        import datetime
        
        for i in range(3):
            save_file = os.path.join("saves", f"save_slot_{i}.json")
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
                except:
                    self.save_slots[i] = None
            else:
                self.save_slots[i] = None
    
    def format_date(self, timestamp_str):
        """Formate une date pour l'affichage"""
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(timestamp_str)
            return dt.strftime("%d/%m/%Y %H:%M")
        except:
            return timestamp_str
    
    def draw_save_load_menu(self, menu_type):
        """Dessine le menu de sauvegarde ou de chargement"""
        self.screen.fill(self.BLACK)
        
        # Titre
        title_text = "Charger une partie" if menu_type == "load" else "Sauvegarder la partie"
        title = self.big_font.render(title_text, True, self.WHITE)
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 50))
        self.screen.blit(title, title_rect)
        
        # Instructions
        instruction = "Sélectionnez un slot de sauvegarde" if menu_type == "save" else "Sélectionnez une sauvegarde à charger"
        instr_surf = self.font.render(instruction, True, self.GRAY)
        instr_rect = instr_surf.get_rect(center=(self.screen.get_width()//2, 100))
        self.screen.blit(instr_surf, instr_rect)
        
        # Dessiner les slots de sauvegarde
        slot_width = 700
        slot_height = 120
        start_y = 150
        spacing = 140
        
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
            pygame.draw.rect(self.screen, slot_color, (x, y, slot_width, slot_height))
            pygame.draw.rect(self.screen, border_color, (x, y, slot_width, slot_height), 3)
            
            # Titre du slot
            slot_title = self.button_font.render(f"Slot {i+1}", True, self.WHITE)
            self.screen.blit(slot_title, (x + 20, y + 10))
            
            if self.save_slots[i] and self.save_slots[i]["exists"]:
                # Slot avec sauvegarde
                save_info = self.save_slots[i]
                
                # Date et heure
                date_text = self.format_date(save_info["timestamp"])
                date_surf = self.small_font.render(f"Sauvegardé le: {date_text}", True, self.WHITE)
                self.screen.blit(date_surf, (x + 20, y + 40))
                
                # Temps de jeu
                playtime_surf = self.small_font.render(f"Temps de jeu: {save_info['playtime']}", True, self.WHITE)
                self.screen.blit(playtime_surf, (x + 20, y + 60))
                
                # Monde
                world_surf = self.small_font.render(f"Monde: {save_info['level_name']}", True, self.WHITE)
                self.screen.blit(world_surf, (x + 20, y + 80))
                
                # Santé du joueur
                health_surf = self.small_font.render(f"Santé: {save_info['player_health']}/100", True, self.GREEN)
                self.screen.blit(health_surf, (x + 400, y + 40))
                
                if menu_type == "load":
                    action_text = "Appuyez sur Entrée pour charger"
                else:
                    action_text = "Appuyez sur Entrée pour écraser"
                action_surf = self.small_font.render(action_text, True, self.YELLOW)
                self.screen.blit(action_surf, (x + 400, y + 80))
                
            else:
                # Slot vide
                empty_text = self.font.render("Slot vide", True, self.GRAY)
                self.screen.blit(empty_text, (x + 20, y + 50))
                
                if menu_type == "save":
                    create_text = self.small_font.render("Appuyez sur Entrée pour créer une nouvelle sauvegarde", True, self.YELLOW)
                    self.screen.blit(create_text, (x + 200, y + 80))
                elif menu_type == "load":
                    unavailable_text = self.small_font.render("Aucune sauvegarde disponible", True, self.RED)
                    self.screen.blit(unavailable_text, (x + 200, y + 80))
        
        # Bouton retour
        button_y = start_y + 3 * spacing + 20
        self.draw_button("Retour", 50, button_y, 120, 50, 
                        self.selected_save_slot == 3)
        
        # Instructions de navigation
        nav_text = "Haut/Bas: Naviguer • Entrée: Sélectionner • Échap: Retour"
        nav_surf = self.small_font.render(nav_text, True, self.GRAY)
        nav_rect = nav_surf.get_rect(center=(self.screen.get_width()//2, self.screen.get_height() - 30))
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
                self.save_settings()
            elif event.key == pygame.K_UP:
                self.selected_button = max(0, self.selected_button - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_button = min(4, self.selected_button + 1)  # 0-4: résolution(</>), fullscreen, contrôles, retour
            elif event.key == pygame.K_LEFT:
                if self.selected_button == 0 or self.selected_button == 1:  # Résolution
                    self.current_resolution = (self.current_resolution - 1) % len(self.resolutions)
                    self.save_settings()
            elif event.key == pygame.K_RIGHT:
                if self.selected_button == 0 or self.selected_button == 1:  # Résolution
                    self.current_resolution = (self.current_resolution + 1) % len(self.resolutions)
                    self.save_settings()
            elif event.key == pygame.K_RETURN:
                if self.selected_button == 0:  # Résolution précédente
                    self.current_resolution = (self.current_resolution - 1) % len(self.resolutions)
                    self.save_settings()
                elif self.selected_button == 1:  # Résolution suivante
                    self.current_resolution = (self.current_resolution + 1) % len(self.resolutions)
                    self.save_settings()
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
            
            # Clic sur les boutons de résolution
            if pygame.Rect(400, 115, 40, 30).collidepoint(mouse_pos):  # Bouton <
                self.current_resolution = (self.current_resolution - 1) % len(self.resolutions)
                self.save_settings()
            elif pygame.Rect(450, 115, 40, 30).collidepoint(mouse_pos):  # Bouton >
                self.current_resolution = (self.current_resolution + 1) % len(self.resolutions)
                self.save_settings()
            # Clic sur le bouton fullscreen
            elif pygame.Rect(400, 165, 100, 30).collidepoint(mouse_pos):
                self.fullscreen = not self.fullscreen
                self.save_settings()
                return "toggle_fullscreen"
            # Clic sur le bouton contrôles
            elif pygame.Rect(400, 215, 100, 30).collidepoint(mouse_pos):
                self.current_menu = "controls"
                self.controls_menu_selected = 0
            # Clic sur le bouton retour
            elif pygame.Rect(50, self.screen.get_height() - 80, 100, 50).collidepoint(mouse_pos):
                self.current_menu = "main"
                self.selected_button = 0
                self.save_settings()
        
        return None
    
    def handle_controls_event(self, event):
        """Gère les événements du menu des contrôles"""
        modifiable_controls = [k for k in self.control_names.keys() if k != "harvest"]
        max_selection = len(modifiable_controls)  # +1 pour le bouton retour sera géré séparément
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_menu = "options"
                self.selected_button = 3  # Retour sur le bouton contrôles
                self.save_settings()
            elif event.key == pygame.K_UP:
                self.controls_menu_selected = max(0, self.controls_menu_selected - 1)
            elif event.key == pygame.K_DOWN:
                self.controls_menu_selected = min(max_selection, self.controls_menu_selected + 1)
            elif event.key == pygame.K_RETURN:
                if self.controls_menu_selected < max_selection:
                    # Modifier un contrôle
                    control_key = modifiable_controls[self.controls_menu_selected]
                    return f"remap_control_{control_key}"
                else:
                    # Bouton retour
                    self.current_menu = "options"
                    self.selected_button = 3
                    self.save_settings()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Vérifier les clics sur les boutons de contrôles
            y = 150
            button_height = 40
            button_width = 200
            button_x = 350
            
            for i, control_key in enumerate(modifiable_controls):
                button_rect = pygame.Rect(button_x, y + i * 60, button_width, button_height)
                if button_rect.collidepoint(mouse_pos):
                    return f"remap_control_{control_key}"
            
            # Vérifier le clic sur le bouton retour
            retour_rect = pygame.Rect(self.screen.get_width()//2 - 100, 
                                    self.screen.get_height() - 100, 200, 50)
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
            elif event.key == pygame.K_RETURN:
                if self.selected_save_slot == 3:  # Bouton retour
                    self.current_menu = "main"
                    self.selected_save_slot = 0
                else:
                    # Sauvegarder ou charger
                    if menu_type == "load":
                        if (self.save_slots[self.selected_save_slot] and 
                            self.save_slots[self.selected_save_slot]["exists"]):
                            return f"load_slot_{self.selected_save_slot}"
                    else:  # save
                        return f"save_slot_{self.selected_save_slot}"
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            slot_width = 700
            slot_height = 120
            start_y = 150
            spacing = 140
            
            # Vérifier les clics sur les slots
            for i in range(3):
                x = self.screen.get_width()//2 - slot_width//2
                y = start_y + i * spacing
                slot_rect = pygame.Rect(x, y, slot_width, slot_height)
                
                if slot_rect.collidepoint(mouse_pos):
                    self.selected_save_slot = i
                    if menu_type == "load":
                        if (self.save_slots[i] and self.save_slots[i]["exists"]):
                            return f"load_slot_{i}"
                    else:  # save
                        return f"save_slot_{i}"
            
            # Vérifier le clic sur le bouton retour
            button_y = start_y + 3 * spacing + 20
            retour_rect = pygame.Rect(50, button_y, 120, 50)
            if retour_rect.collidepoint(mouse_pos):
                self.current_menu = "main"
                self.selected_save_slot = 0
        
        return None
    
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
        """Retourne la résolution actuelle"""
        return self.resolutions[self.current_resolution]
    
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
