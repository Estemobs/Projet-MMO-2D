"""
Affichage dynamique des raccourcis clavier en bas de l'écran
"""

import pygame


class ControlsHint:
    """Affiche les contrôles contextuels en bas de l'écran."""

    # Contrôles par défaut
    CONTROLS = {
        "move": "ZQSD / Flèches",
        "attack": "Clic gauche",
        "inventory": "E",
        "craft": "C",
        "build": "B",
        "minimap": "M",
        "pause": "Échap",
        "eat": "Clic droit (inventaire)",
    }

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 20)
        self.visible = True
        self.alpha = 180
        self.fade_speed = 2
        self.target_alpha = 180

    def set_context(self, context):
        """Change les hints affichés selon le contexte."""
        self.context = context

    def update(self, dt):
        """Met à jour l'opacité."""
        if self.alpha < self.target_alpha:
            self.alpha = min(self.target_alpha, self.alpha + self.fade_speed)
        elif self.alpha > self.target_alpha:
            self.alpha = max(self.target_alpha, self.alpha - self.fade_speed)

    def draw(self, screen, context="normal"):
        """
        Dessine les hints en bas de l'écran.
        context: "normal", "inventory", "crafting", "build"
        """
        if not self.visible:
            return

        # Définir les hints selon le contexte
        if context == "inventory":
            hints = [
                ("E", "Fermer"),
                ("Clic", "Utiliser/Équiper"),
                ("Clic droit", "Manger"),
            ]
        elif context == "crafting":
            hints = [
                ("C", "Fermer"),
                ("Clic", "Craft"),
            ]
        elif context == "build":
            hints = [
                ("B", "Quitter"),
                ("Clic", "Construire"),
                ("Molette", "Rotation"),
            ]
        else:
            hints = [
                ("ZQSD", "Déplacer"),
                ("E", "Inventaire"),
                ("C", "Craft"),
                ("B", "Construire"),
                ("Clic", "Récolter/Attaquer"),
                ("Échap", "Pause"),
            ]

        # Dessiner le panneau de fond
        panel_height = 30
        panel_y = self.screen_height - panel_height - 5

        bg_surface = pygame.Surface((self.screen_width, panel_height), pygame.SRCALPHA)
        bg_surface.fill((10, 15, 30, int(self.alpha * 0.6)))
        screen.blit(bg_surface, (0, panel_y))

        # Dessiner chaque hint
        x_offset = 20
        for key, label in hints:
            # Touche (fond clair)
            key_text = self.font.render(key, True, (200, 220, 255))
            key_bg = pygame.Surface((key_text.get_width() + 10, 20), pygame.SRCALPHA)
            key_bg.fill((50, 70, 120, int(self.alpha * 0.8)))
            screen.blit(key_bg, (x_offset - 5, panel_y + 5))
            screen.blit(key_text, (x_offset, panel_y + 6))

            x_offset += key_text.get_width() + 15

            # Label (texte gris)
            label_text = self.font.render(label, True, (160, 170, 190))
            label_text.set_alpha(int(self.alpha))
            screen.blit(label_text, (x_offset, panel_y + 6))
            x_offset += label_text.get_width() + 25
