"""
Menu de configuration des contrôles avec style moderne
"""

import pygame
import math
from game.constants import s


class ControlsMenu:
    """Menu dédié à la configuration des contrôles."""

    def __init__(self, controls, control_names):
        self.controls = controls
        self.control_names = control_names
        self.selected_index = 0
        self.remapping = False
        self.remap_key = None
        self._time = 0.0

        # Couleurs
        self.WHITE = (245, 247, 255)
        self.GRAY = (132, 144, 170)
        self.BLUE = (88, 138, 255)
        self.DARK_GRAY = (36, 44, 68)

        # Contrôles modifiables (exclure la souris)
        self.modifiable = [(k, v) for k, v in self.control_names.items() if k != "harvest"]

    def draw(self, screen, time=0.0):
        """Dessine le menu des contrôles."""
        self._time = time
        screen_width = screen.get_width()

        # Fond
        bg = pygame.Surface((screen_width, screen.get_height()), pygame.SRCALPHA)
        bg.fill((8, 12, 24, 200))
        screen.blit(bg, (0, 0))

        # Panneau central
        panel_w = min(s(800), screen_width - s(80))
        panel_h = min(s(550), screen.get_height() - s(100))
        panel_x = (screen_width - panel_w) // 2
        panel_y = s(50)

        panel_bg = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        for i in range(panel_h):
            t = i / panel_h
            alpha = int(220 - t * 20)
            r = int(16 + t * 6)
            g = int(22 + t * 8)
            b = int(40 + t * 12)
            pygame.draw.line(panel_bg, (r, g, b, alpha), (0, i), (panel_w, i))
        border_alpha = int(140 + math.sin(time * 1.5) * 30) if time else 140
        pygame.draw.rect(panel_bg, (88, 138, 255, border_alpha), (0, 0, panel_w, panel_h), 2, border_radius=s(12))
        screen.blit(panel_bg, (panel_x, panel_y))

        # Titre
        title_font = pygame.font.Font(None, s(36))
        title = title_font.render("Configuration des Controles", True, self.WHITE)
        title_rect = title.get_rect(center=(screen_width // 2, panel_y + s(40)))
        screen.blit(title, title_rect)

        # Instructions
        instr_font = pygame.font.Font(None, s(20))
        instr = instr_font.render("Cliquez sur une ligne pour modifier la touche", True, self.GRAY)
        instr_rect = instr.get_rect(center=(screen_width // 2, panel_y + s(70)))
        screen.blit(instr, instr_rect)

        # Ligne séparatrice
        sep_y = panel_y + s(90)
        pygame.draw.line(screen, (88, 138, 255, 100), (panel_x + s(20), sep_y), (panel_x + panel_w - s(20), sep_y), 1)

        # Liste des contrôles
        item_h = s(45)
        start_y = panel_y + s(100)

        option_font = pygame.font.Font(None, s(24))
        key_font = pygame.font.Font(None, s(22))

        for i, (key, name) in enumerate(self.modifiable):
            y = start_y + i * item_h
            is_selected = (i == self.selected_index)

            # Fond de la ligne
            if is_selected:
                sel_bg = pygame.Surface((panel_w - s(40), item_h - s(4)), pygame.SRCALPHA)
                pulse = int(abs(math.sin(time * 2)) * 20) + 40
                pygame.draw.rect(sel_bg, (112, 165, 255, pulse), (0, 0, panel_w - s(40), item_h - s(4)), border_radius=s(6))
                screen.blit(sel_bg, (panel_x + s(20), y))

            # Nom du contrôle
            name_surf = option_font.render(name, True, self.WHITE if is_selected else (180, 190, 220))
            screen.blit(name_surf, (panel_x + s(30), y + s(12)))

            # Touche actuelle
            key_name = pygame.key.name(self.controls[key]).upper()
            key_color = (255, 220, 80) if is_selected else (140, 160, 200)

            # Fond du badge touche
            key_text = key_font.render(key_name, True, key_color)
            key_w = key_text.get_width() + s(20)
            key_bg = pygame.Surface((key_w, s(24)), pygame.SRCALPHA)
            bg_color = (50, 70, 120, 180) if is_selected else (40, 50, 80, 120)
            pygame.draw.rect(key_bg, bg_color, (0, 0, key_w, s(24)), border_radius=s(4))
            pygame.draw.rect(key_bg, (*key_color, 100), (0, 0, key_w, s(24)), 1, border_radius=s(4))
            screen.blit(key_bg, (panel_x + panel_w - s(30) - key_w, y + s(10)))
            screen.blit(key_text, (panel_x + panel_w - s(30) - key_w + s(10), y + s(12)))

        # Bouton retour
        btn_y = start_y + len(self.modifiable) * item_h + s(20)
        btn_w = s(200)
        btn_h = s(45)
        btn_x = (screen_width - btn_w) // 2

        is_back_selected = (self.selected_index == len(self.modifiable))
        self.back_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

        btn_bg = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
        if is_back_selected:
            pygame.draw.rect(btn_bg, (112, 165, 255, 220), (0, 0, btn_w, btn_h), border_radius=s(10))
            pulse = int(abs(math.sin(time * 3)) * 25) + 45
            glow = pygame.Surface((btn_w + s(14), btn_h + s(14)), pygame.SRCALPHA)
            pygame.draw.rect(glow, (112, 165, 255, pulse), (0, 0, btn_w + s(14), btn_h + s(14)), border_radius=s(14))
            screen.blit(glow, (btn_x - s(7), btn_y - s(7)))
        else:
            pygame.draw.rect(btn_bg, (62, 88, 148, 220), (0, 0, btn_w, btn_h), border_radius=s(10))
        screen.blit(btn_bg, (btn_x, btn_y))

        border_c = (189, 214, 255) if is_back_selected else (80, 100, 150)
        pygame.draw.rect(screen, border_c, self.back_rect, 2, border_radius=s(10))

        back_text = key_font.render("Retour aux Options", True, (255, 255, 255) if is_back_selected else (200, 210, 235))
        back_rect = back_text.get_rect(center=self.back_rect.center)
        screen.blit(back_text, back_rect)

        # Instructions de navigation
        nav_font = pygame.font.Font(None, s(18))
        nav_text = "↑↓: Naviguer • Entrée/Clic: Modifier • Échap: Retour"
        nav_surf = nav_font.render(nav_text, True, self.GRAY)
        nav_rect = nav_surf.get_rect(center=(screen_width // 2, panel_y + panel_h - s(20)))
        screen.blit(nav_surf, nav_rect)

        # Overlay de remapping
        if self.remapping:
            self._draw_remap_overlay(screen, time)

    def _draw_remap_overlay(self, screen, time):
        """Dessine l'overlay de remapping."""
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        dialog_w = s(450)
        dialog_h = s(180)
        dialog_x = (screen_width - dialog_w) // 2
        dialog_y = (screen_height - dialog_h) // 2

        dialog_bg = pygame.Surface((dialog_w, dialog_h), pygame.SRCALPHA)
        pygame.draw.rect(dialog_bg, (20, 28, 50, 240), (0, 0, dialog_w, dialog_h), border_radius=s(12))
        border_pulse = int(120 + math.sin(time * 3) * 40)
        pygame.draw.rect(dialog_bg, (255, 220, 80, border_pulse), (0, 0, dialog_w, dialog_h), 2, border_radius=s(12))
        screen.blit(dialog_bg, (dialog_x, dialog_y))

        # Titre
        control_name = self.control_names.get(self.remap_key, "")
        title_font = pygame.font.Font(None, s(32))
        title = title_font.render(f"Modifier: {control_name}", True, (245, 247, 255))
        title_rect = title.get_rect(center=(screen_width // 2, dialog_y + s(50)))
        screen.blit(title, title_rect)

        # Instruction
        instr_font = pygame.font.Font(None, s(24))
        instr = instr_font.render("Appuyez sur une nouvelle touche...", True, (255, 220, 80))
        instr_rect = instr.get_rect(center=(screen_width // 2, dialog_y + s(100)))
        screen.blit(instr, instr_rect)

        cancel_font = pygame.font.Font(None, s(20))
        cancel = cancel_font.render("(Echap pour annuler)", True, self.GRAY)
        cancel_rect = cancel.get_rect(center=(screen_width // 2, dialog_y + s(140)))
        screen.blit(cancel, cancel_rect)

    def handle_event(self, event):
        """Gère les événements. Retourne l'action ou None."""
        if self.remapping:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.remapping = False
                    self.remap_key = None
                    return None
                else:
                    old_key = pygame.key.name(self.controls[self.remap_key])
                    self.controls[self.remap_key] = event.key
                    self.remapping = False
                    self.remap_key = None
                    return "save_settings"
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"
            elif event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_index = min(len(self.modifiable), self.selected_index + 1)
            elif event.key == pygame.K_RETURN:
                if self.selected_index < len(self.modifiable):
                    self.remap_key = self.modifiable[self.selected_index][0]
                    self.remapping = True
                else:
                    return "back"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            # Vérifier les clics sur les lignes
            for i in range(len(self.modifiable)):
                # Approximation - dans un vrai système on stockerait les rects
                pass
            # Vérifier le clic sur le bouton retour
            if hasattr(self, 'back_rect') and self.back_rect.collidepoint(mouse_pos):
                return "back"

        return None
