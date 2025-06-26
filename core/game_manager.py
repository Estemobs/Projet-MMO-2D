"""
Gestionnaire principal du jeu MMO 2D
"""

import pygame
import random
import math
import time
import os
import sys

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from ui.inventory import InventoryUI
from ui.menu import Menu
from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, ENEMY_COUNT, COLORS, TARGET_FPS
from game.tiletype import TileType
from game.player import Player
from game.enemy import Enemy
from game.world import WorldGenerator
from game.camera import Camera
from game.hud import HUD
from game.render_manager import RenderManager
from game.gameplay_manager import GameplayManager
from game.minimap import MiniMap
from game.sprite_manager import get_sprite_manager
from core.items import create_items, create_recipes
from systems.save_system import SaveSystem

# Initialisation de Pygame
pygame.init()

class GameManager:
    """Gestionnaire principal du jeu"""
    
    def __init__(self):
        # État du jeu
        self.state = "menu"  # "menu", "playing", "paused"
        
        # Initialisation basique
        # Créer un écran temporaire pour charger les paramètres
        temp_screen = pygame.display.set_mode((800, 600))
        temp_font = pygame.font.Font(None, 24)
        
        # Charger les paramètres d'affichage
        temp_menu = Menu(temp_screen, temp_font)
        
        if temp_menu.fullscreen:
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            print(f"✅ Lancement en mode plein écran ({info.current_w}x{info.current_h})")
        else:
            resolution = temp_menu.resolutions[temp_menu.current_resolution]
            self.screen = pygame.display.set_mode(resolution)
            print(f"✅ Lancement en mode fenêtré ({resolution[0]}x{resolution[1]})")
            
        pygame.display.set_caption("MMO 2D - Jeu de survie")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Système de contenu
        self.items = create_items()
        self.recipes = create_recipes(self.items)
        
        # Sprite manager
        self.sprite_manager = get_sprite_manager()
        
        # Interfaces
        self.menu = Menu(self.screen, self.font)
        self.inventory_ui = InventoryUI(self.screen, self.font, self.sprite_manager)
        
        # Nouveaux gestionnaires modulaires
        self.render_manager = RenderManager(self.screen)
        self.gameplay_manager = GameplayManager()
        self.minimap = MiniMap(self.screen.get_width(), self.screen.get_height())  # Passer la vraie taille
        
        # Composants du jeu (initialisés quand on commence une partie)
        self.world_map = None
        self.player = None
        self.camera = None
        self.hud = None
        self.enemies = []
        self.dropped_inventories = []  # Liste des inventaires déposés
        
        # Système de temps
        self.game_start_time = None
        self.total_playtime = 0
        
        # Système de sauvegarde
        self.save_system = SaveSystem()
        
        # Variables pour le message de sauvegarde
        self.show_save_message = False
        self.save_message_timer = 0.0
        
        self.running = True

    def init_game(self):
        """Initialise une nouvelle partie"""
        # Utiliser le nouveau GameplayManager
        self.gameplay_manager.init_new_game(self.screen.get_width(), self.screen.get_height())
        
        # Récupérer les références depuis le GameplayManager
        self.world_map = self.gameplay_manager.world_map
        self.player = self.gameplay_manager.player
        self.camera = self.gameplay_manager.camera
        self.enemies = self.gameplay_manager.enemies
        self.dropped_inventories = self.gameplay_manager.death_markers
        
        # Initialiser le HUD
        self.hud = HUD(self.font)
        
        # Initialiser la minimap avec la carte du monde
        self.minimap.generate_world_minimap(self.world_map)
        
        # Donner quelques items de départ au joueur
        self._give_starting_items()
        
        self.state = "playing"

    def _give_starting_items(self):
        """Donne les items de départ au joueur"""
        self.player.inventory.add_item(self.items["wood"], 10)
        self.player.inventory.add_item(self.items["stone"], 5)
        self.player.inventory.add_item(self.items["apple"], 3)

    def save_game(self, slot_number=0):
        """Sauvegarde la partie"""
        if self.player is None:
            return False
            
        return self.save_system.save_game(
            slot_number, 
            self.player, 
            self.world_map, 
            self.enemies, 
            self.gameplay_manager.total_playtime
        )

    def load_game(self, slot_number=0):
        """Charge une partie"""
        game_data = self.save_system.load_game(slot_number)
        
        if not game_data:
            return False
            
        # Charger dans le GameplayManager
        self.gameplay_manager.load_game_data(game_data, self.screen.get_width(), self.screen.get_height())
        
        # Synchroniser les références
        self.world_map = self.gameplay_manager.world_map
        self.player = self.gameplay_manager.player
        self.camera = self.gameplay_manager.camera
        self.enemies = self.gameplay_manager.enemies
        self.dropped_inventories = self.gameplay_manager.death_markers
        
        # Réinitialiser le HUD
        self.hud = HUD(self.font)
        
        # Initialiser la minimap avec la carte du monde chargée
        self.minimap.generate_world_minimap(self.world_map)
        
        self.state = "playing"
        return True

    def handle_events(self):
        """Gère tous les événements du jeu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state == "menu":
                self._handle_menu_events(event)
            elif self.state == "playing":
                self._handle_game_events(event)

    def _handle_menu_events(self, event):
        """Gère les événements du menu"""
        action = self.menu.handle_event(event)
        if action == "new_game":
            self.init_game()
        elif action == "load_menu":
            self.menu.current_menu = "load_menu"
            self.menu.selected_save_slot = 0
            self.menu.refresh_save_slots()
        elif action == "save_menu":
            if self.player is not None:  # Autorise si un jeu est en cours
                self.menu.current_menu = "save_menu"
                self.menu.selected_save_slot = 0
                self.menu.refresh_save_slots()
            else:
                print("❌ Aucun jeu en cours à sauvegarder")
        elif action == "options":
            self.menu.current_menu = "options"
            self.menu.selected_button = 0
        elif action == "quit":
            self.running = False
        elif action == "toggle_fullscreen":
            self._toggle_fullscreen()
        elif action and action.startswith("remap_control_"):
            control_key = action.split("remap_control_")[-1]
            self._remap_control(control_key)
        elif action and action.startswith("load_slot_"):
            slot_number = int(action.split("_")[-1])
            if self.load_game(slot_number):
                print(f"✅ Partie chargée depuis le slot {slot_number}")
            else:
                print(f"❌ Impossible de charger le slot {slot_number}")
        elif action and action.startswith("save_slot_"):
            slot_number = int(action.split("_")[-1])
            if self.save_game(slot_number):
                print(f"✅ Partie sauvegardée dans le slot {slot_number}")
                self.menu.refresh_save_slots()  # Actualiser l'affichage
                
                # Retourner au jeu avec un message de confirmation
                self.state = "playing"
                self.show_save_message = True
                self.save_message_timer = 3.0  # Afficher pendant 3 secondes
            else:
                print(f"❌ Impossible de sauvegarder dans le slot {slot_number}")
        elif action and action.startswith("delete_slot_"):
            slot_number = int(action.split("_")[-1])
            if self.menu.delete_save_slot(slot_number):
                self.menu.refresh_save_slots()  # Actualiser l'affichage

    def _handle_game_events(self, event):
        """Gère les événements en jeu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = "menu"
                self.menu.current_menu = "main"
                self.menu.selected_button = 0
            elif event.key == pygame.K_F5:
                if self.save_game():
                    print("✅ Partie sauvegardée!")
                    # Afficher le message à l'écran aussi
                    self.show_save_message = True
                    self.save_message_timer = 3.0  # Afficher pendant 3 secondes
                else:
                    print("❌ Erreur lors de la sauvegarde")
            elif event.key == self.menu.controls["inventory"]:
                self.inventory_ui.toggle_visibility()
            elif event.key == self.menu.controls["build_mode"]:
                self.player.build_mode = not self.player.build_mode
                print(f"🏗️ Mode construction: {'ACTIVÉ' if self.player.build_mode else 'DÉSACTIVÉ'}")
            elif event.key == self.menu.controls["foundation"]:
                self.player.selected_building = "foundation"
                print("🧱 Sélectionné: Fondation")
            elif event.key == self.menu.controls["wall"]:
                self.player.selected_building = "wall"
                print("🏠 Sélectionné: Mur")
        
        # Passer les événements aux composants du jeu
        if hasattr(self.player, 'handle_event'):
            self.player.handle_event(event)
        
        if self.inventory_ui.visible:
            self.inventory_ui.handle_event(event, self.player.inventory, self.recipes)

    def update(self, dt):
        """Met à jour l'état du jeu"""
        if self.state == "playing":
            # Mettre à jour avec le GameplayManager
            keys = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            
            # Déléguer la mise à jour au GameplayManager
            self.gameplay_manager.update(keys, mouse_buttons, mouse_pos, dt, self.menu.controls, self.camera, self.items)
            
            # Synchroniser les références
            self.player = self.gameplay_manager.player
            self.enemies = self.gameplay_manager.enemies
            self.dropped_inventories = self.gameplay_manager.death_markers
            
            # Gestion du timer du message de sauvegarde
            if hasattr(self.gameplay_manager, 'show_save_message') and self.gameplay_manager.show_save_message:
                if hasattr(self.gameplay_manager, 'save_message_timer') and self.gameplay_manager.save_message_timer <= 0:
                    self.gameplay_manager.show_save_message = False

    def draw(self):
        """Dessine tout le contenu du jeu"""
        self.screen.fill(COLORS["BLACK"])
        
        if self.state == "menu":
            self.menu.draw()
        elif self.state == "playing":
            self._draw_game()
        
        pygame.display.flip()

    def _draw_game(self):
        """Dessine le contenu du jeu"""
        # Dessiner le monde avec le RenderManager
        self.render_manager.draw_world(self.world_map, self.camera)
        
        # Dessiner les entités avec le RenderManager
        self.render_manager.draw_entities(
            self.player, self.enemies, self.dropped_inventories, self.camera, 
            self.gameplay_manager.item_manager
        )
        
        # Dessiner la minimap en haut à gauche
        self.minimap.draw(self.screen, self.player, self.enemies, self.camera, self.dropped_inventories)
        
        # Dessiner le HUD
        self.hud.draw(self.screen, self.player, self)
        
        # Afficher le message de sauvegarde si nécessaire
        if hasattr(self, 'show_save_message') and self.show_save_message:
            self._draw_save_confirmation()
        
        # Dessiner l'interface d'inventaire
        if self.inventory_ui.visible:
            self.inventory_ui.draw(self.player.inventory, self.recipes)
        self.inventory_ui.draw(self.player.inventory, self.recipes)
        
        # Instructions
        if not self.inventory_ui.visible:
            self._draw_instructions()

    def _draw_instructions(self):
        """Dessine les instructions à l'écran avec les contrôles personnalisés"""
        # Récupérer les noms des touches configurées
        move_up = pygame.key.name(self.menu.controls["move_up"]).upper()
        move_down = pygame.key.name(self.menu.controls["move_down"]).upper()
        move_left = pygame.key.name(self.menu.controls["move_left"]).upper()
        move_right = pygame.key.name(self.menu.controls["move_right"]).upper()
        build_mode = pygame.key.name(self.menu.controls["build_mode"]).upper()
        inventory = pygame.key.name(self.menu.controls["inventory"]).upper()
        foundation = pygame.key.name(self.menu.controls["foundation"]).upper()
        wall = pygame.key.name(self.menu.controls["wall"]).upper()
        
        instructions = [
            f"{move_up}{move_left}{move_down}{move_right}: Se déplacer",
            "Clic gauche: Récolter les ressources ou construire", 
            f"{build_mode}: Activer/désactiver le mode construction",
            f"{foundation}: Sélectionner fondation, {wall}: Sélectionner mur",
            f"{inventory}: Ouvrir inventaire",
            "F5: Sauvegarder, Échap: Menu principal"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, COLORS["WHITE"])
            self.screen.blit(text, (10, self.screen.get_height() - 120 + i * 20))

    def _draw_save_confirmation(self):
        """Dessine le message de confirmation de sauvegarde"""
        # Créer le texte du message
        message = "✅ Partie sauvegardée !"
        big_font = pygame.font.Font(None, 48)
        text_surface = big_font.render(message, True, COLORS["GREEN"])
        
        # Calculer la position centrée avec la taille actuelle de l'écran
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        text_rect = text_surface.get_rect()
        text_x = (screen_width - text_rect.width) // 2
        text_y = screen_height // 4
        
        # Dessiner un fond semi-transparent
        background_padding = 20
        background_rect = pygame.Rect(
            text_x - background_padding,
            text_y - background_padding,
            text_rect.width + 2 * background_padding,
            text_rect.height + 2 * background_padding
        )
        
        # Surface avec transparence
        background_surface = pygame.Surface((background_rect.width, background_rect.height))
        background_surface.set_alpha(180)
        background_surface.fill(COLORS["BLACK"])
        self.screen.blit(background_surface, (background_rect.x, background_rect.y))
        
        # Bordure verte
        pygame.draw.rect(self.screen, COLORS["GREEN"], background_rect, 3)
        
        # Afficher le texte
        self.screen.blit(text_surface, (text_x, text_y))

    def _toggle_fullscreen(self):
        """Bascule entre le mode plein écran et fenêtré"""
        try:
            if self.menu.is_fullscreen():
                # Mode plein écran - utiliser toute la résolution de l'écran
                info = pygame.display.Info()
                self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
                print(f"✅ Mode plein écran activé ({info.current_w}x{info.current_h})")
            else:
                # Mode fenêtré
                current_resolution = self.menu.get_resolution()
                self.screen = pygame.display.set_mode(current_resolution)
                print(f"✅ Mode fenêtré activé ({current_resolution[0]}x{current_resolution[1]})")
            
            # Mettre à jour le menu avec le nouvel écran
            self.menu.screen = self.screen
            
            # Si on est en jeu, mettre à jour les autres composants
            if self.state == "playing":
                if hasattr(self, 'hud') and self.hud:
                    self.hud.screen = self.screen
                if hasattr(self, 'camera') and self.camera:
                    self.camera.update_screen_size(self.screen.get_width(), self.screen.get_height())
            
        except Exception as e:
            print(f"❌ Erreur lors du changement de mode d'affichage: {e}")
    
    def _remap_control(self, control_key):
        """Lance le processus de remapping d'une touche"""
        print(f"📝 Appuyez sur une nouvelle touche pour '{self.menu.control_names[control_key]}'...")
        print("   (Appuyez sur Échap pour annuler)")
        
        # Sauvegarder l'état actuel du menu
        previous_menu = self.menu.current_menu
        previous_selected = self.menu.controls_menu_selected
        
        # Attendre l'input de l'utilisateur
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("❌ Remapping annulé")
                        return
                    else:
                        # Assigner la nouvelle touche
                        old_key = pygame.key.name(self.menu.controls[control_key])
                        new_key = pygame.key.name(event.key)
                        
                        self.menu.controls[control_key] = event.key
                        self.menu.save_settings()
                        
                        print(f"✅ Contrôle '{self.menu.control_names[control_key]}' changé:")
                        print(f"   {old_key.upper()} → {new_key.upper()}")
                        waiting_for_key = False
            
            # Redessiner l'écran pendant l'attente
            self.menu.draw()
            
            # Afficher un message d'attente avec un fond plus visible
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Boîte de dialogue
            dialog_width = 500
            dialog_height = 150
            dialog_x = (self.screen.get_width() - dialog_width) // 2
            dialog_y = (self.screen.get_height() - dialog_height) // 2
            
            # Fond de la boîte
            pygame.draw.rect(self.screen, (40, 40, 40), (dialog_x, dialog_y, dialog_width, dialog_height))
            pygame.draw.rect(self.screen, (255, 255, 255), (dialog_x, dialog_y, dialog_width, dialog_height), 3)
            
            # Titre
            title_text = f"Modifier: {self.menu.control_names[control_key]}"
            title_surf = self.font.render(title_text, True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(dialog_x + dialog_width//2, dialog_y + 40))
            self.screen.blit(title_surf, title_rect)
            
            # Instructions
            waiting_text = "Appuyez sur une nouvelle touche..."
            waiting_surf = self.font.render(waiting_text, True, (255, 255, 0))
            waiting_rect = waiting_surf.get_rect(center=(dialog_x + dialog_width//2, dialog_y + 80))
            self.screen.blit(waiting_surf, waiting_rect)
            
            cancel_text = "(Échap pour annuler)"
            cancel_surf = self.small_font.render(cancel_text, True, (200, 200, 200))
            cancel_rect = cancel_surf.get_rect(center=(dialog_x + dialog_width//2, dialog_y + 110))
            self.screen.blit(cancel_surf, cancel_rect)
            
            pygame.display.flip()
            self.clock.tick(30)  # Limiter le FPS pendant l'attente

    def run(self):
        """Boucle principale du jeu"""
        while self.running:
            dt = self.clock.tick(TARGET_FPS) / 1000.0  # Delta time en secondes
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()

    def get_playtime(self):
        """Retourne le temps de jeu actuel"""
        if self.gameplay_manager.game_start_time and self.state == "playing":
            current_session = time.time() - self.gameplay_manager.game_start_time
            total_time = self.gameplay_manager.total_playtime + current_session
        else:
            total_time = self.gameplay_manager.total_playtime
        
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        seconds = int(total_time % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
