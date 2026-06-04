"""
Minimap Battle Royale
"""

import pygame
from .constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE


class MiniMap:
    def __init__(self, screen_width, screen_height):
        self.width = 200
        self.height = 150
        self.x = screen_width - self.width - 10
        self.y = 10
        self.scale = min(self.width / (MAP_WIDTH * TILE_SIZE), self.height / (MAP_HEIGHT * TILE_SIZE))
        self.world_surface = None
        self.fog_surface = None

    def generate_world_minimap(self, world_map):
        self.world_surface = pygame.Surface((self.width, self.height))
        self.fog_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.fog_surface.fill((0, 0, 0, 180))

        from .tiletype import TileType
        colors = {
            TileType.GRASS: (50, 110, 45),
            TileType.DIRT: (110, 90, 60),
            TileType.WATER: (35, 90, 150),
            TileType.ROAD: (80, 75, 65),
            TileType.BUILDING: (90, 85, 75),
            TileType.WALL: (80, 70, 55),
            TileType.LOOT_SPOT: (160, 140, 50),
            TileType.SAND: (170, 155, 115),
        }

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                mx = int(x * TILE_SIZE * self.scale)
                my = int(y * TILE_SIZE * self.scale)
                size = max(1, int(TILE_SIZE * self.scale))
                color = colors.get(world_map[y][x], (60, 60, 60))
                pygame.draw.rect(self.world_surface, color, (mx, my, size, size))

    def update_screen_size(self, sw, sh):
        self.x = sw - self.width - 10
        self.y = 10

    def world_to_minimap(self, wx, wy):
        return int(wx * self.scale), int(wy * self.scale)

    def draw(self, screen, player, enemies=None, camera=None, death_markers=None):
        import math

        shadow = pygame.Surface((self.width + 8, self.height + 8), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 80), (0, 0, self.width + 8, self.height + 8), border_radius=6)
        screen.blit(shadow, (self.x - 4, self.y - 4))

        bg = pygame.Surface((self.width + 4, self.height + 4), pygame.SRCALPHA)
        pygame.draw.rect(bg, (10, 14, 28, 200), (0, 0, self.width + 4, self.height + 4), border_radius=6)
        screen.blit(bg, (self.x - 2, self.y - 2))

        if self.world_surface:
            screen.blit(self.world_surface, (self.x, self.y))

        if self.fog_surface and player:
            revealed = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            revealed.fill((0, 0, 0, 160))
            px, py = self.world_to_minimap(player.x, player.y)
            radius = int(25)
            pygame.draw.circle(revealed, (0, 0, 0, 255), (px, py), radius)
            revealed.set_colorkey((0, 0, 0))
            self.fog_surface.fill((0, 0, 0, 160))
            mask = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            mask.fill((0, 0, 0, 160))
            pygame.draw.circle(mask, (0, 0, 0, 0), (px, py), radius)
            self.fog_surface.blit(mask, (0, 0))

        if enemies:
            for enemy in enemies:
                if enemy.health <= 0:
                    continue
                emx, emy = self.world_to_minimap(enemy.x, enemy.y)
                color = enemy.color_tier.get(enemy.tier, (200, 80, 80))
                pygame.draw.circle(screen, color, (self.x + emx, self.y + emy), 2)

        if player:
            pmx, pmy = self.world_to_minimap(player.x, player.y)
            pygame.draw.circle(screen, (60, 140, 255), (self.x + pmx, self.y + pmy), 3)
            pygame.draw.circle(screen, (120, 190, 255), (self.x + pmx, self.y + pmy), 1)

        if camera:
            cmx = int(camera.x * self.scale)
            cmy = int(camera.y * self.scale)
            cmw = int(camera.screen_width * self.scale)
            cmh = int(camera.screen_height * self.scale)
            pygame.draw.rect(screen, (255, 255, 100), (self.x + cmx, self.y + cmy, cmw, cmh), 1)

        font = pygame.font.Font(None, 14)
        screen.blit(font.render("Carte", True, (120, 140, 180)), (self.x + 4, self.y - 14))
