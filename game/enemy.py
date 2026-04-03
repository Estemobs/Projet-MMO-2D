import math
import random
from .constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE
from .tiletype import TileType

class Enemy:
    # Loot table: list of (item_key, probability, min_qty, max_qty)
    LOOT_TABLE = [
        ("meat",     0.70, 1, 2),
        ("coal",     0.40, 1, 3),
        ("iron_ore", 0.15, 1, 2),
        ("stone",    0.30, 1, 3),
    ]
    # XP reward for killing this enemy
    XP_REWARD = 20

    def __init__(self, x, y, faction="hostile"):
        self.x = x
        self.y = y
        self.health = 50
        self.max_health = 50
        self.speed = 50
        self.damage = 10
        self.faction = faction
        self.last_attack_time = 0
        self.attack_cooldown = 1.0  # 1 seconde entre les attaques
        self.detection_range = 3  # tiles de portée de détection
        
        # Animation
        self.is_moving = False
        self.animation_time = 0
        self.animation_speed = 0.5  # Plus lent que le joueur

    def is_dead(self):
        """Returns True if this enemy has no health left."""
        return self.health <= 0
    
    def get_loot(self, items):
        """Returns a list of (Item, quantity) to drop on death."""
        drops = []
        for item_key, probability, min_qty, max_qty in self.LOOT_TABLE:
            if random.random() < probability and item_key in items:
                qty = random.randint(min_qty, max_qty)
                drops.append((items[item_key], qty))
        return drops

    def move_towards_player(self, player_x, player_y, dt, world_map):
        # Calculer la direction vers le joueur
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        self.is_moving = True
        self.animation_time += dt
        
        if distance > 0:
            # Normaliser la direction
            dx /= distance
            dy /= distance
            
            # Calculer la nouvelle position
            new_x = self.x + dx * self.speed * dt
            new_y = self.y + dy * self.speed * dt
            
            # Vérifier les limites et obstacles
            if 0 <= new_x < MAP_WIDTH * TILE_SIZE and 0 <= new_y < MAP_HEIGHT * TILE_SIZE:
                tile_x = int(new_x // TILE_SIZE)
                tile_y = int(new_y // TILE_SIZE)
                
                # Terrain praticable pour les ennemis
                walkable_tiles = [TileType.GRASS, TileType.DIRT, TileType.FOUNDATION]
                if world_map[tile_y][tile_x] in walkable_tiles:
                    self.x = new_x
                    self.y = new_y
    
    def attack_player(self, player, current_time):
        if current_time - self.last_attack_time >= self.attack_cooldown:
            player.health -= self.damage
            self.last_attack_time = current_time
            return True
        return False

    def update(self, player, world_map, dt):
        """Met à jour l'état de l'ennemi"""
        import time
        current_time = time.time()
        
        # Calculer la distance au joueur
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Si le joueur est dans la portée de détection
        if distance <= self.detection_range * TILE_SIZE:
            # Si assez proche pour attaquer (1 tile)
            if distance <= TILE_SIZE:
                self.attack_player(player, current_time)
            else:
                # Se déplacer vers le joueur
                self.move_towards_player(player.x, player.y, dt, world_map)
