"""
Render Manager - Battle Royale style
"""

import pygame
import math
from .constants import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, COLORS
from .tiletype import TileType
from .sprite_manager import get_sprite_manager


def _hash_pos(x, y):
    return (x * 7919 + y * 6271) % 1000


class RenderManager:
    def __init__(self, screen):
        self.screen = screen
        self.sprite_manager = get_sprite_manager()
        self.time = 0.0

        self._tile_colors = {
            TileType.GRASS: (70, 140, 60),
            TileType.DIRT: (130, 105, 70),
            TileType.WATER: (40, 110, 180),
            TileType.ROAD: (90, 85, 75),
            TileType.BUILDING: (80, 75, 65),
            TileType.WALL: (100, 90, 75),
            TileType.LOOT_SPOT: (180, 160, 60),
            TileType.SAND: (190, 175, 130),
        }

    def update_time(self, dt):
        self.time += dt

    def draw_world(self, world_map, camera):
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        start_x = max(0, int(camera.x // TILE_SIZE))
        end_x = min(MAP_WIDTH, int((camera.x + sw) // TILE_SIZE) + 2)
        start_y = max(0, int(camera.y // TILE_SIZE))
        end_y = min(MAP_HEIGHT, int((camera.y + sh) // TILE_SIZE) + 2)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = world_map[y][x]
                sx = x * TILE_SIZE - camera.x
                sy = y * TILE_SIZE - camera.y

                color = self._tile_colors.get(tile, (80, 80, 80))

                if tile == TileType.GRASS:
                    h = _hash_pos(x, y)
                    noise = (h % 11) - 5
                    color = tuple(max(0, min(255, c + noise)) for c in color)
                elif tile == TileType.WATER:
                    wave = math.sin(self.time * 2 + x * 0.5 + y * 0.3) * 15
                    color = tuple(max(0, min(255, int(c + wave))) for c in color)
                elif tile == TileType.LOOT_SPOT:
                    pulse = int(abs(math.sin(self.time * 2 + x + y)) * 40)
                    color = (color[0], min(255, color[1] + pulse), color[2])

                pygame.draw.rect(self.screen, color, (sx, sy, TILE_SIZE, TILE_SIZE))

                if tile == TileType.WALL:
                    pygame.draw.rect(self.screen, (70, 60, 50), (sx, sy, TILE_SIZE, TILE_SIZE), 2)
                    pygame.draw.line(self.screen, (60, 50, 40), (sx, sy), (sx + TILE_SIZE, sy + TILE_SIZE), 1)
                elif tile == TileType.BUILDING:
                    pygame.draw.rect(self.screen, (60, 55, 48), (sx, sy, TILE_SIZE, TILE_SIZE), 1)
                elif tile == TileType.ROAD:
                    if _hash_pos(x, y) % 4 == 0:
                        pygame.draw.line(self.screen, (100, 95, 85), (sx + 4, sy + TILE_SIZE // 2),
                                        (sx + TILE_SIZE - 4, sy + TILE_SIZE // 2), 1)
                elif tile == TileType.LOOT_SPOT:
                    glow = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    a = int(abs(math.sin(self.time * 1.5 + x * 0.3 + y * 0.7)) * 50) + 20
                    pygame.draw.circle(glow, (255, 220, 80, a), (TILE_SIZE // 2, TILE_SIZE // 2), 6)
                    self.screen.blit(glow, (sx, sy))

    def draw_player(self, player, camera):
        px = player.x - camera.x
        py = player.y - camera.y

        shadow = pygame.Surface((32, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 50), (0, 0, 32, 8))
        self.screen.blit(shadow, (int(px) - 2, int(py) + TILE_SIZE - 2))

        sprite_name = "player"
        if player.is_moving:
            frame = player.animation_time % 0.5
            sprite_name = "player_walk1" if frame < 0.25 else "player_walk2"

        draw_x = int(px - 8)
        draw_y = int(py - 8)
        if not self.sprite_manager.draw_entity(self.screen, sprite_name, draw_x, draw_y):
            cx, cy = int(px + TILE_SIZE // 2), int(py + TILE_SIZE // 2)
            pygame.draw.circle(self.screen, (20, 60, 120), (cx, cy), 14)
            pygame.draw.circle(self.screen, (80, 160, 255), (cx, cy), 12)

    def draw_enemies(self, enemies, camera):
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        for enemy in enemies:
            if enemy.health <= 0:
                continue

            ex = enemy.x - camera.x
            ey = enemy.y - camera.y

            if -TILE_SIZE <= ex <= sw and -TILE_SIZE <= ey <= sh:
                cx, cy = int(ex + TILE_SIZE // 2), int(ey + TILE_SIZE // 2)
                color = enemy.color_tier.get(enemy.tier, (200, 80, 80))

                shadow = pygame.Surface((28, 6), pygame.SRCALPHA)
                pygame.draw.ellipse(shadow, (0, 0, 0, 40), (0, 0, 28, 6))
                self.screen.blit(shadow, (int(ex) + 2, int(ey) + TILE_SIZE - 2))

                if not self.sprite_manager.draw_entity(self.screen, "enemy", int(ex - 8), int(ey - 8)):
                    pygame.draw.circle(self.screen, (80, 20, 20), (cx, cy), 13)
                    pygame.draw.circle(self.screen, color, (cx, cy), 11)
                    eye_off = 3
                    pygame.draw.circle(self.screen, (255, 255, 255), (cx - eye_off, cy - 2), 3)
                    pygame.draw.circle(self.screen, (255, 255, 255), (cx + eye_off, cy - 2), 3)
                    pygame.draw.circle(self.screen, (20, 20, 20), (cx - eye_off, cy - 2), 1)
                    pygame.draw.circle(self.screen, (20, 20, 20), (cx + eye_off, cy - 2), 1)

                bar_w = 30
                bar_h = 4
                ratio = max(0, enemy.health / enemy.max_health)
                bx = cx - bar_w // 2
                by = int(ey) - 10
                pygame.draw.rect(self.screen, (30, 30, 30), (bx, by, bar_w, bar_h), border_radius=2)
                fill = int(bar_w * ratio)
                bc = (50, 200, 80) if ratio > 0.5 else ((220, 180, 40) if ratio > 0.25 else (220, 50, 50))
                if fill > 0:
                    pygame.draw.rect(self.screen, bc, (bx, by, fill, bar_h), border_radius=2)

                tier_text = {1: "", 2: "+", 3: "++"}
                if enemy.tier > 1:
                    tf = pygame.font.Font(None, 14)
                    tt = tf.render(tier_text[enemy.tier], True, color)
                    self.screen.blit(tt, (cx + 14, cy - 8))

    def draw_death_markers(self, death_markers, camera):
        for marker in death_markers:
            mx = marker.x - camera.x
            my = marker.y - camera.y
            pulse = int(abs(math.sin(self.time * 2)) * 30) + 20
            glow = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 200, 100, pulse), (20, 20), 20)
            self.screen.blit(glow, (int(mx) - 4, int(my) - 4))
            cx, cy = int(mx + TILE_SIZE // 2), int(my + TILE_SIZE // 2)
            pygame.draw.rect(self.screen, (100, 95, 90), (cx - 6, cy - 8, 12, 14), border_radius=2)
            pygame.draw.line(self.screen, (200, 195, 185), (cx, cy - 5), (cx, cy + 2), 2)
            pygame.draw.line(self.screen, (200, 195, 185), (cx - 3, cy - 2), (cx + 3, cy - 2), 2)

    def draw_entities(self, player, enemies, death_markers, camera, item_manager=None):
        self.draw_player(player, camera)
        self.draw_enemies(enemies, camera)
        self.draw_death_markers(death_markers, camera)
        if item_manager:
            item_manager.draw_all(self.screen, camera, self.sprite_manager)
