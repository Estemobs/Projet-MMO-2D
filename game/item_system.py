"""
Système d'items dispersés pour le jeu MMO 2D (style Surviv.io)
"""

import pygame
import random
import math
import time

class DroppedItem:
    """Item qui tombe et rebondit au sol"""
    def __init__(self, x, y, item, quantity=1):
        self.x = x
        self.y = y
        self.item = item
        self.quantity = quantity
        
        # Physique de dispersion (plus forte pour ressembler à Surviv.io)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(150, 300)  # Vitesse beaucoup plus élevée
        self.velocity_x = math.cos(angle) * speed
        self.velocity_y = math.sin(angle) * speed
        
        # Propriétés physiques
        self.friction = 0.85  # Friction plus faible pour aller plus loin
        self.bounce_factor = 0.8  # Rebond plus énergique
        self.lifetime = 300.0  # 5 minutes avant disparition
        self.pickup_radius = 32  # Rayon plus grand pour pickup
        
        # Animation
        self.spawn_time = time.time()
        self.bounce_height = 0
        self.bounce_speed = 0
        
    def update(self, dt, world_map):
        """Met à jour la physique de l'item"""
        from .constants import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT
        from .tiletype import TileType
        
        # Appliquer la vélocité
        new_x = self.x + self.velocity_x * dt
        new_y = self.y + self.velocity_y * dt
        
        # Vérifier les collisions avec le monde
        tile_x = int(new_x // TILE_SIZE)
        tile_y = int(new_y // TILE_SIZE)
        
        # Collision avec les bords du monde
        if new_x < 0 or new_x >= MAP_WIDTH * TILE_SIZE:
            self.velocity_x *= -self.bounce_factor
        else:
            self.x = new_x
            
        if new_y < 0 or new_y >= MAP_HEIGHT * TILE_SIZE:
            self.velocity_y *= -self.bounce_factor
        else:
            self.y = new_y
        
        # Collision avec les obstacles (arbres, pierres, etc.)
        if (0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT and 
            world_map[tile_y][tile_x] in [TileType.TREE, TileType.STONE, TileType.WALL]):
            
            # Rebondir dans une direction aléatoire
            bounce_angle = random.uniform(0, 2 * math.pi)
            bounce_speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2) * self.bounce_factor
            self.velocity_x = math.cos(bounce_angle) * bounce_speed
            self.velocity_y = math.sin(bounce_angle) * bounce_speed
        
        # Appliquer la friction
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        
        # Animation de rebond
        self.bounce_height = max(0, self.bounce_height + self.bounce_speed * dt)
        self.bounce_speed -= 300 * dt  # Gravité
        
        if self.bounce_height <= 0:
            self.bounce_height = 0
            if abs(self.velocity_x) + abs(self.velocity_y) > 20:
                self.bounce_speed = 80  # Nouveau rebond
        
        # Diminuer la durée de vie
        self.lifetime -= dt
        
    def can_pickup(self, player_x, player_y):
        """Vérifie si le joueur peut ramasser l'item"""
        distance = math.sqrt((self.x - player_x)**2 + (self.y - player_y)**2)
        return distance <= self.pickup_radius and abs(self.velocity_x) + abs(self.velocity_y) < 10
    
    def is_expired(self):
        """Vérifie si l'item doit disparaître"""
        return self.lifetime <= 0
    
    def draw(self, screen, camera, sprite_manager):
        """Dessine l'item sur l'écran"""
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y - self.bounce_height
        
        # Vérifier si l'item est visible
        if (-32 <= screen_x <= screen.get_width() and 
            -32 <= screen_y <= screen.get_height()):
            
            # Essayer d'utiliser un sprite
            if not sprite_manager.draw_item(screen, self.item.name, int(screen_x), int(screen_y)):
                # Fallback: cercle coloré
                color = self._get_item_color()
                pygame.draw.circle(screen, color, (int(screen_x + 16), int(screen_y + 16)), 8)
            
            # Afficher la quantité si > 1
            if self.quantity > 1:
                font = pygame.font.Font(None, 16)
                text = font.render(str(self.quantity), True, (255, 255, 255))
                screen.blit(text, (screen_x + 20, screen_y))
            
            # Effet de brillance si récemment droppé
            age = time.time() - self.spawn_time
            if age < 2.0:  # 2 secondes d'effet
                alpha = int(255 * (1 - age / 2.0))
                glow_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (255, 255, 0, alpha), (16, 16), 16)
                screen.blit(glow_surface, (screen_x, screen_y))
    
    def _get_item_color(self):
        """Retourne une couleur basée sur le type d'item"""
        item_colors = {
            "wood": (139, 69, 19),
            "stone": (128, 128, 128),
            "iron_ore": (169, 169, 169),
            "gold_ore": (255, 215, 0),
            "diamond_ore": (185, 242, 255),
            "coal": (64, 64, 64),
            "apple": (255, 0, 0),
            "berry": (128, 0, 128),
        }
        return item_colors.get(self.item.name, (255, 255, 255))


class ItemManager:
    """Gestionnaire des items dispersés dans le monde"""
    def __init__(self):
        self.dropped_items = []
    
    def drop_item(self, x, y, item, quantity=1):
        """Droppe un item à une position avec dispersion"""
        dropped = DroppedItem(x, y, item, quantity)
        self.dropped_items.append(dropped)
    
    def drop_multiple_items(self, x, y, items_list):
        """Droppe plusieurs items avec dispersion"""
        for item, quantity in items_list:
            for _ in range(quantity):
                self.drop_item(x, y, item, 1)
    
    def update(self, dt, world_map):
        """Met à jour tous les items droppés"""
        # Mettre à jour la physique
        for item in self.dropped_items[:]:
            item.update(dt, world_map)
            
            # Supprimer les items expirés
            if item.is_expired():
                self.dropped_items.remove(item)
    
    def try_pickup(self, player_x, player_y, player_inventory):
        """Essaie de ramasser des items près du joueur"""
        picked_items = []
        
        for item in self.dropped_items[:]:
            if item.can_pickup(player_x, player_y):
                # Essayer d'ajouter à l'inventaire
                remaining = player_inventory.add_item(item.item, item.quantity)
                
                if remaining == 0:
                    # Item complètement ramassé
                    self.dropped_items.remove(item)
                    picked_items.append(item.item.name)
                elif remaining < item.quantity:
                    # Item partiellement ramassé
                    item.quantity = remaining
                    picked_items.append(f"{item.quantity - remaining}x {item.item.name}")
        
        return picked_items
    
    def draw_all(self, screen, camera, sprite_manager):
        """Dessine tous les items droppés"""
        for item in self.dropped_items:
            item.draw(screen, camera, sprite_manager)
    
    def clear_all(self):
        """Supprime tous les items droppés"""
        self.dropped_items.clear()
