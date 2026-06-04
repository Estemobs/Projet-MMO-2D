"""
Generateur de map Battle Royale
Terrain ouvert, batiments, routes, zones de loot
"""

from .tiletype import TileType
from .constants import MAP_WIDTH, MAP_HEIGHT
import random
import math


class NaturalWorldGenerator:

    @staticmethod
    def generate_natural_map():
        world_map = [[TileType.GRASS for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

        NaturalWorldGenerator._generate_terrain(world_map)
        NaturalWorldGenerator._generate_roads(world_map)
        NaturalWorldGenerator._generate_water(world_map)
        NaturalWorldGenerator._generate_buildings(world_map)
        NaturalWorldGenerator._generate_cover(world_map)
        NaturalWorldGenerator._generate_loot_spots(world_map)

        return world_map

    @staticmethod
    def _generate_terrain(world_map):
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                nx = x / MAP_WIDTH
                ny = y / MAP_HEIGHT
                n = math.sin(nx * 6) * math.cos(ny * 6) * 0.3 + 0.5
                if n < 0.2:
                    world_map[y][x] = TileType.SAND
                elif n > 0.85:
                    world_map[y][x] = TileType.DIRT

    @staticmethod
    def _generate_roads(world_map):
        for _ in range(3):
            if random.choice([True, False]):
                sy = random.randint(MAP_HEIGHT // 4, 3 * MAP_HEIGHT // 4)
                ey = random.randint(MAP_HEIGHT // 4, 3 * MAP_HEIGHT // 4)
                for x in range(MAP_WIDTH):
                    progress = x / MAP_WIDTH
                    y = int(sy + (ey - sy) * progress + math.sin(progress * 8) * 5)
                    for dy in range(-1, 2):
                        ny = y + dy
                        if 0 <= ny < MAP_HEIGHT:
                            world_map[ny][x] = TileType.ROAD
            else:
                sx = random.randint(MAP_WIDTH // 4, 3 * MAP_WIDTH // 4)
                ex = random.randint(MAP_WIDTH // 4, 3 * MAP_WIDTH // 4)
                for y in range(MAP_HEIGHT):
                    progress = y / MAP_HEIGHT
                    x = int(sx + (ex - sx) * progress + math.sin(progress * 8) * 5)
                    for dx in range(-1, 2):
                        nx = x + dx
                        if 0 <= nx < MAP_WIDTH:
                            world_map[y][nx] = TileType.ROAD

    @staticmethod
    def _generate_water(world_map):
        for _ in range(random.randint(2, 4)):
            cx = random.randint(15, MAP_WIDTH - 15)
            cy = random.randint(15, MAP_HEIGHT - 15)
            size = random.randint(4, 8)
            for dy in range(-size, size + 1):
                for dx in range(-size, size + 1):
                    d = math.sqrt(dx * dx + dy * dy)
                    if d <= size:
                        x, y = cx + dx, cy + dy
                        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                            prob = 1 - (d / size) ** 2
                            if random.random() < prob:
                                world_map[y][x] = TileType.WATER

    @staticmethod
    def _generate_buildings(world_map):
        buildings = []
        for _ in range(random.randint(12, 18)):
            bx = random.randint(5, MAP_WIDTH - 10)
            by = random.randint(5, MAP_HEIGHT - 10)
            bw = random.randint(3, 6)
            bh = random.randint(3, 6)

            can_place = True
            for obx, oby, obw, obh in buildings:
                if bx < obx + obw + 2 and bx + bw + 2 > obx and by < oby + obh + 2 and by + bh + 2 > oby:
                    can_place = False
                    break

            if can_place:
                buildings.append((bx, by, bw, bh))
                for dy in range(bh):
                    for dx in range(bw):
                        x, y = bx + dx, by + dy
                        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                            if dy == 0 or dy == bh - 1 or dx == 0 or dx == bw - 1:
                                world_map[y][x] = TileType.WALL
                            else:
                                world_map[y][x] = TileType.BUILDING

                for _ in range(2):
                    rx = bx + random.randint(1, bw - 2)
                    ry = by + random.randint(1, bh - 2)
                    if 0 <= rx < MAP_WIDTH and 0 <= ry < MAP_HEIGHT:
                        world_map[ry][rx] = TileType.LOOT_SPOT

    @staticmethod
    def _generate_cover(world_map):
        for _ in range(random.randint(20, 35)):
            x = random.randint(2, MAP_WIDTH - 3)
            y = random.randint(2, MAP_HEIGHT - 3)
            if world_map[y][x] == TileType.GRASS:
                world_map[y][x] = TileType.WALL

    @staticmethod
    def _generate_loot_spots(world_map):
        for _ in range(random.randint(40, 60)):
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            if world_map[y][x] in (TileType.GRASS, TileType.DIRT, TileType.ROAD):
                world_map[y][x] = TileType.LOOT_SPOT
