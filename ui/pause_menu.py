"""
Menu de pause pour le jeu MMO 2D
"""

import pygame
import math
from game.constants import s


class PauseMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.visible = False
        self._menu_time = 0.0
        
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
        self.BUTTON_BORDER = (189, 214, 255)
        
        # Boutons
        self.button_width = s(240)
        self.button_height = s(50)
        self.button_spacing = s(15)
        
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
        start_y = (screen_height - total_height) // 2 + s(40)
        
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
        
        self._menu_time += 0.016
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Fond semi-transparent avec le jeu visible en arrière-plan
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        
        # Panneau central
        panel_width = s(350)
        panel_height = s(400)
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2
        
        # Fond du panneau avec gradient
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        for i in range(panel_height):
            t = i / panel_height
            alpha = int(230 - t * 20)
            r = int(20 + t * 5)
            g = int(28 + t * 5)
            b = int(50 + t * 8)
            pygame.draw.line(panel, (r, g, b, alpha), (0, i), (panel_width, i))
        # Bordure lumineuse animée
        border_alpha = int(100 + math.sin(self._menu_time * 2) * 30)
        pygame.draw.rect(panel, (88, 138, 255, border_alpha), (0, 0, panel_width, panel_height), 2, border_radius=s(12))
        self.screen.blit(panel, (panel_x, panel_y))
        
        # Titre "PAUSE"
        title_font = pygame.font.Font(None, s(48))
        title_text = title_font.render("PAUSE", True, self.WHITE)
        title_rect = title_text.get_rect(center=(screen_width // 2, panel_y + s(50)))
        self.screen.blit(title_text, title_rect)
        
        # Ligne séparatrice
        sep_surf = pygame.Surface((panel_width - s(40), 2), pygame.SRCALPHA)
        pygame.draw.line(sep_surf, (88, 138, 255, 150), (0, 0), (panel_width - s(40), 0), 1)
        self.screen.blit(sep_surf, (panel_x + s(20), panel_y + s(80)))
        
        # Dessiner les boutons
        btn_font = pygame.font.Font(None, s(28))
        for i, button in enumerate(self.buttons):
            if i == self.selected_button:
                color = self.BUTTON_SELECTED
                border_color = self.WHITE
            else:
                color = self.BUTTON_DEFAULT
                border_color = self.GRAY
            
            # Fond du bouton avec effet glow
            btn_surface = pygame.Surface((button["rect"].width, button["rect"].height), pygame.SRCALPHA)
            pygame.draw.rect(btn_surface, (*color, 220), (0, 0, button["rect"].width, button["rect"].height), border_radius=s(8))
            pygame.draw.rect(btn_surface, (*border_color, 180), (0, 0, button["rect"].width, button["rect"].height), 2, border_radius=s(8))
            self.screen.blit(btn_surface, button["rect"])
            
            # Glow pour bouton sélectionné
            if i == self.selected_button:
                glow_surf = pygame.Surface((button["rect"].width + 12, button["rect"].height + 12), pygame.SRCALPHA)
                pulse = int(abs(math.sin(self._menu_time * 3)) * 25) + 40
                pygame.draw.rect(glow_surf, (112, 165, 255, pulse), (0, 0, button["rect"].width + 12, button["rect"].height + 12), border_radius=s(12))
                self.screen.blit(glow_surf, (button["rect"].x - 6, button["rect"].y - 6))
            
            # Texte du bouton
            text_color = (255, 255, 255) if i == self.selected_button else (200, 210, 235)
            button_text = btn_font.render(button["text"], True, text_color)
            text_rect = button_text.get_rect(center=button["rect"].center)
            if i == self.selected_button:
                shadow = btn_font.render(button["text"], True, (0, 0, 0))
                self.screen.blit(shadow, (text_rect.x + 1, text_rect.y + 1))
            self.screen.blit(button_text, text_rect)
        
        # Instructions en bas
        small_font = pygame.font.Font(None, s(18))
        instructions = [
            "Échap: Reprendre",
            "↑↓: Naviguer",
            "Entrée: Sélectionner"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = small_font.render(instruction, True, self.GRAY)
            inst_rect = inst_text.get_rect(center=(screen_width // 2, panel_y + panel_height - s(55) + i * s(18)))
            self.screen.blit(inst_text, inst_rect)
    
    def handle_event(self, event):
        """Gère les événements du menu de pause"""
        if not self.visible:
            return None
        
        action = None
        
        # Gestion des clics de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
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
        self.setup_buttons()  # Recalculer les positions
    
    def hide(self):
        """Cache le menu de pause"""
        self.visible = False
