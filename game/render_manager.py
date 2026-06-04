"""
Gestionnaire de rendu pour le jeu MMO 2D
Améliorations visuelles : variations herbe, ombres, eau animée, grille subtile
"""

import pygame
import math
from .constants import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, COLORS
from .tiletype import TileType
from .sprite_manager import get_sprite_manager


def _hash_pos(x, y):
    """Hash déterministe pour varier les tiles selon la position."""
    return (x * 7919 + y * 6271) % 1000


def _lerp_color(c1, c2, t):
    """Interpolation linéaire entre deux couleurs RGB."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


class RenderManager:
    def __init__(self, screen):
        self.screen = screen
        self.sprite_manager = get_sprite_manager()
        self.time = 0.0

        # Pré-calculer les variations de herbe (4 teintes)
        self._grass_variants = [
            (74, 200, 115),   # vert un peu plus sombre
            (84, 214, 125),   # vert de base
            (94, 224, 135),   # vert un peu plus clair
            (79, 207, 120),   # vert intermédiaire
        ]

        # Couleurs de fallback améliorées
        self._tile_colors = {
            TileType.GRASS: (84, 214, 125),
            TileType.TREE: (52, 130, 72),
            TileType.STONE: (140, 140, 145),
            TileType.IRON_ORE: (160, 110, 95),
            TileType.GOLD_ORE: (220, 185, 60),
            TileType.DIAMOND_ORE: (120, 200, 240),
            TileType.COAL_ORE: (50, 50, 55),
            TileType.APPLE_TREE: (60, 160, 80),
            TileType.BERRY_BUSH: (140, 70, 160),
            TileType.FOUNDATION: (130, 125, 115),
            TileType.WALL: (120, 85, 50),
            TileType.DIRT: (139, 117, 78),
            TileType.WATER: (50, 140, 200),
        }

    def update_time(self, dt):
        """Met à jour le temps pour les animations."""
        self.time += dt

    def get_tile_sprite_name(self, tile_type, x=0, y=0):
        """Retourne le nom du sprite pour une tile avec variantes."""
        seed = _hash_pos(x, y)

        if tile_type == TileType.GRASS:
            return "grass_1"
        elif tile_type == TileType.DIRT:
            return f"dirt_{(seed % 3) + 1}"
        elif tile_type == TileType.WATER:
            # Animation : cycle entre les 3 variantes
            cycle = int(self.time * 2) % 3
            return f"water_{cycle + 1}"
        elif tile_type == TileType.TREE:
            variants = ["tree_oak", "tree_birch", "tree_pine"]
            return variants[seed % 3]
        elif tile_type == TileType.STONE:
            return f"stones_{(seed % 3) + 1}"
        else:
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

    def _get_grass_color(self, x, y):
        """Retourne une couleur de herbe variable selon la position."""
        h = _hash_pos(x, y)
        variant = self._grass_variants[h % len(self._grass_variants)]
        # Ajouter un micro-bruit
        noise = (h % 7) - 3  # -3 à +3
        return tuple(max(0, min(255, c + noise)) for c in variant)

    def _draw_tile_fallback(self, tile_type, screen_x, screen_y, x, y):
        """Dessine une tile sans sprite (fallback coloré amélioré)."""
        if tile_type == TileType.GRASS:
            color = self._get_grass_color(x, y)
        elif tile_type == TileType.WATER:
            # Eau avec variation de couleur animée
            wave = math.sin(self.time * 2 + x * 0.5 + y * 0.3) * 15
            base = self._tile_colors.get(tile_type, (50, 140, 200))
            color = tuple(max(0, min(255, int(c + wave))) for c in base)
        else:
            color = self._tile_colors.get(tile_type, (100, 100, 100))

        pygame.draw.rect(self.screen, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))

        # Grille très subtile pour la lisibilité
        grid_color = (0, 0, 0, 25)
        pygame.draw.rect(self.screen, (0, 0, 0), (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 1)
        # Rendre la grille plus subtile avec une surface alpha
        grid_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(grid_surf, (0, 0, 0, 20), grid_surf.get_rect())
        self.screen.blit(grid_surf, (screen_x, screen_y))

    def _draw_tree_shadow(self, screen_x, screen_y):
        """Dessine une ombre d'arbre sous la tile."""
        shadow_surf = pygame.Surface((TILE_SIZE + 8, 12), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 50), (0, 0, TILE_SIZE + 8, 12))
        self.screen.blit(shadow_surf, (screen_x - 4, screen_y + TILE_SIZE - 6))

    def draw_world(self, world_map, camera):
        """Dessine le monde avec sprites, variations et ombres."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        start_x = max(0, int(camera.x // TILE_SIZE))
        end_x = min(MAP_WIDTH, int((camera.x + screen_width) // TILE_SIZE) + 2)
        start_y = max(0, int(camera.y // TILE_SIZE))
        end_y = min(MAP_HEIGHT, int((camera.y + screen_height) // TILE_SIZE) + 2)

        # Pass 1 : tiles de base (herbe, terre, eau, etc.)
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile_type = world_map[y][x]
                screen_x = x * TILE_SIZE - camera.x
                screen_y = y * TILE_SIZE - camera.y

                sprite_name = self.get_tile_sprite_name(tile_type, x, y)
                if not self.sprite_manager.draw_tile(self.screen, sprite_name, screen_x, screen_y):
                    self._draw_tile_fallback(tile_type, screen_x, screen_y, x, y)

        # Pass 2 : ombres et overlays (arbres, buissons, minerais)
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile_type = world_map[y][x]
                screen_x = x * TILE_SIZE - camera.x
                screen_y = y * TILE_SIZE - camera.y

                # Ombres sous les arbres et buissons
                if tile_type in (TileType.TREE, TileType.APPLE_TREE, TileType.BERRY_BUSH):
                    self._draw_tree_shadow(screen_x, screen_y)

                # Lueur subtile sur les minerais rares
                if tile_type in (TileType.GOLD_ORE, TileType.DIAMOND_ORE):
                    glow_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    pulse = int(abs(math.sin(self.time * 1.5 + x + y)) * 40)
                    glow_color = (255, 220, 100, pulse) if tile_type == TileType.GOLD_ORE else (100, 200, 255, pulse)
                    pygame.draw.circle(glow_surf, glow_color, (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 2)
                    self.screen.blit(glow_surf, (screen_x, screen_y))

    def draw_player(self, player, camera):
        """Dessine le joueur avec ombre portée et animation."""
        player_screen_x = player.x - camera.x
        player_screen_y = player.y - camera.y

        offset_x = (48 - TILE_SIZE) // 2
        offset_y = (48 - TILE_SIZE) // 2
        draw_x = int(player_screen_x - offset_x)
        draw_y = int(player_screen_y - offset_y)

        # Ombre du joueur
        shadow_surf = pygame.Surface((40, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 60), (0, 0, 40, 10))
        self.screen.blit(shadow_surf, (int(player_screen_x) - 4, int(player_screen_y) + TILE_SIZE - 4))

        # Sprite du joueur
        sprite_name = "player"
        if hasattr(player, 'is_moving') and player.is_moving:
            if hasattr(player, 'animation_time'):
                frame_duration = 0.25
                animation_cycle = player.animation_time % (frame_duration * 2)
                sprite_name = "player_walk1" if animation_cycle < frame_duration else "player_walk2"

        if not self.sprite_manager.draw_entity(self.screen, sprite_name, draw_x, draw_y):
            # Fallback amélioré : silhouette avec contour
            cx = int(player_screen_x + TILE_SIZE // 2)
            cy = int(player_screen_y + TILE_SIZE // 2)
            pygame.draw.circle(self.screen, (20, 60, 120), (cx, cy), 14)
            pygame.draw.circle(self.screen, COLORS["BLUE"], (cx, cy), 12)
            pygame.draw.circle(self.screen, (140, 200, 255), (cx - 2, cy - 3), 4)

    def draw_enemies(self, enemies, camera):
        """Dessine les ennemis avec ombre et barre de vie améliorée."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        for enemy in enemies:
            enemy_screen_x = enemy.x - camera.x
            enemy_screen_y = enemy.y - camera.y

            if (-TILE_SIZE <= enemy_screen_x <= screen_width and
                -TILE_SIZE <= enemy_screen_y <= screen_height):

                offset_x = (48 - TILE_SIZE) // 2
                offset_y = (48 - TILE_SIZE) // 2
                draw_x = int(enemy_screen_x - offset_x)
                draw_y = int(enemy_screen_y - offset_y)

                # Ombre
                shadow_surf = pygame.Surface((40, 10), pygame.SRCALPHA)
                pygame.draw.ellipse(shadow_surf, (0, 0, 0, 50), (0, 0, 40, 10))
                self.screen.blit(shadow_surf, (int(enemy_screen_x) - 4, int(enemy_screen_y) + TILE_SIZE - 4))

                # Sprite
                sprite_name = "enemy"
                if hasattr(enemy, 'is_moving') and enemy.is_moving:
                    if hasattr(enemy, 'animation_time'):
                        frame_duration = 0.4
                        animation_cycle = enemy.animation_time % (frame_duration * 2)
                        sprite_name = "enemy_move1" if animation_cycle < frame_duration else "enemy"

                if not self.sprite_manager.draw_entity(self.screen, sprite_name, draw_x, draw_y):
                    cx = int(enemy_screen_x + TILE_SIZE // 2)
                    cy = int(enemy_screen_y + TILE_SIZE // 2)
                    pygame.draw.circle(self.screen, (120, 30, 30), (cx, cy), 14)
                    pygame.draw.circle(self.screen, COLORS["RED"], (cx, cy), 12)

                # Barre de vie améliorée avec gradient
                bar_width = 48
                bar_height = 6
                health_ratio = max(0, enemy.health / enemy.max_health)

                # Fond avec bordure arrondie
                bar_bg = pygame.Surface((bar_width, bar_height + 2), pygame.SRCALPHA)
                pygame.draw.rect(bar_bg, (20, 20, 30, 180), (0, 1, bar_width, bar_height), border_radius=3)
                self.screen.blit(bar_bg, (draw_x, draw_y - 12))

                # Barre de vie avec couleur dynamique
                if health_ratio < 0.33:
                    bar_color = (220, 50, 50)
                elif health_ratio < 0.66:
                    bar_color = (220, 180, 40)
                else:
                    bar_color = (50, 200, 80)

                fill_width = int(bar_width * health_ratio)
                if fill_width > 0:
                    bar_fill = pygame.Surface((fill_width, bar_height), pygame.SRCALPHA)
                    pygame.draw.rect(bar_fill, (*bar_color, 220), (0, 0, fill_width, bar_height), border_radius=2)
                    self.screen.blit(bar_fill, (draw_x, draw_y - 11))

                # Bordure fine
                pygame.draw.rect(self.screen, (80, 80, 100), (draw_x, draw_y - 12, bar_width, bar_height + 2), 1, border_radius=3)

    def draw_death_markers(self, death_markers, camera):
        """Dessine les marqueurs de mort avec lueur."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        for marker in death_markers:
            marker_screen_x = marker.x - camera.x
            marker_screen_y = marker.y - camera.y

            if (-TILE_SIZE <= marker_screen_x <= screen_width and
                -TILE_SIZE <= marker_screen_y <= screen_height):

                # Lueur pulsante autour du marqueur
                pulse = int(abs(math.sin(self.time * 2)) * 30) + 20
                glow_surf = pygame.Surface((48, 48), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (255, 200, 100, pulse), (24, 24), 24)
                self.screen.blit(glow_surf, (int(marker_screen_x) - 8, int(marker_screen_y) - 8))

                # Tombe
                if not self.sprite_manager.draw_entity(self.screen, "tombstone",
                                                       int(marker_screen_x), int(marker_screen_y)):
                    center_x = int(marker_screen_x + TILE_SIZE // 2)
                    center_y = int(marker_screen_y + TILE_SIZE // 2)

                    # Base
                    pygame.draw.ellipse(self.screen, (30, 30, 35), (center_x - 14, center_y + 6, 28, 10))
                    # Pierre
                    pygame.draw.rect(self.screen, (100, 95, 90), (center_x - 8, center_y - 10, 16, 18), border_radius=3)
                    pygame.draw.rect(self.screen, (70, 65, 60), (center_x - 8, center_y - 10, 16, 18), 1, border_radius=3)
                    # Croix
                    pygame.draw.line(self.screen, (200, 195, 185), (center_x, center_y - 7), (center_x, center_y + 3), 2)
                    pygame.draw.line(self.screen, (200, 195, 185), (center_x - 4, center_y - 3), (center_x + 4, center_y - 3), 2)

                # Texte "Inventaire" avec ombre
                font = pygame.font.Font(None, 16)
                text_bg = font.render("Inventaire", True, (0, 0, 0))
                text_fg = font.render("Inventaire", True, (255, 230, 150))
                self.screen.blit(text_bg, (marker_screen_x + 1, marker_screen_y - 19))
                self.screen.blit(text_fg, (marker_screen_x, marker_screen_y - 20))

    def draw_entities(self, player, enemies, death_markers, camera, item_manager=None):
        """Dessine toutes les entités du jeu."""
        self.draw_player(player, camera)
        self.draw_enemies(enemies, camera)
        self.draw_death_markers(death_markers, camera)

        if item_manager:
            item_manager.draw_all(self.screen, camera, self.sprite_manager)
