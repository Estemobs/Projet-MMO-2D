"""
Système de tutoriel intégré pour les nouveaux joueurs
"""

import pygame


class Tutorial:
    """Gère les notifications tutoriel au début de la partie."""

    # Étapes du tutoriel
    STEPS = [
        {
            "id": "welcome",
            "title": "Bienvenue !",
            "text": "Bienvenue dans le monde du MMO 2D !",
            "condition": "always",
            "duration": 3.0,
        },
        {
            "id": "move",
            "title": "Se déplacer",
            "text": "Utilise ZQSD ou les flèches pour te déplacer",
            "condition": "move",
            "duration": 4.0,
        },
        {
            "id": "harvest",
            "title": "Récolter",
            "text": "Clique gauche sur un arbre ou une pierre pour récolter",
            "condition": "harvest",
            "duration": 4.0,
        },
        {
            "id": "craft",
            "title": "Crafting",
            "text": "Appuie sur C pour ouvrir le crafting et créer des outils",
            "condition": "craft",
            "duration": 4.0,
        },
        {
            "id": "eat",
            "title": "Manger",
            "text": "Utilise clic droit sur la nourriture dans l'inventaire pour manger",
            "condition": "eat",
            "duration": 4.0,
        },
        {
            "id": "survive",
            "title": "Survivre",
            "text": "Oversee ta barre de faim et santé ! La nuit approche...",
            "condition": "always",
            "duration": 5.0,
        },
    ]

    def __init__(self):
        self.current_step = 0
        self.shown_steps = set()
        self.active_notification = None
        self.notification_timer = 0.0
        self.alpha = 0
        self.fade_in = True

        # Stats du joueur pour débloquer les étapes
        self.player_moved = False
        self.player_harvested = False
        self.player_crafted = False
        self.player_ate = False

    def on_player_move(self):
        """Appelé quand le joueur bouge pour la première fois."""
        self.player_moved = True

    def on_player_harvest(self):
        """Appelé quand le joueur récolte pour la première fois."""
        self.player_harvested = True

    def on_player_craft(self):
        """Appelé quand le joueur craft pour la première fois."""
        self.player_crafted = True

    def on_player_eat(self):
        """Appelé quand le joueur mange pour la première fois."""
        self.player_ate = True

    def _check_conditions(self):
        """Vérifie quelles étapes sont débloquées."""
        for i, step in enumerate(self.STEPS):
            if i in self.shown_steps:
                continue

            if step["condition"] == "always":
                return i
            elif step["condition"] == "move" and self.player_moved:
                return i
            elif step["condition"] == "harvest" and self.player_harvested:
                return i
            elif step["condition"] == "craft" and self.player_crafted:
                return i
            elif step["condition"] == "eat" and self.player_ate:
                return i

        return None

    def update(self, dt):
        """Met à jour le tutoriel."""
        # Vérifier s'il y a une nouvelle étape à montrer
        if self.active_notification is None:
            next_step = self._check_conditions()
            if next_step is not None:
                self.current_step = next_step
                self.active_notification = self.STEPS[next_step]
                self.notification_timer = self.active_notification["duration"]
                self.alpha = 0
                self.fade_in = True

        # Mettre à jour la notification active
        if self.active_notification:
            # Fade in
            if self.fade_in:
                self.alpha += 500 * dt
                if self.alpha >= 255:
                    self.alpha = 255
                    self.fade_in = False

            # Timer
            self.notification_timer -= dt
            if self.notification_timer <= 0:
                # Fade out
                self.alpha -= 300 * dt
                if self.alpha <= 0:
                    self.alpha = 0
                    self.shown_steps.add(self.current_step)
                    self.active_notification = None

    def draw(self, screen):
        """Dessine la notification tutoriel."""
        if self.active_notification is None or self.alpha <= 0:
            return

        screen_width = screen.get_width()

        # Position en haut de l'écran
        panel_width = 450
        panel_height = 70
        panel_x = (screen_width - panel_width) // 2
        panel_y = 60

        # Surface avec alpha
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)

        # Fond
        bg_alpha = int(self.alpha * 0.85)
        pygame.draw.rect(panel, (20, 30, 50, bg_alpha), (0, 0, panel_width, panel_height), border_radius=10)

        # Bordure dorée
        border_alpha = int(self.alpha * 0.9)
        pygame.draw.rect(panel, (255, 200, 80, border_alpha), (0, 0, panel_width, panel_height), 2, border_radius=10)

        screen.blit(panel, (panel_x, panel_y))

        # Titre (en haut)
        title_font = pygame.font.Font(None, 28)
        title = title_font.render(self.active_notification["title"], True, (255, 220, 120))
        title.set_alpha(int(self.alpha))
        screen.blit(title, (panel_x + 15, panel_y + 8))

        # Texte (en bas)
        text_font = pygame.font.Font(None, 22)
        text = text_font.render(self.active_notification["text"], True, (200, 210, 230))
        text.set_alpha(int(self.alpha))
        screen.blit(text, (panel_x + 15, panel_y + 38))

    def is_active(self):
        """Vérifie si une notification est active."""
        return self.active_notification is not None
