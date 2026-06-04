"""
Gameplay Manager - Battle Royale
"""

import time
import random
from .player import Player
from .enemy import Enemy
from .natural_world import NaturalWorldGenerator
from .camera import Camera
from .item_system import ItemManager
from .particles import ParticleManager
from .sound_manager import get_sound_manager
from .constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, ENEMY_COUNT


class DeathMarker:
    def __init__(self, x, y, inventory):
        self.x = x
        self.y = y
        self.inventory = inventory
        self.timestamp = time.time()

    def can_pickup(self, px, py):
        return ((px - self.x)**2 + (py - self.y)**2)**0.5 <= TILE_SIZE * 2


class GameplayManager:
    def __init__(self):
        self.world_map = None
        self.player = None
        self.camera = None
        self.enemies = []
        self.death_markers = []
        self.item_manager = ItemManager()
        self.particle_manager = ParticleManager()
        self.sound_manager = get_sound_manager()
        self.tutorial = None
        self.game_start_time = None
        self.total_playtime = 0
        self.show_death_message = False
        self.death_message_timer = 0.0
        self.alive_count = 0

    def init_new_game(self, sw, sh):
        self.world_map = NaturalWorldGenerator.generate_natural_map()
        self.player = Player(MAP_WIDTH * TILE_SIZE // 2, MAP_HEIGHT * TILE_SIZE // 2)
        self.camera = Camera(sw, sh)
        self.game_start_time = time.time()
        self.total_playtime = 0
        self.death_markers = []
        self.alive_count = ENEMY_COUNT

        self.enemies = []
        tiers = [1] * (ENEMY_COUNT * 2 // 3) + [2] * (ENEMY_COUNT // 4) + [3] * max(1, ENEMY_COUNT // 6)
        random.shuffle(tiers)

        for tier in tiers:
            for _ in range(100):
                x = random.randint(0, MAP_WIDTH - 1) * TILE_SIZE
                y = random.randint(0, MAP_HEIGHT - 1) * TILE_SIZE
                if abs(x - self.player.x) > TILE_SIZE * 15 or abs(y - self.player.y) > TILE_SIZE * 15:
                    tx, ty = int(x // TILE_SIZE), int(y // TILE_SIZE)
                    from .tiletype import TileType
                    if 0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT and self.world_map[ty][tx] not in (TileType.WATER, TileType.WALL):
                        self.enemies.append(Enemy(x, y, tier))
                        break

        self._spawn_world_loot()
        self.alive_count = len(self.enemies) + 1
        return True

    def _spawn_world_loot(self):
        from .tiletype import TileType
        from core.items import create_items
        items = create_items()
        loot_items = list(items.values())

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.world_map[y][x] == TileType.LOOT_SPOT:
                    item = random.choice(loot_items)
                    wx = x * TILE_SIZE + TILE_SIZE // 2
                    wy = y * TILE_SIZE + TILE_SIZE // 2
                    self.item_manager.drop_item(wx, wy, item, 1)

    def load_game_data(self, game_data, sw, sh):
        self.world_map = game_data["world_map"]
        self.player = Player(game_data["player"]["x"], game_data["player"]["y"])
        self.player.health = game_data["player"]["health"]
        self.player.inventory = game_data["player"]["inventory"]
        self.camera = Camera(sw, sh)
        self.enemies = []
        for ed in game_data.get("enemies", []):
            e = Enemy(ed["x"], ed["y"], ed.get("tier", 1))
            e.health = ed["health"]
            self.enemies.append(e)
        self.death_markers = []
        self.total_playtime = game_data.get("playtime", 0)
        self.game_start_time = time.time()
        self.alive_count = len(self.enemies) + 1

    def update(self, keys, mouse_buttons, mouse_pos, dt, controls, camera, items):
        if not self.player:
            return

        dx, dy = self.player.update(keys, dt, controls)
        if dx != 0 or dy != 0:
            self.player.move(dx, dy, dt, self.world_map)
            if hasattr(self, 'particle_manager'):
                self.particle_manager.emit_dust(self.player.x + 16, self.player.y + 28)

        if hasattr(self, 'particle_manager'):
            self.particle_manager.update(dt)

        self.item_manager.update(dt, self.world_map)

        picked = self.item_manager.try_pickup(self.player.x, self.player.y, self.player.inventory)
        if picked:
            self.sound_manager.play('pickup')
            self.player.apply_armor_bonus()

        if self.player.health <= 0:
            self.handle_player_death()

        if mouse_buttons[0]:
            self.handle_mouse_click(mouse_pos, items)

        dead = []
        for enemy in self.enemies:
            if enemy.is_dead():
                dead.append(enemy)
            else:
                enemy.update(self.player, self.world_map, dt)

        for enemy in dead:
            self._handle_enemy_death(enemy, items)
            self.enemies.remove(enemy)
            self.alive_count = max(1, self.alive_count - 1)

        self._respawn_enemies_if_needed()
        self.camera.follow_player(self.player)

        if self.show_death_message:
            self.death_message_timer -= dt
            if self.death_message_timer <= 0:
                self.show_death_message = False

    def _handle_enemy_death(self, enemy, items):
        drops = enemy.get_loot(items)
        for item, qty in drops:
            for _ in range(qty):
                ox = random.randint(-16, 16)
                oy = random.randint(-16, 16)
                self.item_manager.drop_item(enemy.x + ox, enemy.y + oy, item, 1)
        self.player.xp += enemy.XP_REWARD
        self.sound_manager.play('hit')
        self.player.kills += 1

    def _respawn_enemies_if_needed(self):
        pass

    def handle_player_death(self):
        if self.player.health > 0:
            return
        if hasattr(self, 'particle_manager'):
            self.particle_manager.emit_death_effect(self.player.x + 16, self.player.y + 16)
        self.sound_manager.play('death')

        marker = DeathMarker(self.player.x, self.player.y, self.player.inventory)
        self.death_markers.append(marker)

        self.player.x = MAP_WIDTH * TILE_SIZE // 2
        self.player.y = MAP_HEIGHT * TILE_SIZE // 2
        self.player.health = self.player.max_health

        from ui.inventory import Inventory
        self.player.inventory = Inventory(24)
        self.player.apply_armor_bonus()

        self.show_death_message = True
        self.death_message_timer = 4.0

    def handle_mouse_click(self, mouse_pos, items):
        current_time = time.time()

        for i, marker in enumerate(self.death_markers):
            if marker.can_pickup(self.player.x, self.player.y):
                world_x = mouse_pos[0] + self.camera.x
                world_y = mouse_pos[1] + self.camera.y
                dist = ((world_x - marker.x)**2 + (world_y - marker.y)**2)**0.5
                if dist <= TILE_SIZE:
                    self.player.inventory = marker.inventory
                    self.player.apply_armor_bonus()
                    self.death_markers.pop(i)
                    return

        hit, damage = self.player.attack_enemies(
            self.enemies, mouse_pos, self.camera.x, self.camera.y, current_time
        )
        if hit:
            if hasattr(self, 'particle_manager'):
                self.particle_manager.emit_damage_flash(hit.x + 16, hit.y + 16)
            self.sound_manager.play('hit')

    def get_playtime(self):
        if self.game_start_time:
            total = self.total_playtime + (time.time() - self.game_start_time)
        else:
            total = self.total_playtime
        h = int(total // 3600)
        m = int((total % 3600) // 60)
        s = int(total % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def get_save_data(self):
        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "playtime": self.get_playtime(),
            "level_name": "Battle Royale",
            "world_map": self.world_map,
            "player": {
                "x": self.player.x, "y": self.player.y,
                "health": self.player.health,
                "inventory": {"slots": self.player.inventory.slots},
            },
            "enemies": [{"x": e.x, "y": e.y, "health": e.health, "tier": e.tier} for e in self.enemies],
            "death_markers": [{"x": m.x, "y": m.y, "inventory": m.inventory} for m in self.death_markers],
        }
