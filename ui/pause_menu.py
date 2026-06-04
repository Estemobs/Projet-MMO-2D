"""
Menu de pause pour le jeu MMO 2D
"""

import pygame

class PauseMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.big_font = pygame.font.Font(None, 48)
        self.visible = False
        
        # Couleurs modernes (cohérentes avec le reste du jeu)
        self.WHITE = (245, 247, 255)
        self.BLACK = (8, 12, 24)
        self.GRAY = (132, 144, 170)
        self.BLUE = (88, 138, 255)
        self.GREEN = (84, 214, 125)
        self.RED = (245, 98, 98)
        self.PANEL = (16, 22, 40)
        self.BUTTON_DEFAULT = (62, 88, 148)
        self.BUTTON_SELECTED = (112, 165, 255)
        
        # Boutons
        self.button_width = 220
        self.button_height = 50
        self.button_spacing = 15
        
        self.selected_button = 0
        self.buttons = [
            {"text": "Reprendre", "action": "resume"},
            {"text": "Sauvegarder", "action": "save"},
            {"text": "Menu principal", "action": "menu"},
            {"text": "Quitter", "action": "quit"}
        ]
        
        # Calculer les positions des boutons
        self.setup_buttons()
    
    def setup_buttons(self):
        """Configure les positions des boutons"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        total_height = len(self.buttons) * self.button_height + (len(self.buttons) - 1) * self.button_spacing
        start_y = (screen_height - total_height) // 2 + 30
        
        for i, button in enumerate(self.buttons):
            button["rect"] = pygame.Rect(
                (screen_width - self.button_width) // 2,
                start_y + i * (self.button_height + self.button_spacing),
                self.button_width,
                self.button_height
            )
    
    def draw(self):
        """Dessine le menu de pause"""
        if not self.visible:
            return
        
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Fond semi-transparent avec le jeu visible en arrière-plan
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        
        # Panneau central
        panel_width = 300
        panel_height = 350
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2
        
        # Fond du panneau avec gradient
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel, (20, 28, 50, 230), (0, 0, panel_width, panel_height), border_radius=12)
        pygame.draw.rect(panel, (88, 138, 255, 100), (0, 0, panel_width, panel_height), 2, border_radius=12)
        self.screen.blit(panel, (panel_x, panel_y))
        
        # Titre "PAUSE"
        title_text = self.big_font.render("PAUSE", True, self.WHITE)
        title_rect = title_text.get_rect(center=(screen_width // 2, panel_y + 50))
        self.screen.blit(title_text, title_rect)
        
        # Ligne séparatrice
        pygame.draw.line(self.screen, (88, 138, 255, 150), 
                        (panel_x + 20, panel_y + 80), 
                        (panel_x + panel_width - 20, panel_y + 80), 1)
        
        # Dessiner les boutons
        for i, button in enumerate(self.buttons):
            # Couleur du bouton
            if i == self.selected_button:
                color = self.BUTTON_SELECTED
                border_color = self.WHITE
            else:
                color = self.BUTTON_DEFAULT
                border_color = self.GRAY
            
            # Fond du bouton
            btn_surface = pygame.Surface((button["rect"].width, button["rect"].height), pygame.SRCALPHA)
            pygame.draw.rect(btn_surface, (*color, 220), (0, 0, button["rect"].width, button["rect"].height), border_radius=8)
            pygame.draw.rect(btn_surface, (*border_color, 180), (0, 0, button["rect"].width, button["rect"].height), 2, border_radius=8)
            self.screen.blit(btn_surface, button["rect"])
            
            # Texte du bouton
            button_text = self.font.render(button["text"], True, self.WHITE)
            text_rect = button_text.get_rect(center=button["rect"].center)
            self.screen.blit(button_text, text_rect)
        
        # Instructions en bas
        instructions = [
            "Échap: Reprendre",
            "↑↓: Naviguer",
            "Entrée: Sélectionner"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = pygame.font.Font(None, 20).render(instruction, True, self.GRAY)
            inst_rect = inst_text.get_rect(center=(screen_width // 2, panel_y + panel_height - 50 + i * 18))
            self.screen.blit(inst_text, inst_rect)
    
    def handle_event(self, event):
        """Gère les événements du menu de pause"""
        if not self.visible:
            return None
        
        action = None
        
        # Gestion des clics de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    if button["rect"].collidepoint(mouse_pos):
                        self.selected_button = i
                        action = button["action"]
                        break
        
        # Gestion du clavier
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                action = "resume"
            
            elif event.key == pygame.K_UP:
                self.selected_button = (self.selected_button - 1) % len(self.buttons)
            
            elif event.key == pygame.K_DOWN:
                self.selected_button = (self.selected_button + 1) % len(self.buttons)
            
            elif event.key == pygame.K_RETURN:
                action = self.buttons[self.selected_button]["action"]
        
        return action
    
    def show(self):
        """Affiche le menu de pause"""
        self.visible = True
        self.selected_button = 0
    
    def hide(self):
        """Cache le menu de pause"""
        self.visible = False
