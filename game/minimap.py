"""
Système de minimap pour le jeu MMO 2D
"""

import pygame
from .constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE

class MiniMap:
    def __init__(self, screen_width, screen_height):
        self.width = 200
        self.height = 150
        self.x = 10
        self.y = 10
        self.scale = min(self.width / (MAP_WIDTH * TILE_SIZE), self.height / (MAP_HEIGHT * TILE_SIZE))
        
        # Couleurs pour la minimap
        self.colors = {
            'grass': (34, 139, 34),
            'tree': (101, 67, 33),
            'stone': (128, 128, 128),
            'iron_ore': (139, 69, 19),
            'gold_ore': (255, 215, 0),
            'diamond_ore': (185, 242, 255),
            'coal_ore': (64, 64, 64),
            'fruit_tree': (255, 0, 0),
            'foundation': (160, 160, 160),
            'wall': (139, 69, 19),
            'player': (0, 100, 255),
            'enemy': (255, 0, 0),
            'death_marker': (255, 255, 255)
        }
        
        # Cache de la minimap du monde
        self.world_surface = None
        self.death_markers = []  # Liste des marqueurs de mort
    
    def generate_world_minimap(self, world_map):
        """Génère la minimap du monde (à faire une seule fois)"""
        self.world_surface = pygame.Surface((self.width, self.height))
        
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                # Convertir les coordonnées du monde en coordonnées minimap
                mini_x = int(x * TILE_SIZE * self.scale)
                mini_y = int(y * TILE_SIZE * self.scale)
                
                # Obtenir la couleur de la tile
                tile_type = world_map[y][x]
                color = self.get_tile_color(tile_type)
                
                # Dessiner un pixel ou petit rectangle sur la minimap
                size = max(1, int(TILE_SIZE * self.scale))
                pygame.draw.rect(self.world_surface, color, (mini_x, mini_y, size, size))
    
    def get_tile_color(self, tile_type):
        """Convertit un type de tile en couleur pour la minimap"""
        from .tiletype import TileType
        
        tile_colors = {
            TileType.GRASS: self.colors['grass'],
            TileType.TREE: self.colors['tree'],
            TileType.STONE: self.colors['stone'],
            TileType.IRON_ORE: self.colors['iron_ore'],
            TileType.GOLD_ORE: self.colors['gold_ore'],
            TileType.DIAMOND_ORE: self.colors['diamond_ore'],
            TileType.COAL_ORE: self.colors['coal_ore'],
            TileType.FRUIT_TREE: self.colors['fruit_tree'],
            TileType.FOUNDATION: self.colors['foundation'],
            TileType.WALL: self.colors['wall'],
        }
        
        return tile_colors.get(tile_type, self.colors['grass'])
    
    def add_death_marker(self, world_x, world_y):
        """Ajoute un marqueur de mort à la minimap"""
        mini_x = int(world_x * self.scale)
        mini_y = int(world_y * self.scale)
        self.death_markers.append((mini_x, mini_y))
        print(f"💀 Marqueur de mort ajouté à la minimap ({mini_x}, {mini_y})")
    
    def clear_death_markers(self):
        """Efface tous les marqueurs de mort"""
        self.death_markers.clear()
    
    def world_to_minimap(self, world_x, world_y):
        """Convertit des coordonnées monde en coordonnées minimap"""
        mini_x = int(world_x * self.scale)
        mini_y = int(world_y * self.scale)
        return mini_x, mini_y
    
    def draw(self, screen, player, enemies=None, camera=None):
        """Dessine la minimap"""
        # Fond de la minimap
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)
        
        # Dessiner le monde si disponible
        if self.world_surface:
            screen.blit(self.world_surface, (self.x, self.y))
        
        # Dessiner les marqueurs de mort
        for marker_x, marker_y in self.death_markers:
            pygame.draw.circle(screen, self.colors['death_marker'], 
                             (self.x + marker_x, self.y + marker_y), 3)
            # Ajouter une croix
            pygame.draw.line(screen, (255, 0, 0), 
                           (self.x + marker_x - 2, self.y + marker_y - 2),
                           (self.x + marker_x + 2, self.y + marker_y + 2), 2)
            pygame.draw.line(screen, (255, 0, 0), 
                           (self.x + marker_x + 2, self.y + marker_y - 2),
                           (self.x + marker_x - 2, self.y + marker_y + 2), 2)
        
        # Dessiner les ennemis
        if enemies:
            for enemy in enemies:
                enemy_mini_x, enemy_mini_y = self.world_to_minimap(enemy.x, enemy.y)
                pygame.draw.circle(screen, self.colors['enemy'], 
                                 (self.x + enemy_mini_x, self.y + enemy_mini_y), 2)
        
        # Dessiner le joueur
        if player:
            player_mini_x, player_mini_y = self.world_to_minimap(player.x, player.y)
            pygame.draw.circle(screen, self.colors['player'], 
                             (self.x + player_mini_x, self.y + player_mini_y), 3)
        
        # Dessiner la zone visible (caméra)
        if camera:
            # Calculer la zone visible sur la minimap
            camera_mini_x = int(camera.x * self.scale)
            camera_mini_y = int(camera.y * self.scale)
            camera_mini_w = int(camera.screen_width * self.scale)
            camera_mini_h = int(camera.screen_height * self.scale)
            
            # Dessiner le rectangle de la caméra
            pygame.draw.rect(screen, (255, 255, 0), 
                           (self.x + camera_mini_x, self.y + camera_mini_y, 
                            camera_mini_w, camera_mini_h), 1)
        
        # Titre de la minimap
        font = pygame.font.Font(None, 16)
        title = font.render("MiniMap", True, (255, 255, 255))
        screen.blit(title, (self.x + 5, self.y - 20))
