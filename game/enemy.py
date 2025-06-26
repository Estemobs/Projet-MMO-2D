import pygame
import math
from .constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE
from .tiletype import TileType

class Enemy:
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
    
    def move_towards_player(self, player_x, player_y, dt, world_map):
        # Calculer la direction vers le joueur
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
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
                
                if world_map[tile_y][tile_x] in [TileType.GRASS, TileType.FOUNDATION]:
                    self.x = new_x
                    self.y = new_y
    
    def attack_player(self, player, current_time):
        if current_time - self.last_attack_time >= self.attack_cooldown:
            player.health -= self.damage
            self.last_attack_time = current_time
            return True
        return False
