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
            'dirt': (139, 117, 78),  # Terre
            'water': (64, 164, 223),  # Eau
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
            TileType.DIRT: self.colors['dirt'],
            TileType.WATER: self.colors['water'],
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
        self.x = screen_width - self.width - 10  # Petite marge à droite
        self.y = 10  # Petite marge en haut

    def update_screen_size(self, screen_width, screen_height):
        """Met à jour la taille d'écran de la minimap."""
        self.screen_width = screen_width
        self.x = screen_width - self.width - 10
        self.y = 10
    
    def draw(self, screen, player, enemies=None, camera=None, death_markers=None):
        """Dessine la minimap avec style amélioré."""
        import math
        
        # Ombre portée de la minimap
        shadow_surf = pygame.Surface((self.width + 12, self.height + 12), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 80), (0, 0, self.width + 12, self.height + 12), border_radius=8)
        screen.blit(shadow_surf, (self.x - 6, self.y - 4))

        # Fond semi-transparent
        bg_surf = pygame.Surface((self.width + 8, self.height + 8), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (10, 14, 28, 200), (0, 0, self.width + 8, self.height + 8), border_radius=8)
        screen.blit(bg_surf, (self.x - 4, self.y - 4))

        # Dessiner le monde si disponible
        if self.world_surface:
            # Masque arrondi pour la minimap
            mask_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            mask_surf.blit(self.world_surface, (0, 0))
            pygame.draw.rect(mask_surf, (0, 0, 0, 0), (0, 0, self.width, self.height), 0, border_radius=6)
            screen.blit(mask_surf, (self.x, self.y))

        # Bordure extérieure
        pygame.draw.rect(screen, (60, 80, 130), (self.x - 4, self.y - 4, self.width + 8, self.height + 8), 1, border_radius=8)

        # Dessiner les marqueurs de mort
        if death_markers:
            for marker in death_markers:
                marker_mini_x, marker_mini_y = self.world_to_minimap(marker.x, marker.y)
                mx = self.x + marker_mini_x
                my = self.y + marker_mini_y

                # Lueur pulsante
                glow_alpha = int(abs(math.sin(pygame.time.get_ticks() / 300)) * 60) + 40
                glow_surf = pygame.Surface((14, 14), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (255, 200, 80, glow_alpha), (7, 7), 7)
                screen.blit(glow_surf, (mx - 7, my - 7))

                # Tombe miniature
                pygame.draw.rect(screen, (80, 75, 70), (mx - 2, my - 2, 4, 5))
                pygame.draw.line(screen, (200, 195, 185), (mx, my - 1), (mx, my + 2), 1)
                pygame.draw.line(screen, (200, 195, 185), (mx - 1, my), (mx + 1, my), 1)

        # Dessiner les ennemis
        if enemies:
            for enemy in enemies:
                enemy_mini_x, enemy_mini_y = self.world_to_minimap(enemy.x, enemy.y)
                pygame.draw.circle(screen, (220, 60, 60),
                                 (self.x + enemy_mini_x, self.y + enemy_mini_y), 2)

        # Dessiner le joueur (point bleu brillant)
        if player:
            player_mini_x, player_mini_y = self.world_to_minimap(player.x, player.y)
            px = self.x + player_mini_x
            py = self.y + player_mini_y
            # Halo
            pygame.draw.circle(screen, (60, 120, 255), (px, py), 4)
            pygame.draw.circle(screen, (120, 180, 255), (px, py), 2)

        # Dessiner la zone visible (caméra)
        if camera:
            camera_mini_x = int(camera.x * self.scale)
            camera_mini_y = int(camera.y * self.scale)
            camera_mini_w = int(camera.screen_width * self.scale)
            camera_mini_h = int(camera.screen_height * self.scale)
            view_rect = pygame.Rect(
                self.x + camera_mini_x, self.y + camera_mini_y,
                camera_mini_w, camera_mini_h
            )
            pygame.draw.rect(screen, (255, 255, 100), view_rect, 1)

        # Titre de la minimap
        font = pygame.font.Font(None, 14)
        title = font.render("Carte", True, (140, 160, 200))
        screen.blit(title, (self.x + 6, self.y - 18))
