"""
Système de minimap pour le jeu MMO 2D
"""

import pygame
from .constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE

class MiniMap:
    def __init__(self, screen_width, screen_height):
        self.width = 280  # Beaucoup plus grande
        self.height = 200  # Plus haute aussi
        # Position dans le coin en haut à droite avec petite marge
        self.x = screen_width - self.width - 10  # Petite marge à droite
        self.y = 10  # Petite marge en haut
        self.screen_width = screen_width  # Garder la largeur pour les updates
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
            'apple_tree': (255, 0, 0),
            'berry_bush': (128, 0, 128),
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
            TileType.APPLE_TREE: self.colors['apple_tree'],
            TileType.BERRY_BUSH: self.colors['berry_bush'],
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
    
    def update_position(self, screen_width, screen_height):
        """Met à jour la position de la minimap selon la taille d'écran"""
        self.screen_width = screen_width
        self.x = screen_width - self.width  # Complètement collé à droite
        self.y = 0
    
    def draw(self, screen, player, enemies=None, camera=None, death_markers=None):
        """Dessine la minimap"""
        # Fond de la minimap avec une bordure pour remplir l'espace
        background_rect = pygame.Rect(self.x - 5, self.y, self.width + 5, self.height + 5)
        pygame.draw.rect(screen, (20, 20, 20), background_rect)  # Fond gris foncé
        
        # Fond de la minimap
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)
        
        # Dessiner le monde si disponible
        if self.world_surface:
            screen.blit(self.world_surface, (self.x, self.y))
        
        # Dessiner les marqueurs de mort passés en paramètre
        if death_markers:
            for marker in death_markers:
                marker_mini_x, marker_mini_y = self.world_to_minimap(marker.x, marker.y)
                
                # Dessiner un fond plus visible pour la tombe
                pygame.draw.circle(screen, (50, 50, 50), 
                                 (self.x + marker_mini_x, self.y + marker_mini_y), 6)
                pygame.draw.circle(screen, (200, 200, 200), 
                                 (self.x + marker_mini_x, self.y + marker_mini_y), 5)
                
                # Dessiner une tombe stylisée
                tomb_x = self.x + marker_mini_x
                tomb_y = self.y + marker_mini_y
                
                # Base de la tombe
                pygame.draw.rect(screen, (80, 80, 80), 
                               (tomb_x - 3, tomb_y + 2, 6, 2))
                
                # Pierre tombale
                pygame.draw.rect(screen, (120, 120, 120), 
                               (tomb_x - 2, tomb_y - 3, 4, 5))
                
                # Croix sur la tombe
                pygame.draw.line(screen, (255, 255, 255), 
                               (tomb_x, tomb_y - 2), (tomb_x, tomb_y + 1), 1)
                pygame.draw.line(screen, (255, 255, 255), 
                               (tomb_x - 1, tomb_y - 1), (tomb_x + 1, tomb_y - 1), 1)
                
                # Ajouter un effet de brillance
                pygame.draw.circle(screen, (255, 255, 0, 100), 
                                 (self.x + marker_mini_x, self.y + marker_mini_y), 8, 1)
        
        # Dessiner les marqueurs de mort stockés localement (rétro-compatibilité)
        for marker_x, marker_y in self.death_markers:
            # Dessiner un fond plus visible pour la tombe
            pygame.draw.circle(screen, (50, 50, 50), 
                             (self.x + marker_x, self.y + marker_y), 6)
            pygame.draw.circle(screen, (200, 200, 200), 
                             (self.x + marker_x, self.y + marker_y), 5)
            
            # Dessiner une tombe stylisée
            tomb_x = self.x + marker_x
            tomb_y = self.y + marker_y
            
            # Base de la tombe
            pygame.draw.rect(screen, (80, 80, 80), 
                           (tomb_x - 3, tomb_y + 2, 6, 2))
            
            # Pierre tombale
            pygame.draw.rect(screen, (120, 120, 120), 
                           (tomb_x - 2, tomb_y - 3, 4, 5))
            
            # Croix sur la tombe
            pygame.draw.line(screen, (255, 255, 255), 
                           (tomb_x, tomb_y - 2), (tomb_x, tomb_y + 1), 1)
            pygame.draw.line(screen, (255, 255, 255), 
                           (tomb_x - 1, tomb_y - 1), (tomb_x + 1, tomb_y - 1), 1)
            
            # Ajouter un effet de brillance
            pygame.draw.circle(screen, (255, 255, 0, 100), 
                             (self.x + marker_x, self.y + marker_y), 8, 1)
        
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
