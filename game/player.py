import random
import os
import sys

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from ui.inventory import Inventory
from .constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE
from .tiletype import TileType

class DroppedInventory:
    """Représente un inventaire déposé au sol"""
    def __init__(self, x, y, inventory):
        self.x = x
        self.y = y
        self.inventory = inventory
        self.size = TILE_SIZE

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 100
        self.health = 100
        self.max_health = 100
        self.faction = "player"
        self.build_mode = False
        self.selected_building = "foundation"
        self.inventory = Inventory(36)
        self.hunger = 100
        self.max_hunger = 100

    def move(self, dx, dy, dt, world_map):
        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt
        if 0 <= new_x < MAP_WIDTH * TILE_SIZE and 0 <= new_y < MAP_HEIGHT * TILE_SIZE:
            tile_x = int(new_x // TILE_SIZE)
            tile_y = int(new_y // TILE_SIZE)
            if world_map[tile_y][tile_x] == TileType.GRASS:
                self.x = new_x
                self.y = new_y

    def harvest_resource(self, world_map, mouse_pos, camera_x, camera_y, items):
        world_x = mouse_pos[0] + camera_x
        world_y = mouse_pos[1] + camera_y
        tile_x = int(world_x // TILE_SIZE)
        tile_y = int(world_y // TILE_SIZE)
        player_tile_x = int(self.x // TILE_SIZE)
        player_tile_y = int(self.y // TILE_SIZE)
        distance = ((tile_x - player_tile_x)**2 + (tile_y - player_tile_y)**2) ** 0.5
        if distance <= 2:
            if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
                tile_type = world_map[tile_y][tile_x]
                if tile_type == TileType.TREE:
                    self.inventory.add_item(items["wood"], 1)
                    world_map[tile_y][tile_x] = TileType.GRASS
                    return True
                elif tile_type == TileType.STONE:
                    self.inventory.add_item(items["stone"], 1)
                    world_map[tile_y][tile_x] = TileType.GRASS
                    return True
                elif tile_type == TileType.IRON_ORE:
                    self.inventory.add_item(items["iron_ore"], 1)
                    world_map[tile_y][tile_x] = TileType.GRASS
                    return True
                elif tile_type == TileType.GOLD_ORE:
                    self.inventory.add_item(items["gold_ore"], 1)
                    world_map[tile_y][tile_x] = TileType.GRASS
                    return True
                elif tile_type == TileType.DIAMOND_ORE:
                    self.inventory.add_item(items["diamond_ore"], 1)
                    world_map[tile_y][tile_x] = TileType.GRASS
                    return True
                elif tile_type == TileType.COAL_ORE:
                    self.inventory.add_item(items["coal"], 1)
                    world_map[tile_y][tile_x] = TileType.GRASS
                    return True
                elif tile_type == TileType.APPLE_TREE:
                    self.inventory.add_item(items["apple"], random.randint(1, 3))
                    self.inventory.add_item(items["wood"], 1)
                    world_map[tile_y][tile_x] = TileType.GRASS
                    return True
                elif tile_type == TileType.BERRY_BUSH:
                    self.inventory.add_item(items["berry"], random.randint(2, 5))
                    world_map[tile_y][tile_x] = TileType.GRASS
                    return True
        return False

    def build_structure(self, world_map, mouse_pos, camera_x, camera_y):
        world_x = mouse_pos[0] + camera_x
        world_y = mouse_pos[1] + camera_y
        tile_x = int(world_x // TILE_SIZE)
        tile_y = int(world_y // TILE_SIZE)
        player_tile_x = int(self.x // TILE_SIZE)
        player_tile_y = int(self.y // TILE_SIZE)
        distance = ((tile_x - player_tile_x)**2 + (tile_y - player_tile_y)**2) ** 0.5
        if distance <= 3:
            if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
                if world_map[tile_y][tile_x] == TileType.GRASS:
                    building_costs = {
                        "foundation": {"wood": 2, "stone": 1},
                        "wall": {"wood": 1, "stone": 2}
                    }
                    if self.selected_building in building_costs:
                        cost = building_costs[self.selected_building]
                        can_build = all(self.inventory.has_item(resource, amount) for resource, amount in cost.items())
                        if can_build:
                            for resource, amount in cost.items():
                                self.inventory.remove_item(resource, amount)
                            if self.selected_building == "foundation":
                                world_map[tile_y][tile_x] = TileType.FOUNDATION
                            elif self.selected_building == "wall":
                                world_map[tile_y][tile_x] = TileType.WALL
                            return True
        return False

    def eat_food(self, food_item, heal_amount):
        if self.inventory.has_item(food_item, 1):
            self.inventory.remove_item(food_item, 1)
            self.health = min(self.max_health, self.health + heal_amount)
            self.hunger = min(self.max_hunger, self.hunger + heal_amount // 2)
            return True
        return False

    def update(self, keys, dt, controls=None):
        """Met à jour l'état du joueur"""
        # Diminuer la faim au fil du temps (beaucoup plus lentement)
        self.hunger = max(0, self.hunger - 0.3 * dt)  # Encore plus lent
        
        # Si le joueur a faim, perdre de la santé (plus lentement)
        if self.hunger <= 0:
            self.health = max(0, self.health - 1.5 * dt)  # Réduit encore plus
        
        # Régénération naturelle si le joueur n'a pas faim
        elif self.hunger > 30 and self.health < self.max_health:
            self.health = min(self.max_health, self.health + 3 * dt)  # Un peu plus de régénération
        
        # Gestion du déplacement avec les contrôles configurés
        if controls is None:
            # Contrôles par défaut si aucun contrôle personnalisé n'est fourni
            import pygame
            controls = {
                "move_up": pygame.K_w,
                "move_down": pygame.K_s,
                "move_left": pygame.K_a,
                "move_right": pygame.K_d
            }
        
        dx = 0
        dy = 0
        
        if keys[controls["move_up"]]:
            dy -= 1
        if keys[controls["move_down"]]:
            dy += 1
        if keys[controls["move_left"]]:
            dx -= 1
        if keys[controls["move_right"]]:
            dx += 1
        
        # Normaliser le vecteur de déplacement si mouvement diagonal
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2)
            dy *= 0.707
            
        return dx, dy

    def handle_mouse_click(self, mouse_pos, world_map, camera_x, camera_y, items):
        """Gère les clics de souris du joueur"""
        if self.build_mode:
            # Mode construction
            return self.build_structure(world_map, mouse_pos, camera_x, camera_y)
        else:
            # Mode récolte
            self.harvest_resource(world_map, mouse_pos, camera_x, camera_y, items)
    
    def is_dead(self):
        """Vérifie si le joueur est mort"""
        return self.health <= 0
    
    def die(self):
        """Fait mourir le joueur et retourne son inventaire"""
        if self.health <= 0:
            # Sauvegarder l'inventaire à déposer
            dropped_inventory = DroppedInventory(self.x, self.y, self.inventory)
            
            # Respawn du joueur
            self.respawn()
            
            return dropped_inventory
        return None
    
    def respawn(self):
        """Fait respawn le joueur"""
        # Position de spawn (centre de la carte)
        self.x = MAP_WIDTH * TILE_SIZE // 2
        self.y = MAP_HEIGHT * TILE_SIZE // 2
        
        # Restaurer les stats
        self.health = self.max_health
        self.hunger = self.max_hunger
        
        # Nouvel inventaire vide
        self.inventory = Inventory(36)
        
        print("💀 Vous êtes mort ! Vous avez respawn au centre de la carte.")
        print("🎒 Votre inventaire a été déposé à l'endroit de votre mort.")
