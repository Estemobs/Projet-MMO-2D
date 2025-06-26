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

from ui.inventory import Item, ItemStack, Inventory, CraftingRecipe, InventoryUI
from ui.menu import Menu
from ui.pause_menu import PauseMenu
from .constants import *
from .tiletype import TileType
from .player import Player
from .enemy import Enemy
from .world import WorldGenerator
from .camera import Camera
from .sprite_manager import get_sprite_manager
from .hud import HUD
from .factions import Faction
from .building import Building

# Initialisation de Pygame
pygame.init()

class Game:
    def __init__(self):
        # État du jeu
        self.state = "menu"  # "menu", "playing", "paused"
        
        # Initialisation basique
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("MMO 2D - Jeu de survie")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        # Sprite manager
        self.sprite_manager = get_sprite_manager()
        
        # Menu
        self.menu = Menu(self.screen, self.font)
        self.pause_menu = PauseMenu(self.screen, self.font)
        
        # Composants du jeu (initialisés quand on commence une partie)
        self.world_map = None
        self.player = None
        self.camera = None
        self.hud = None
        self.enemies = []
        
        # Système d'items et crafting
        self.items = self.create_items()
        self.recipes = self.create_recipes()
        self.inventory_ui = InventoryUI(self.screen, self.font)
        
        # Système de temps de jeu
        self.game_start_time = None
        self.total_playtime = 0  # en secondes
        
        self.running = True
    
    def create_items(self):
        """Crée tous les items du jeu"""
        items = {
            # Ressources de base
            "wood": Item("Bois", "resource", "Matériau de base pour la construction", 99, BROWN),
            "stone": Item("Pierre", "resource", "Matériau solide pour les constructions", 99, GRAY),
            "iron_ore": Item("Minerai de fer", "resource", "Utilisé pour créer des outils", 99, DARK_GRAY),
            "gold_ore": Item("Minerai d'or", "resource", "Précieux minerai doré", 99, (255, 215, 0)),
            "diamond_ore": Item("Minerai de diamant", "resource", "Le plus précieux des minerais", 99, (185, 242, 255)),
            "coal": Item("Charbon", "resource", "Combustible et matériau", 99, (36, 36, 36)),
            
            # Nourriture
            "apple": Item("Pomme", "food", "Restaure 10 points de vie", 10, RED),
            "berry": Item("Baie", "food", "Restaure 5 points de vie", 20, PURPLE),
            "bread": Item("Pain", "food", "Restaure 20 points de vie", 5, (222, 184, 135)),
            
            # Matériaux raffinés
            "iron_ingot": Item("Lingot de fer", "material", "Fer purifié", 99, (169, 169, 169)),
            "gold_ingot": Item("Lingot d'or", "material", "Or purifié", 99, (255, 215, 0)),
            "diamond": Item("Diamant", "material", "Diamant taillé", 99, (185, 242, 255)),
            
            # Outils
            "wooden_sword": Item("Épée en bois", "weapon", "Arme basique", 1, BROWN),
            "iron_sword": Item("Épée en fer", "weapon", "Arme solide", 1, DARK_GRAY),
            "gold_sword": Item("Épée en or", "weapon", "Arme précieuse", 1, (255, 215, 0)),
            "diamond_sword": Item("Épée en diamant", "weapon", "L'arme ultime", 1, (185, 242, 255)),
            
            "wooden_pickaxe": Item("Pioche en bois", "tool", "Outil de minage basique", 1, BROWN),
            "iron_pickaxe": Item("Pioche en fer", "tool", "Outil de minage avancé", 1, DARK_GRAY),
            
            # Armures
            "leather_armor": Item("Armure en cuir", "armor", "Protection basique", 1, (139, 69, 19)),
            "iron_armor": Item("Armure en fer", "armor", "Protection solide", 1, DARK_GRAY),
        }
        return items
    
    def create_recipes(self):
        """Crée toutes les recettes de crafting"""
        recipes = [
            # Raffinement
            CraftingRecipe("Lingot de fer", {"iron_ore": 2, "coal": 1}, self.items["iron_ingot"], 1),
            CraftingRecipe("Lingot d'or", {"gold_ore": 2, "coal": 1}, self.items["gold_ingot"], 1),
            CraftingRecipe("Diamant", {"diamond_ore": 1}, self.items["diamond"], 1),
            
            # Nourriture
            CraftingRecipe("Pain", {"wood": 2}, self.items["bread"], 1),  # Simplifié
            
            # Armes
            CraftingRecipe("Épée en bois", {"wood": 3, "stone": 1}, self.items["wooden_sword"], 1),
            CraftingRecipe("Épée en fer", {"iron_ingot": 2, "wood": 1}, self.items["iron_sword"], 1),
            CraftingRecipe("Épée en or", {"gold_ingot": 2, "wood": 1}, self.items["gold_sword"], 1),
            CraftingRecipe("Épée en diamant", {"diamond": 2, "wood": 1}, self.items["diamond_sword"], 1),
            
            # Outils
            CraftingRecipe("Pioche en bois", {"wood": 3, "stone": 2}, self.items["wooden_pickaxe"], 1),
            CraftingRecipe("Pioche en fer", {"iron_ingot": 3, "wood": 2}, self.items["iron_pickaxe"], 1),
            
            # Armures
            CraftingRecipe("Armure en cuir", {"wood": 8}, self.items["leather_armor"], 1),  # Simplifié
            CraftingRecipe("Armure en fer", {"iron_ingot": 8}, self.items["iron_armor"], 1),
        ]
        return recipes
    
    def init_game(self):
        """Initialise une nouvelle partie"""
        self.world_map = WorldGenerator.generate_map()
        self.player = Player(MAP_WIDTH * TILE_SIZE // 2, MAP_HEIGHT * TILE_SIZE // 2)
        self.camera = Camera()
        self.hud = HUD(self.font)
        
        # Initialiser le temps de jeu
        self.game_start_time = time.time()
        self.total_playtime = 0
        
        # Générer quelques ennemis
        self.enemies = []
        for _ in range(5):
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
        
        # Donner quelques items de départ au joueur
        self.player.inventory.add_item(self.items["wood"], 10)
        self.player.inventory.add_item(self.items["stone"], 5)
        self.player.inventory.add_item(self.items["apple"], 3)
        
        self.state = "playing"
    
    def get_tile_color(self, tile_type):
        color_map = {
            TileType.GRASS: GREEN,
            TileType.TREE: BROWN,
            TileType.STONE: GRAY,
            TileType.IRON_ORE: DARK_GRAY,
            TileType.WALL: ORANGE,
            TileType.FOUNDATION: YELLOW,
            TileType.GOLD_ORE: (255, 215, 0),  # Or
            TileType.DIAMOND_ORE: (185, 242, 255),  # Diamant
            TileType.COAL_ORE: (36, 36, 36),  # Charbon
            TileType.APPLE_TREE: (34, 139, 34),  # Vert pomme
            TileType.BERRY_BUSH: (128, 0, 128),  # Violet baies
            TileType.DIRT: (139, 117, 78),  # Terre
            TileType.WATER: (64, 164, 223),  # Eau
        }
        return color_map.get(tile_type, GREEN)  # Fallback vers vert
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state == "menu":
                action = self.menu.handle_event(event)
                if action == "new_game":
                    self.init_game()
                elif action == "load_menu":
                    self.menu.current_menu = "load_menu"
                    self.menu.selected_save_slot = 0
                    self.menu.refresh_save_slots()
                elif action == "save_menu":
                    if self.state == "playing":
                        self.menu.current_menu = "save_menu"
                        self.menu.selected_save_slot = 0
                        self.menu.refresh_save_slots()
                    else:
                        print("❌ Aucune partie en cours à sauvegarder")
                elif action == "options":
                    self.menu.current_menu = "options"
                    self.menu.selected_button = 0
                elif action == "quit":
                    self.running = False
                elif action and action.startswith("load_slot_"):
                    slot_number = int(action.split("_")[-1])
                    self.load_game_from_slot(slot_number)
                elif action and action.startswith("save_slot_"):
                    slot_number = int(action.split("_")[-1])
                    self.save_game_to_slot(slot_number)
            
            elif self.state == "playing":
                # Gestion du menu de pause en priorité
                if self.pause_menu.visible:
                    pause_action = self.pause_menu.handle_event(event)
                    if pause_action == "resume":
                        self.pause_menu.hide()
                    elif pause_action == "save":
                        self.save_game()
                        print("✅ Partie sauvegardée!")
                    elif pause_action == "menu":
                        self.pause_menu.hide()
                        self.state = "menu"
                        self.menu.current_menu = "main"
                        self.menu.selected_button = 0
                    elif pause_action == "quit":
                        self.running = False
                    continue  # Ne pas traiter d'autres événements si le menu pause est ouvert
                
                # Gestion de l'inventaire
                self.inventory_ui.handle_event(event, self.player.inventory, self.recipes)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Ouvrir le menu de pause au lieu de quitter directement
                        self.pause_menu.show()
                    elif event.key == pygame.K_i:
                        self.inventory_ui.toggle_visibility()
                    elif event.key == pygame.K_b:
                        self.player.build_mode = not self.player.build_mode
                        print(f"Mode construction: {'Activé' if self.player.build_mode else 'Désactivé'}")
                    elif event.key == pygame.K_1:
                        self.player.selected_building = "foundation"
                        print("Structure sélectionnée: Fondation")
                    elif event.key == pygame.K_2:
                        self.player.selected_building = "wall"
                        print("Structure sélectionnée: Mur")
                    elif event.key == pygame.K_F5:  # Sauvegarde rapide
                        self.save_game()
                    elif event.key == pygame.K_h:  # Manger de la nourriture
                        if self.player.eat_food("apple", 10):
                            print("Pomme consommée! +10 santé")
                        elif self.player.eat_food("berry", 5):
                            print("Baie consommée! +5 santé")
                        elif self.player.eat_food("bread", 20):
                            print("Pain consommé! +20 santé")
                
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.inventory_ui.visible and not self.pause_menu.visible:
                    if event.button == 1:  # Clic gauche
                        mouse_pos = pygame.mouse.get_pos()
                        if self.player.build_mode:
                            if self.player.build_structure(self.world_map, mouse_pos, self.camera.x, self.camera.y):
                                print(f"Structure {self.player.selected_building} construite!")
                        else:
                            if self.player.harvest_resource(self.world_map, mouse_pos, self.camera.x, self.camera.y, self.items):
                                print("Ressource récoltée!")
    
    def update(self, dt):
        if self.state != "playing":
            return
        
        # Ne pas mettre à jour le jeu si le menu de pause est ouvert
        if self.pause_menu.visible:
            return
        
        # Gestion des inputs du clavier
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        
        # Normaliser le mouvement diagonal
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707
        
        # Déplacer le joueur
        self.player.move(dx, dy, dt, self.world_map)
        
        # Mettre à jour la caméra
        self.camera.update(self.player.x, self.player.y)
        
        # Mettre à jour les ennemis
        current_time = pygame.time.get_ticks() / 1000.0
        for enemy in self.enemies:
            # Calculer la distance au joueur
            distance_to_player = math.sqrt((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)
            
            if distance_to_player <= enemy.detection_range * TILE_SIZE:
                # Si assez proche pour attaquer
                if distance_to_player <= TILE_SIZE:
                    if enemy.attack_player(self.player, current_time):
                        print(f"Le joueur a subi {enemy.damage} dégâts!")
                        if self.player.health <= 0:
                            print("Game Over!")
                            self.state = "menu"
                            self.menu.current_menu = "main"
                else:
                    # Se déplacer vers le joueur
                    enemy.move_towards_player(self.player.x, self.player.y, dt, self.world_map)
        
        # Mettre à jour le temps de jeu
        self.update_playtime()
    
    def draw(self):
        if self.state == "menu":
            self.menu.draw()
        elif self.state == "playing":
            self.screen.fill(BLACK)
            
            # Calculer les tiles visibles
            start_x = max(0, int(self.camera.x // TILE_SIZE))
            end_x = min(MAP_WIDTH, int((self.camera.x + WINDOW_WIDTH) // TILE_SIZE) + 1)
            start_y = max(0, int(self.camera.y // TILE_SIZE))
            end_y = min(MAP_HEIGHT, int((self.camera.y + WINDOW_HEIGHT) // TILE_SIZE) + 1)
            
            # Dessiner les tiles visibles
            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    tile_type = self.world_map[y][x]
                    color = self.get_tile_color(tile_type)
                    
                    screen_x = x * TILE_SIZE - self.camera.x
                    screen_y = y * TILE_SIZE - self.camera.y
                    
                    pygame.draw.rect(self.screen, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                    
                    # Ajouter des bordures pour mieux voir les tiles
                    pygame.draw.rect(self.screen, BLACK, (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 1)
            
            # Dessiner le joueur avec sprite animé (plus gros)
            player_screen_x = self.player.x - self.camera.x - 8  # Décaler pour centrer le sprite 48x48
            player_screen_y = self.player.y - self.camera.y - 8
            
            # Utiliser le sprite animé
            current_sprite = self.player.get_current_sprite()
            if not self.sprite_manager.draw_entity(self.screen, current_sprite, int(player_screen_x), int(player_screen_y)):
                # Fallback sur cercle si sprite manquant
                pygame.draw.circle(self.screen, BLUE, 
                                 (int(self.player.x - self.camera.x + TILE_SIZE // 2), 
                                  int(self.player.y - self.camera.y + TILE_SIZE // 2)), 
                                 TILE_SIZE // 3)
            
            # Dessiner les ennemis avec sprites plus gros
            for enemy in self.enemies:
                enemy_screen_x = enemy.x - self.camera.x - 8  # Décaler pour centrer le sprite 48x48
                enemy_screen_y = enemy.y - self.camera.y - 8
                
                # Ne dessiner que les ennemis visibles
                if (-TILE_SIZE <= enemy_screen_x <= WINDOW_WIDTH and 
                    -TILE_SIZE <= enemy_screen_y <= WINDOW_HEIGHT):
                    
                    # Essayer d'utiliser le sprite, sinon fallback sur cercle
                    if not self.sprite_manager.draw_entity(self.screen, "enemy", int(enemy_screen_x), int(enemy_screen_y)):
                        pygame.draw.circle(self.screen, RED,
                                         (int(enemy.x - self.camera.x + TILE_SIZE // 2),
                                          int(enemy.y - self.camera.y + TILE_SIZE // 2)),
                                         TILE_SIZE // 4)
            
            # Dessiner le HUD
            self.hud.draw(self.screen, self.player, self)
            
            # Dessiner l'interface d'inventaire
            self.inventory_ui.draw(self.player.inventory, self.recipes)
            
            # Dessiner le menu de pause par-dessus tout
            self.pause_menu.draw()
            
            # Instructions
            if not self.inventory_ui.visible:
                instructions = [
                    "WASD ou flèches: Se déplacer",
                    "Clic gauche: Récolter les ressources ou construire", 
                    "B: Activer/désactiver le mode construction",
                    "1: Sélectionner fondation, 2: Sélectionner mur",
                    "I: Ouvrir inventaire, H: Manger nourriture",
                    "F5: Sauvegarder, Échap: Menu principal"
                ]
                
                for i, instruction in enumerate(instructions):
                    text = self.font.render(instruction, True, WHITE)
                    self.screen.blit(text, (10, WINDOW_HEIGHT - 120 + i * 20))
            
            pygame.display.flip()
        else:
            pygame.display.flip()
    
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Delta time en secondes
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
    
    def save_game(self, filename="savegame.json"):
        """Sauvegarde la partie actuelle"""
        if self.state != "playing":
            return
        
        try:
            import json
            # Préparer les données de sauvegarde
            save_data = {
                "world_map": [[tile.value for tile in row] for row in self.world_map],
                "player": {
                    "x": self.player.x,
                    "y": self.player.y,
                    "health": self.player.health,
                    "inventory": []
                },
                "enemies": []
            }
            
            # Sauvegarder l'inventaire
            for slot in self.player.inventory.slots:
                if slot:
                    save_data["player"]["inventory"].append({
                        "name": slot.item.name,
                        "quantity": slot.quantity
                    })
            
            # Sauvegarder les ennemis
            for enemy in self.enemies:
                save_data["enemies"].append({
                    "x": enemy.x,
                    "y": enemy.y,
                    "health": enemy.health
                })
            
            # Écrire le fichier de sauvegarde
            with open(filename, "w") as f:
                json.dump(save_data, f, indent=2)
            
            print("✅ Partie sauvegardée!")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
    
    def load_game(self, filename="savegame.json"):
        """Charge une partie sauvegardée"""
        try:
            import json
            import os
            
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    save_data = json.load(f)
                
                # Recréer le monde
                self.world_map = [[TileType(tile) for tile in row] for row in save_data["world_map"]]
                
                # Recréer le joueur
                player_data = save_data["player"]
                self.player = Player(player_data["x"], player_data["y"])
                self.player.health = player_data["health"]
                
                # Restaurer l'inventaire
                for item_data in player_data["inventory"]:
                    item_name = item_data["name"]
                    quantity = item_data["quantity"]
                    if item_name in self.items:
                        self.player.inventory.add_item(self.items[item_name], quantity)
                
                # Recréer les autres composants
                self.camera = Camera()
                self.hud = HUD(self.font)
                self.enemies = []
                
                # Recréer les ennemis
                for enemy_data in save_data["enemies"]:
                    enemy = Enemy(enemy_data["x"], enemy_data["y"])
                    enemy.health = enemy_data["health"]
                    self.enemies.append(enemy)
                
                self.state = "playing"
                print("✅ Partie chargée avec succès!")
            else:
                print("❌ Aucune sauvegarde trouvée")
                # Créer une nouvelle partie à la place
                self.init_game()
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            # Créer une nouvelle partie en cas d'erreur
            self.init_game()
    
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
    
    def update_playtime(self):
        """Met à jour le temps de jeu total"""
        if self.game_start_time and self.state == "playing":
            current_session = time.time() - self.game_start_time
            self.total_playtime += current_session
            self.game_start_time = time.time()
    
    def load_game_from_slot(self, slot_number):
        """Charge un jeu depuis un slot spécifique"""
        filename = f"savegame_slot_{slot_number}.json"
        self.load_game(filename)
    
    def save_game_to_slot(self, slot_number):
        """Sauvegarde le jeu dans un slot spécifique"""
        filename = f"savegame_slot_{slot_number}.json"
        self.save_game(filename)
