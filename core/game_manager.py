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
        
        # Interfaces
        self.menu = Menu(self.screen, self.font)
        self.inventory_ui = InventoryUI(self.screen, self.font)
        
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
        self.world_map = WorldGenerator.generate_map()
        self.player = Player(MAP_WIDTH * TILE_SIZE // 2, MAP_HEIGHT * TILE_SIZE // 2)
        self.camera = Camera(self.screen.get_width(), self.screen.get_height())
        self.hud = HUD(self.font)
        self.dropped_inventories = []  # Réinitialiser les inventaires déposés
        
        # Initialiser le temps de jeu
        self.game_start_time = time.time()
        self.total_playtime = 0
        
        # Générer quelques ennemis
        self._spawn_enemies()
        
        # Donner quelques items de départ au joueur
        self._give_starting_items()
        
        self.state = "playing"

    def _spawn_enemies(self):
        """Génère les ennemis dans le monde"""
        self.enemies = []
        for _ in range(ENEMY_COUNT):
            while True:
                enemy_x = random.randint(0, MAP_WIDTH - 1) * TILE_SIZE
                enemy_y = random.randint(0, MAP_HEIGHT - 1) * TILE_SIZE
                
                tile_x = int(enemy_x // TILE_SIZE)
                tile_y = int(enemy_y // TILE_SIZE)
                distance_from_player = math.sqrt((enemy_x - self.player.x)**2 + (enemy_y - self.player.y)**2)
                
                if (self.world_map[tile_y][tile_x] == TileType.GRASS and 
                    distance_from_player > 200):
                    self.enemies.append(Enemy(enemy_x, enemy_y))
                    break

    def _give_starting_items(self):
        """Donne les items de départ au joueur"""
        self.player.inventory.add_item(self.items["wood"], 10)
        self.player.inventory.add_item(self.items["stone"], 5)
        self.player.inventory.add_item(self.items["apple"], 3)

    def get_tile_color(self, tile_type):
        """Retourne la couleur d'un type de tile"""
        color_map = {
            TileType.GRASS: COLORS["GREEN"],
            TileType.TREE: COLORS["BROWN"],
            TileType.STONE: COLORS["GRAY"],
            TileType.IRON_ORE: COLORS["DARK_GRAY"],
            TileType.WALL: (255, 165, 0),  # Orange
            TileType.FOUNDATION: (255, 255, 0),  # Jaune
            TileType.GOLD_ORE: (255, 215, 0),  # Or
            TileType.DIAMOND_ORE: (185, 242, 255),  # Diamant
            TileType.COAL_ORE: (36, 36, 36),  # Charbon
            TileType.APPLE_TREE: (34, 139, 34),  # Vert pomme
            TileType.BERRY_BUSH: (128, 0, 128)  # Violet baies
        }
        return color_map.get(tile_type, COLORS["BLACK"])

    def save_game(self, slot_number=0):
        """Sauvegarde la partie"""
        if self.player is None:
            return False
            
        return self.save_system.save_game(
            slot_number, 
            self.player, 
            self.world_map, 
            self.enemies, 
            self.total_playtime
        )

    def load_game(self, slot_number=0):
        """Charge une partie"""
        game_data = self.save_system.load_game(slot_number)
        
        if not game_data:
            return False
            
        # Restaurer l'état du jeu
        self.world_map = game_data["world_map"]
        self.player = Player(game_data["player"]["x"], game_data["player"]["y"])
        self.player.health = game_data["player"]["health"]
        self.player.inventory = game_data["player"]["inventory"]
        self.total_playtime = game_data["playtime"]
        
        # Réinitialiser les composants
        self.camera = Camera(self.screen.get_width(), self.screen.get_height())
        self.hud = HUD(self.font)
        
        # Restaurer les ennemis
        self.enemies = []
        for enemy_data in game_data["enemies"]:
            enemy = Enemy(enemy_data["x"], enemy_data["y"])
            enemy.health = enemy_data["health"]
            self.enemies.append(enemy)
        
        self.game_start_time = time.time()
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
            # Mettre à jour le joueur
            keys = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            
            # Mise à jour du joueur
            dx, dy = self.player.update(keys, dt, self.menu.controls)
            
            # Appliquer le mouvement au joueur
            if dx != 0 or dy != 0:
                self.player.move(dx, dy, dt, self.world_map)
            
            # Vérifier si le joueur est mort
            if self.player.is_dead():
                dropped_inventory = self.player.die()
                if dropped_inventory:
                    self.dropped_inventories.append(dropped_inventory)
            
            # Gestion des clics de souris
            if mouse_buttons[0]:  # Clic gauche
                # Vérifier d'abord s'il y a un inventaire déposé à récupérer
                if not self._try_pickup_dropped_inventory(mouse_pos):
                    # Sinon, gestion normale
                    self.player.handle_mouse_click(mouse_pos, self.world_map, 
                                                 self.camera.x, self.camera.y, self.items)
            
            # Mise à jour des ennemis
            for enemy in self.enemies:
                enemy.update(self.player, self.world_map, dt)
            
            # Mise à jour de la caméra
            self.camera.follow_player(self.player)
            
            # Gestion du timer du message de sauvegarde
            if hasattr(self, 'show_save_message') and self.show_save_message:
                if hasattr(self, 'save_message_timer') and self.save_message_timer > 0:
                    self.save_message_timer -= dt
                    if self.save_message_timer <= 0:
                        self.show_save_message = False

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
        # Utiliser la taille actuelle de l'écran
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Calculer les tiles visibles
        start_x = max(0, int(self.camera.x // TILE_SIZE))
        end_x = min(MAP_WIDTH, int((self.camera.x + screen_width) // TILE_SIZE) + 1)
        start_y = max(0, int(self.camera.y // TILE_SIZE))
        end_y = min(MAP_HEIGHT, int((self.camera.y + screen_height) // TILE_SIZE) + 1)
        
        # Dessiner les tiles visibles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile_type = self.world_map[y][x]
                color = self.get_tile_color(tile_type)
                
                screen_x = x * TILE_SIZE - self.camera.x
                screen_y = y * TILE_SIZE - self.camera.y
                
                pygame.draw.rect(self.screen, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(self.screen, COLORS["BLACK"], (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 1)
        
        # Dessiner le joueur
        player_screen_x = self.player.x - self.camera.x
        player_screen_y = self.player.y - self.camera.y
        
        pygame.draw.circle(self.screen, COLORS["BLUE"], 
                         (int(player_screen_x + TILE_SIZE // 2), 
                          int(player_screen_y + TILE_SIZE // 2)), 
                         TILE_SIZE // 3)
        
        # Dessiner les ennemis
        for enemy in self.enemies:
            enemy_screen_x = enemy.x - self.camera.x
            enemy_screen_y = enemy.y - self.camera.y
            
            if (-TILE_SIZE <= enemy_screen_x <= screen_width and 
                -TILE_SIZE <= enemy_screen_y <= screen_height):
                pygame.draw.circle(self.screen, COLORS["RED"],
                                 (int(enemy_screen_x + TILE_SIZE // 2),
                                  int(enemy_screen_y + TILE_SIZE // 2)),
                                 TILE_SIZE // 4)
        
        # Dessiner le HUD
        self.hud.draw(self.screen, self.player, self)
        
        # Afficher le message de sauvegarde si nécessaire
        if hasattr(self, 'show_save_message') and self.show_save_message:
            self._draw_save_confirmation()
        
        # Dessiner l'interface d'inventaire
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
        if self.game_start_time and self.state == "playing":
            current_session = time.time() - self.game_start_time
            total_time = self.total_playtime + current_session
        else:
            total_time = self.total_playtime
        
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        seconds = int(total_time % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def _try_pickup_dropped_inventory(self, mouse_pos):
        """Essaie de récupérer un inventaire déposé"""
        world_x = mouse_pos[0] + self.camera.x
        world_y = mouse_pos[1] + self.camera.y
        
        for i, dropped_inv in enumerate(self.dropped_inventories):
            # Vérifier si le clic est sur l'inventaire déposé
            distance = ((world_x - dropped_inv.x)**2 + (world_y - dropped_inv.y)**2)**0.5
            if distance <= TILE_SIZE:
                # Récupérer l'inventaire
                print("🎒 Inventaire récupéré !")
                
                # Transférer tous les items vers le joueur
                for slot in dropped_inv.inventory.slots:
                    if slot:
                        remaining = self.player.inventory.add_item(slot.item, slot.quantity)
                        if remaining > 0:
                            print(f"⚠️ Impossible de récupérer {remaining} x {slot.item.name}")
                
                # Retirer l'inventaire déposé
                self.dropped_inventories.pop(i)
                return True
        
        return False
