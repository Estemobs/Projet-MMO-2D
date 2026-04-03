"""
Gestionnaire de gameplay pour le jeu MMO 2D
"""

import time
import random
from .player import Player
from .enemy import Enemy
from .world import WorldGenerator
from .camera import Camera
from .item_system import ItemManager
from .constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, ENEMY_COUNT

class DeathMarker:
    """Marqueur d'inventaire déposé à la mort"""
    def __init__(self, x, y, inventory):
        self.x = x
        self.y = y
        self.inventory = inventory
        self.timestamp = time.time()
    
    def can_pickup(self, player_x, player_y):
        """Vérifie si le joueur peut ramasser l'inventaire"""
        distance = ((player_x - self.x)**2 + (player_y - self.y)**2) ** 0.5
        return distance <= TILE_SIZE * 2

class GameplayManager:
    def __init__(self):
        self.world_map = None
        self.player = None
        self.camera = None
        self.enemies = []
        self.death_markers = []
        self.item_manager = ItemManager()  # Nouveau système d'items
        
        # Temps de jeu
        self.game_start_time = None
        self.total_playtime = 0
        
        # Messages
        self.show_save_message = False
        self.save_message_timer = 0.0
        self.show_death_message = False
        self.death_message_timer = 0.0
    
    def init_new_game(self, screen_width, screen_height):
        """Initialise une nouvelle partie"""
        self.world_map = WorldGenerator.generate_map()
        self.player = Player(MAP_WIDTH * TILE_SIZE // 2, MAP_HEIGHT * TILE_SIZE // 2)
        self.camera = Camera(screen_width, screen_height)
        
        # Initialiser le temps de jeu
        self.game_start_time = time.time()
        self.total_playtime = 0
        
        # Générer quelques ennemis
        self.enemies = []
        for _ in range(ENEMY_COUNT):
            while True:
                x = random.randint(0, MAP_WIDTH - 1) * TILE_SIZE
                y = random.randint(0, MAP_HEIGHT - 1) * TILE_SIZE
                # S'assurer que l'ennemi n'apparaît pas trop près du joueur
                if abs(x - self.player.x) > TILE_SIZE * 10 or abs(y - self.player.y) > TILE_SIZE * 10:
                    self.enemies.append(Enemy(x, y))
                    break
        
        print(f"🎮 Nouvelle partie initialisée avec {len(self.enemies)} ennemis")
        return True
    
    def load_game_data(self, game_data, screen_width, screen_height):
        """Charge les données d'une partie sauvegardée"""
        # Restaurer la carte du monde
        self.world_map = game_data["world_map"]
        
        # Restaurer le joueur
        self.player = Player(game_data["player"]["x"], game_data["player"]["y"])
        self.player.health = game_data["player"]["health"]
        self.player.hunger = game_data["player"].get("hunger", 100)
        self.player.level = game_data["player"].get("level", 1)
        self.player.xp = game_data["player"].get("xp", 0)
        self.player.max_health = Player.max_health_for_level(self.player.level)
        self.player.inventory = game_data["player"]["inventory"]
        
        # Restaurer la caméra
        self.camera = Camera(screen_width, screen_height)
        
        # Restaurer les ennemis
        self.enemies = []
        for enemy_data in game_data["enemies"]:
            enemy = Enemy(enemy_data["x"], enemy_data["y"])
            enemy.health = enemy_data["health"]
            self.enemies.append(enemy)
        
        # Restaurer les marqueurs de mort si ils existent
        self.death_markers = []
        if "death_markers" in game_data:
            for marker_data in game_data["death_markers"]:
                marker = DeathMarker(
                    marker_data["x"], 
                    marker_data["y"], 
                    marker_data["inventory"]
                )
                self.death_markers.append(marker)
        
        # Restaurer le temps de jeu
        self.total_playtime = game_data.get("playtime", 0)
        self.game_start_time = time.time()
        
        print(f"✅ Partie chargée - Temps de jeu: {self.get_playtime()}")
    
    def update(self, keys, mouse_buttons, mouse_pos, dt, controls, camera, items):
        """Met à jour le gameplay"""
        if not self.player:
            return
        
        # Mise à jour du joueur
        dx, dy = self.player.update(keys, dt, controls)
        
        # Appliquer le mouvement au joueur
        if dx != 0 or dy != 0:
            self.player.move(dx, dy, dt, self.world_map)
        
        # Mise à jour du système d'items
        self.item_manager.update(dt, self.world_map)
        
        # Ramassage automatique des items proches
        picked_items = self.item_manager.try_pickup(self.player.x, self.player.y, self.player.inventory)
        if picked_items:
            print(f"🎒 Ramassé: {', '.join(picked_items)}")
        
        # Vérifier si le joueur est mort
        if self.player.health <= 0:
            self.handle_player_death()
        
        # Gestion des clics de souris (un seul appel par clic)
        if mouse_buttons[0]:
            self.handle_mouse_click(mouse_pos, items)
        
        # Mise à jour des ennemis et suppression des morts
        dead_enemies = []
        for enemy in self.enemies:
            if enemy.is_dead():
                dead_enemies.append(enemy)
            else:
                enemy.update(self.player, self.world_map, dt)
        
        for enemy in dead_enemies:
            self._handle_enemy_death(enemy, items)
            self.enemies.remove(enemy)
        
        # Respawn des ennemis si le nombre tombe trop bas
        self._respawn_enemies_if_needed()
        
        # Mise à jour de la caméra
        self.camera.follow_player(self.player)
        
        # Gestion des timers de messages
        if self.show_save_message:
            self.save_message_timer -= dt
            if self.save_message_timer <= 0:
                self.show_save_message = False
        
        if self.show_death_message:
            self.death_message_timer -= dt
            if self.death_message_timer <= 0:
                self.show_death_message = False
    
    def _handle_enemy_death(self, enemy, items):
        """Handles loot drops and XP when an enemy dies."""
        drops = enemy.get_loot(items)
        for item, qty in drops:
            for _ in range(qty):
                import random as _rng
                ox = _rng.randint(-16, 16)
                oy = _rng.randint(-16, 16)
                self.item_manager.drop_item(enemy.x + ox, enemy.y + oy, item, 1)
        self.player.xp += enemy.XP_REWARD
        self.player._check_level_up()
        print(f"☠️ Ennemi éliminé ! +{enemy.XP_REWARD} XP")

    def _respawn_enemies_if_needed(self):
        """Spawns new enemies when the count is below the minimum."""
        import random as _rng
        min_enemies = max(3, ENEMY_COUNT // 2)
        while len(self.enemies) < min_enemies:
            for _ in range(100):  # max attempts
                x = _rng.randint(0, MAP_WIDTH - 1) * TILE_SIZE
                y = _rng.randint(0, MAP_HEIGHT - 1) * TILE_SIZE
                dist_to_player = ((x - self.player.x) ** 2 + (y - self.player.y) ** 2) ** 0.5
                tile_x = int(x // TILE_SIZE)
                tile_y = int(y // TILE_SIZE)
                from .tiletype import TileType
                if (dist_to_player > TILE_SIZE * 15 and
                        self.world_map[tile_y][tile_x] == TileType.GRASS):
                    self.enemies.append(Enemy(x, y))
                    break

    def handle_player_death(self):
        """Gère la mort du joueur"""
        if self.player.health > 0:
            return  # Le joueur n'est pas mort
        
        # Créer un marqueur de mort avec l'inventaire
        marker = DeathMarker(self.player.x, self.player.y, self.player.inventory)
        self.death_markers.append(marker)
        
        # Respawn du joueur
        self.player.x = MAP_WIDTH * TILE_SIZE // 2
        self.player.y = MAP_HEIGHT * TILE_SIZE // 2
        self.player.health = self.player.max_health
        self.player.hunger = self.player.max_hunger
        
        # Vider l'inventaire du joueur
        from ui.inventory import Inventory
        self.player.inventory = Inventory(36)
        
        # Afficher un message
        self.show_death_message = True
        self.death_message_timer = 5.0
        
        print("💀 Vous êtes mort! Votre inventaire a été déposé.")
        print("🏃 Vous avez respawné au centre de la carte.")
    
    def handle_mouse_click(self, mouse_pos, items):
        """Gère les clics de souris (priorité: marqueurs de mort > attaque > construction/récolte)"""
        import time as _time
        current_time = _time.time()

        # 1. Vérifier les clics sur les marqueurs de mort
        for i, marker in enumerate(self.death_markers):
            if marker.can_pickup(self.player.x, self.player.y):
                world_x = mouse_pos[0] + self.camera.x
                world_y = mouse_pos[1] + self.camera.y
                
                marker_distance = ((world_x - marker.x)**2 + (world_y - marker.y)**2) ** 0.5
                if marker_distance <= TILE_SIZE:
                    self.player.inventory = marker.inventory
                    self.death_markers.pop(i)
                    print("✅ Inventaire récupéré!")
                    return

        # 2. Mode construction
        if self.player.build_mode:
            self.player.build_structure(self.world_map, mouse_pos, self.camera.x, self.camera.y)
            return

        # 3. Attaque d'ennemi (priorité sur la récolte)
        hit_enemy, damage = self.player.attack_enemies(
            self.enemies, mouse_pos, self.camera.x, self.camera.y, current_time
        )
        if hit_enemy is not None:
            return  # attack was performed, don't harvest

        # 4. Récolte de ressources
        self.player.harvest_resource(
            self.world_map, mouse_pos, self.camera.x, self.camera.y,
            items, self.item_manager
        )
    
    def get_playtime(self):
        """Retourne le temps de jeu actuel formaté"""
        if self.game_start_time:
            current_session = time.time() - self.game_start_time
            total_time = self.total_playtime + current_session
        else:
            total_time = self.total_playtime
        
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        seconds = int(total_time % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def get_save_data(self):
        """Retourne les données à sauvegarder"""
        save_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "playtime": self.get_playtime(),
            "level_name": "Monde généré",
            "world_map": self.world_map,
            "player": {
                "x": self.player.x,
                "y": self.player.y,
                "health": self.player.health,
                "hunger": self.player.hunger,
                "inventory": {
                    "slots": self.player.inventory.slots
                }
            },
            "enemies": [
                {
                    "x": enemy.x,
                    "y": enemy.y,
                    "health": enemy.health
                }
                for enemy in self.enemies
            ],
            "death_markers": [
                {
                    "x": marker.x,
                    "y": marker.y,
                    "inventory": marker.inventory
                }
                for marker in self.death_markers
            ]
        }
        return save_data
