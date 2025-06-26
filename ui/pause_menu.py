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
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.BLUE = (0, 100, 255)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        
        # Boutons
        self.button_width = 200
        self.button_height = 50
        self.button_spacing = 20
        
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
        start_y = (screen_height - total_height) // 2
        
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
        
        # Fond semi-transparent avec le jeu visible en arrière-plan
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(150)  # Transparence pour voir le jeu derrière
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Titre "PAUSE"
        title_text = self.big_font.render("PAUSE", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.screen.get_width()//2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Dessiner les boutons
        for i, button in enumerate(self.buttons):
            # Couleur du bouton
            if i == self.selected_button:
                color = self.BLUE
                text_color = self.WHITE
            else:
                color = self.GRAY
                text_color = self.WHITE
            
            # Fond du bouton
            pygame.draw.rect(self.screen, color, button["rect"])
            pygame.draw.rect(self.screen, self.WHITE, button["rect"], 2)
            
            # Texte du bouton
            button_text = self.font.render(button["text"], True, text_color)
            text_rect = button_text.get_rect(center=button["rect"].center)
            self.screen.blit(button_text, text_rect)
        
        # Instructions
        instructions = [
            "Échap: Reprendre la partie",
            "Flèches: Naviguer",
            "Entrée: Sélectionner"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = pygame.font.Font(None, 20).render(instruction, True, self.WHITE)
            self.screen.blit(inst_text, (50, self.screen.get_height() - 80 + i * 25))
    
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
