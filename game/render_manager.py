"""
Gestionnaire de rendu pour le jeu MMO 2D
"""

import pygame
from .constants import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, COLORS
from .tiletype import TileType
from .sprite_manager import get_sprite_manager

class RenderManager:
    def __init__(self, screen):
        self.screen = screen
        self.sprite_manager = get_sprite_manager()
        
    def get_tile_color(self, tile_type):
        """Retourne la couleur d'une tile (fallback si pas de sprite)"""
        tile_colors = {
            TileType.GRASS: COLORS["GREEN"],
            TileType.TREE: COLORS["BROWN"],
            TileType.STONE: COLORS["GRAY"],
            TileType.IRON_ORE: (139, 69, 19),
            TileType.GOLD_ORE: (255, 215, 0),
            TileType.DIAMOND_ORE: (185, 242, 255),
            TileType.COAL_ORE: (64, 64, 64),
            TileType.APPLE_TREE: COLORS["GREEN"],
            TileType.BERRY_BUSH: (128, 0, 128),
            TileType.FOUNDATION: (160, 160, 160),
            TileType.WALL: COLORS["BROWN"],
            TileType.DIRT: (139, 117, 78),  # Couleur terre
            TileType.WATER: (64, 164, 223),  # Couleur eau
        }
        return tile_colors.get(tile_type, COLORS["GREEN"])
    
    def get_tile_sprite_name(self, tile_type, x=0, y=0):
        """Retourne le nom du sprite pour une tile avec variantes consistantes"""
        
        # Utiliser la position pour avoir des sprites consistants
        seed = (x * 7 + y * 13) % 1000
        
        # Pour les types avec variantes, choisir de façon déterministe
        if tile_type == TileType.GRASS:
            # Un seul type d'herbe pour éviter la superposition
            return "grass_1"
        elif tile_type == TileType.DIRT:
            variant = (seed % 3) + 1
            return f"dirt_{variant}"
        elif tile_type == TileType.WATER:
            variant = (seed % 3) + 1
            return f"water_{variant}"
        elif tile_type == TileType.TREE:
            variants = ["tree_oak", "tree_birch", "tree_pine"]
            return variants[seed % 3]
        elif tile_type == TileType.STONE:
            variant = (seed % 3) + 1
            return f"stones_{variant}"
        else:
            # Types de base
            tile_names = {
                TileType.IRON_ORE: "iron_ore",
                TileType.GOLD_ORE: "gold_ore",
                TileType.DIAMOND_ORE: "diamond_ore",
                TileType.COAL_ORE: "coal_ore",
                TileType.APPLE_TREE: "apple_tree",
                TileType.BERRY_BUSH: "berry_bush",
                TileType.FOUNDATION: "foundation",
                TileType.WALL: "wall",
            }
            return tile_names.get(tile_type, "grass_1")
    
    def draw_world(self, world_map, camera):
        """Dessine le monde avec sprites ou couleurs"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Calculer les tiles visibles
        start_x = max(0, int(camera.x // TILE_SIZE))
        end_x = min(MAP_WIDTH, int((camera.x + screen_width) // TILE_SIZE) + 1)
        start_y = max(0, int(camera.y // TILE_SIZE))
        end_y = min(MAP_HEIGHT, int((camera.y + screen_height) // TILE_SIZE) + 1)
        
        # Dessiner les tiles visibles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile_type = world_map[y][x]
                screen_x = x * TILE_SIZE - camera.x
                screen_y = y * TILE_SIZE - camera.y
                
                # Essayer d'utiliser un sprite
                sprite_name = self.get_tile_sprite_name(tile_type, x, y)
                if not self.sprite_manager.draw_tile(self.screen, sprite_name, screen_x, screen_y):
                    # Fallback: dessiner avec des couleurs
                    color = self.get_tile_color(tile_type)
                    pygame.draw.rect(self.screen, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, COLORS["BLACK"], (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 1)
    
    def draw_player(self, player, camera):
        """Dessine le joueur"""
        player_screen_x = player.x - camera.x
        player_screen_y = player.y - camera.y
        
        # Essayer d'utiliser un sprite
        if not self.sprite_manager.draw_entity(self.screen, "player", 
                                               int(player_screen_x), int(player_screen_y)):
            # Fallback: cercle bleu
            pygame.draw.circle(self.screen, COLORS["BLUE"], 
                             (int(player_screen_x + TILE_SIZE // 2), 
                              int(player_screen_y + TILE_SIZE // 2)), 
                             TILE_SIZE // 3)
    
    def draw_enemies(self, enemies, camera):
        """Dessine les ennemis"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        for enemy in enemies:
            enemy_screen_x = enemy.x - camera.x
            enemy_screen_y = enemy.y - camera.y
            
            if (-TILE_SIZE <= enemy_screen_x <= screen_width and 
                -TILE_SIZE <= enemy_screen_y <= screen_height):
                
                # Essayer d'utiliser un sprite
                if not self.sprite_manager.draw_entity(self.screen, "enemy", 
                                                       int(enemy_screen_x), int(enemy_screen_y)):
                    # Fallback: cercle rouge
                    pygame.draw.circle(self.screen, COLORS["RED"], 
                                     (int(enemy_screen_x + TILE_SIZE // 2), 
                                      int(enemy_screen_y + TILE_SIZE // 2)), 
                                     TILE_SIZE // 3)
                
                # Barre de vie de l'ennemi
                bar_width = TILE_SIZE
                bar_height = 4
                health_ratio = enemy.health / enemy.max_health
                
                pygame.draw.rect(self.screen, COLORS["RED"], 
                               (enemy_screen_x, enemy_screen_y - 8, bar_width, bar_height))
                pygame.draw.rect(self.screen, COLORS["GREEN"], 
                               (enemy_screen_x, enemy_screen_y - 8, bar_width * health_ratio, bar_height))
    
    def draw_death_markers(self, death_markers, camera):
        """Dessine les marqueurs de mort"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        for marker in death_markers:
            marker_screen_x = marker.x - camera.x
            marker_screen_y = marker.y - camera.y
            
            if (-TILE_SIZE <= marker_screen_x <= screen_width and 
                -TILE_SIZE <= marker_screen_y <= screen_height):
                
                # Essayer d'utiliser le sprite de tombe
                if not self.sprite_manager.draw_entity(self.screen, "tombstone", 
                                                       int(marker_screen_x), int(marker_screen_y)):
                    # Fallback: tombe dessinée manuellement
                    center_x = int(marker_screen_x + TILE_SIZE // 2)
                    center_y = int(marker_screen_y + TILE_SIZE // 2)
                    
                    # Fond de la tombe
                    pygame.draw.circle(self.screen, (40, 40, 40), (center_x, center_y), 18)
                    pygame.draw.circle(self.screen, (100, 100, 100), (center_x, center_y), 16)
                    
                    # Base de la tombe
                    pygame.draw.rect(self.screen, (80, 80, 80), 
                                   (center_x - 12, center_y + 8, 24, 6))
                    
                    # Pierre tombale
                    pygame.draw.rect(self.screen, (120, 120, 120), 
                                   (center_x - 8, center_y - 8, 16, 16))
                    pygame.draw.rect(self.screen, (60, 60, 60), 
                                   (center_x - 8, center_y - 8, 16, 16), 2)
                    
                    # Croix sur la tombe
                    pygame.draw.line(self.screen, (255, 255, 255), 
                                   (center_x, center_y - 6), (center_x, center_y + 4), 3)
                    pygame.draw.line(self.screen, (255, 255, 255), 
                                   (center_x - 4, center_y - 2), (center_x + 4, center_y - 2), 3)
                    
                    # Petites fleurs
                    pygame.draw.circle(self.screen, (255, 100, 100), (center_x - 10, center_y + 10), 3)
                    pygame.draw.circle(self.screen, (100, 255, 100), (center_x + 10, center_y + 10), 3)
                
                # Texte "Inventaire" plus visible
                font = pygame.font.Font(None, 18)
                text_bg = font.render("Inventaire", True, (0, 0, 0))
                text_fg = font.render("Inventaire", True, (255, 255, 255))
                
                # Ombre du texte
                self.screen.blit(text_bg, (marker_screen_x + 1, marker_screen_y - 21))
                self.screen.blit(text_fg, (marker_screen_x, marker_screen_y - 22))
    
    def draw_entities(self, player, enemies, death_markers, camera, item_manager=None):
        """Dessine toutes les entités du jeu"""
        self.draw_player(player, camera)
        self.draw_enemies(enemies, camera)
        self.draw_death_markers(death_markers, camera)
        
        # Dessiner les items dispersés
        if item_manager:
            item_manager.draw_all(self.screen, camera, self.sprite_manager)
