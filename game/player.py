"""
Joueur Battle Royale
"""

import random
import math
import pygame

from ui.inventory import Inventory
from .constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE
from .tiletype import TileType


class Player:
    WEAPON_DAMAGE = {
        "Pistolet": 15, "Shotgun": 40, "Fusil": 25,
        "Sniper": 60, "SMG": 10, "Katana": 35, "Hache": 20,
    }
    BARE_HANDS_DAMAGE = 5
    ATTACK_RANGE = TILE_SIZE * 2
    ATTACK_COOLDOWN = 0.4

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 140
        self.health = 100
        self.max_health = 100
        self.base_max_health = 100
        self.inventory = Inventory(24)

        self.is_moving = False
        self.animation_time = 0
        self.last_attack_time = 0
        self.attack_feedback = None
        self.xp = 0
        self.level = 1
        self.kills = 0

    def move(self, dx, dy, dt, world_map):
        self.is_moving = (dx != 0 or dy != 0)
        if self.is_moving:
            self.animation_time += dt
        else:
            self.animation_time = 0

        if dx != 0 or dy != 0:
            length = math.sqrt(dx * dx + dy * dy)
            dx /= length
            dy /= length

        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt

        if 0 <= new_x < MAP_WIDTH * TILE_SIZE and 0 <= new_y < MAP_HEIGHT * TILE_SIZE:
            tile_x = int(new_x // TILE_SIZE)
            tile_y = int(new_y // TILE_SIZE)
            tile = world_map[tile_y][tile_x]

            if tile not in (TileType.WATER, TileType.WALL, TileType.BUILDING):
                speed_mult = 0.5 if tile == TileType.SAND else 1.0
                self.x += dx * self.speed * dt * speed_mult
                self.y += dy * self.speed * dt * speed_mult

    def get_current_sprite(self):
        if not self.is_moving:
            return "player"
        cycle = self.animation_time % 0.5
        return "player_walk1" if cycle < 0.25 else "player_walk2"

    def get_attack_damage(self):
        for slot in self.inventory.slots:
            if slot and slot.item.type == "weapon":
                return self.WEAPON_DAMAGE.get(slot.item.name, self.BARE_HANDS_DAMAGE)
        return self.BARE_HANDS_DAMAGE

    def get_weapon_name(self):
        for slot in self.inventory.slots:
            if slot and slot.item.type == "weapon":
                return slot.item.name
        return "Mains"

    def attack_enemies(self, enemies, mouse_pos, camera_x, camera_y, current_time):
        if current_time - self.last_attack_time < self.ATTACK_COOLDOWN:
            return None, 0

        world_x = mouse_pos[0] + camera_x
        world_y = mouse_pos[1] + camera_y

        closest = None
        closest_dist = self.ATTACK_RANGE

        for enemy in enemies:
            if enemy.health <= 0:
                continue
            dist = math.sqrt((enemy.x - world_x) ** 2 + (enemy.y - world_y) ** 2)
            if dist < closest_dist:
                closest_dist = dist
                closest = enemy

        if closest:
            damage = self.get_attack_damage()
            closest.health -= damage
            self.last_attack_time = current_time
            self.attack_feedback = (f"-{damage}", 0.8)
            return closest, damage

        return None, 0

    def heal(self, amount):
        old = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - old

    def apply_armor_bonus(self):
        bonus = 0
        for slot in self.inventory.slots:
            if slot and slot.item.type == "armor":
                if "Lv1" in slot.item.name:
                    bonus = max(bonus, 20)
                elif "Lv2" in slot.item.name:
                    bonus = max(bonus, 40)
                elif "Lv3" in slot.item.name:
                    bonus = max(bonus, 60)
        self.max_health = self.base_max_health + bonus
        self.health = min(self.health, self.max_health)

    def eat_best_food(self):
        for slot in self.inventory.slots:
            if slot and slot.item.type == "heal":
                healed = self.heal(25 if "Bandage" in slot.item.name else (75 if "Medkit" in slot.item.name else 50))
                slot.quantity -= 1
                if slot.quantity <= 0:
                    idx = self.inventory.slots.index(slot)
                    self.inventory.slots[idx] = None
                return slot.item.name, healed
        return None

    def update(self, keys, dt, controls=None):
        if self.attack_feedback:
            text, timer = self.attack_feedback
            timer -= dt
            self.attack_feedback = (text, timer) if timer > 0 else None

        if controls is None:
            controls = {
                "move_up": pygame.K_w, "move_down": pygame.K_s,
                "move_left": pygame.K_a, "move_right": pygame.K_d,
            }

        dx, dy = 0, 0
        if keys[controls["move_up"]]: dy -= 1
        if keys[controls["move_down"]]: dy += 1
        if keys[controls["move_left"]]: dx -= 1
        if keys[controls["move_right"]]: dx += 1

        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        return dx, dy

    def is_dead(self):
        return self.health <= 0
