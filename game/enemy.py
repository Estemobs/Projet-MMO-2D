"""
Ennemis Battle Royale - Combattants agressifs
"""

import math
import random
import time
from .constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE
from .tiletype import TileType


class Enemy:
    LOOT_TABLE = [
        ("bandage", 0.40, 1, 2),
        ("ammo", 0.30, 5, 15),
        ("potion", 0.20, 1, 1),
    ]
    XP_REWARD = 25

    def __init__(self, x, y, tier=1):
        self.x = x
        self.y = y
        self.tier = tier

        hp_table = {1: 60, 2: 100, 3: 150}
        dmg_table = {1: 8, 2: 15, 3: 25}
        speed_table = {1: 55, 2: 65, 3: 80}
        loot_table = {
            1: [("bandage", 0.5, 1, 1), ("ammo", 0.4, 3, 8)],
            2: [("bandage", 0.6, 1, 2), ("ammo", 0.5, 5, 12), ("potion", 0.3, 1, 1)],
            3: [("medkit", 0.4, 1, 1), ("ammo", 0.7, 8, 20), ("potion", 0.5, 1, 2)],
        }

        self.health = hp_table.get(tier, 60)
        self.max_health = self.health
        self.damage = dmg_table.get(tier, 8)
        self.speed = speed_table.get(tier, 55)
        self.detection_range = 7
        self.attack_range = 1.2
        self.attack_cooldown = 1.0
        self.last_attack_time = 0

        self.is_moving = False
        self.animation_time = 0

        self.color_tier = {
            1: (200, 80, 80),
            2: (200, 150, 50),
            3: (180, 50, 200),
        }

    def is_dead(self):
        return self.health <= 0

    def get_loot(self, items):
        drops = []
        tier_loot = self.LOOT_TABLE if self.tier == 1 else [
            ("bandage", 0.6, 1, 2), ("ammo", 0.5, 5, 15), ("potion", 0.3, 1, 1),
        ]
        if self.tier >= 3:
            tier_loot.append(("medkit", 0.3, 1, 1))

        for item_key, prob, min_q, max_q in tier_loot:
            if random.random() < prob and item_key in items:
                drops.append((items[item_key], random.randint(min_q, max_q)))
        return drops

    def move_towards(self, target_x, target_y, dt, world_map):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        self.is_moving = True
        self.animation_time += dt

        if dist > 0:
            dx /= dist
            dy /= dist
            new_x = self.x + dx * self.speed * dt
            new_y = self.y + dy * self.speed * dt

            if 0 <= new_x < MAP_WIDTH * TILE_SIZE and 0 <= new_y < MAP_HEIGHT * TILE_SIZE:
                tx = int(new_x // TILE_SIZE)
                ty = int(new_y // TILE_SIZE)
                if world_map[ty][tx] not in (TileType.WATER, TileType.WALL, TileType.BUILDING):
                    self.x = new_x
                    self.y = new_y

    def attack_target(self, target, current_time):
        if current_time - self.last_attack_time >= self.attack_cooldown:
            target.health -= self.damage
            self.last_attack_time = current_time
            return True
        return False

    def update(self, player, world_map, dt):
        current_time = time.time()
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist <= self.detection_range * TILE_SIZE:
            if dist <= self.attack_range * TILE_SIZE:
                self.attack_target(player, current_time)
            else:
                self.move_towards(player.x, player.y, dt, world_map)
        else:
            self.is_moving = False
