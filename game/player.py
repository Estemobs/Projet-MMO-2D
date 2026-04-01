import random
import os
import sys

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from ui.inventory import Inventory
from .constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE
from .tiletype import TileType

class DroppedInventory:
    """Représente un inventaire déposé au sol"""
    def __init__(self, x, y, inventory):
        self.x = x
        self.y = y
        self.inventory = inventory
        self.size = TILE_SIZE

class Player:
    # Damage values per weapon type
    WEAPON_DAMAGE = {
        "Épée en bois": 10,
        "Épée en fer": 20,
        "Épée en or": 25,
        "Épée en diamant": 40,
        "Pioche en bois": 7,
        "Pioche en fer": 12,
    }
    BARE_HANDS_DAMAGE = 5
    ATTACK_RANGE = TILE_SIZE * 1.5  # pixels
    ATTACK_COOLDOWN = 0.5  # seconds

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 100
        self.health = 100
        self.max_health = 100
        self.faction = "player"
        self.build_mode = False
        
        # Animation
        self.is_moving = False
        self.animation_time = 0
        self.animation_speed = 0.3  # Secondes entre les frames
        self.selected_building = "foundation"
        self.inventory = Inventory(36)
        self.hunger = 100
        self.max_hunger = 100

        # Combat
        self.last_attack_time = 0
        self.attack_feedback = None   # (text, timer) for HUD
        self.xp = 0
        self.level = 1

    def move(self, dx, dy, dt, world_map):
        # Déterminer si le joueur bouge
        self.is_moving = (dx != 0 or dy != 0)
        
        # Mettre à jour l'animation si en mouvement
        if self.is_moving:
            self.animation_time += dt
        else:
            self.animation_time = 0
        
        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt
        if 0 <= new_x < MAP_WIDTH * TILE_SIZE and 0 <= new_y < MAP_HEIGHT * TILE_SIZE:
            tile_x = int(new_x // TILE_SIZE)
            tile_y = int(new_y // TILE_SIZE)
            
            # Terrain praticable : herbe, terre, eau (avec vitesse réduite)
            # OBSTACLES SOLIDES : arbres, minerais, pierres, murs
            walkable_tiles = [TileType.GRASS, TileType.DIRT, TileType.WATER, TileType.FOUNDATION]
            solid_tiles = [
                TileType.TREE, TileType.APPLE_TREE, TileType.BERRY_BUSH,  # Végétation
                TileType.STONE, TileType.IRON_ORE, TileType.GOLD_ORE,    # Minerais
                TileType.DIAMOND_ORE, TileType.COAL_ORE,                 # Minerais
                TileType.WALL                                             # Structures
            ]
            
            current_tile = world_map[tile_y][tile_x]
            
            # Ne pas pouvoir marcher sur les obstacles solides
            if current_tile not in solid_tiles and current_tile in walkable_tiles:
                # Réduire la vitesse dans l'eau
                if current_tile == TileType.WATER:
                    speed_multiplier = 0.5
                else:
                    speed_multiplier = 1.0
                
                self.x = self.x + dx * self.speed * dt * speed_multiplier
                self.y = self.y + dy * self.speed * dt * speed_multiplier
    
    def get_current_sprite(self):
        """Retourne le nom du sprite actuel selon l'animation"""
        if not self.is_moving:
            return "player"
        
        # Alterner entre les sprites de marche
        cycle_time = self.animation_time % (self.animation_speed * 2)
        if cycle_time < self.animation_speed:
            return "player_walk1"
        else:
            return "player_walk2"

    def harvest_resource(self, world_map, mouse_pos, camera_x, camera_y, items, item_manager=None):
        """Récolte des ressources avec système de drop comme Surviv.io"""
        world_x = mouse_pos[0] + camera_x
        world_y = mouse_pos[1] + camera_y
        tile_x = int(world_x // TILE_SIZE)
        tile_y = int(world_y // TILE_SIZE)
        player_tile_x = int(self.x // TILE_SIZE)
        player_tile_y = int(self.y // TILE_SIZE)
        distance = ((tile_x - player_tile_x)**2 + (tile_y - player_tile_y)**2) ** 0.5
        
        if distance <= 2:
            if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
                tile_type = world_map[tile_y][tile_x]
                drop_x = tile_x * TILE_SIZE + TILE_SIZE // 2
                drop_y = tile_y * TILE_SIZE + TILE_SIZE // 2
                
                drops = []  # Liste des drops avec probabilités
                
                if tile_type == TileType.TREE:
                    drops.append((items["wood"], 1))  # Toujours du bois
                    # Chance de pommes
                    if random.random() < 0.3:  # 30% de chance
                        drops.append((items["apple"], random.randint(1, 2)))
                    
                elif tile_type == TileType.STONE:
                    drops.append((items["stone"], random.randint(1, 2)))
                    
                elif tile_type == TileType.IRON_ORE:
                    drops.append((items["iron_ore"], random.randint(1, 3)))
                    
                elif tile_type == TileType.GOLD_ORE:
                    drops.append((items["gold_ore"], random.randint(1, 2)))
                    
                elif tile_type == TileType.DIAMOND_ORE:
                    drops.append((items["diamond_ore"], 1))
                    # Bonus rare
                    if random.random() < 0.1:
                        drops.append((items["diamond_ore"], 1))
                    
                elif tile_type == TileType.COAL_ORE:
                    drops.append((items["coal"], random.randint(2, 4)))
                    
                elif tile_type == TileType.APPLE_TREE:
                    drops.append((items["wood"], 1))
                    drops.append((items["apple"], random.randint(2, 5)))
                    
                elif tile_type == TileType.BERRY_BUSH:
                    drops.append((items["berry"], random.randint(3, 6)))
                
                # Dropper les items avec le nouveau système (style Surviv.io)
                if drops and item_manager:
                    # Disperser chaque item individuellement pour plus d'effet
                    for item, quantity in drops:
                        for _ in range(quantity):
                            # Varier légèrement la position de drop
                            offset_x = random.randint(-16, 16)
                            offset_y = random.randint(-16, 16)
                            item_manager.drop_item(drop_x + offset_x, drop_y + offset_y, item, 1)
                    
                    world_map[tile_y][tile_x] = TileType.GRASS
                    return True
                elif drops and not item_manager:
                    # Fallback: ajouter directement à l'inventaire
                    for item, quantity in drops:
                        self.inventory.add_item(item, quantity)
                    world_map[tile_y][tile_x] = TileType.GRASS
                    return True
        
        return False

    def build_structure(self, world_map, mouse_pos, camera_x, camera_y):
        world_x = mouse_pos[0] + camera_x
        world_y = mouse_pos[1] + camera_y
        tile_x = int(world_x // TILE_SIZE)
        tile_y = int(world_y // TILE_SIZE)
        player_tile_x = int(self.x // TILE_SIZE)
        player_tile_y = int(self.y // TILE_SIZE)
        distance = ((tile_x - player_tile_x)**2 + (tile_y - player_tile_y)**2) ** 0.5
        if distance <= 3:
            if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
                if world_map[tile_y][tile_x] == TileType.GRASS:
                    building_costs = {
                        "foundation": {"wood": 2, "stone": 1},
                        "wall": {"wood": 1, "stone": 2}
                    }
                    if self.selected_building in building_costs:
                        cost = building_costs[self.selected_building]
                        can_build = all(self.inventory.has_item(resource, amount) for resource, amount in cost.items())
                        if can_build:
                            for resource, amount in cost.items():
                                self.inventory.remove_item(resource, amount)
                            if self.selected_building == "foundation":
                                world_map[tile_y][tile_x] = TileType.FOUNDATION
                            elif self.selected_building == "wall":
                                world_map[tile_y][tile_x] = TileType.WALL
                            return True
        return False

    def get_attack_damage(self):
        """Returns damage based on equipped weapon or held item."""
        for slot in self.inventory.slots:
            if slot and slot.item.type in ("weapon", "tool"):
                return self.WEAPON_DAMAGE.get(slot.item.name, self.BARE_HANDS_DAMAGE)
        return self.BARE_HANDS_DAMAGE

    def attack_enemies(self, enemies, mouse_pos, camera_x, camera_y, current_time):
        """
        Attempts to attack the closest enemy near the mouse click.
        Returns (damaged_enemy_or_None, damage_dealt).
        """
        world_x = mouse_pos[0] + camera_x
        world_y = mouse_pos[1] + camera_y

        if current_time - self.last_attack_time < self.ATTACK_COOLDOWN:
            return None, 0  # Still on cooldown

        closest_enemy = None
        closest_dist = self.ATTACK_RANGE

        for enemy in enemies:
            dist = ((enemy.x - world_x) ** 2 + (enemy.y - world_y) ** 2) ** 0.5
            if dist <= closest_dist:
                closest_dist = dist
                closest_enemy = enemy

        if closest_enemy is not None:
            damage = self.get_attack_damage()
            closest_enemy.health -= damage
            self.last_attack_time = current_time
            self.xp += max(1, damage // 2)
            self._check_level_up()
            self.attack_feedback = (f"-{damage}", 1.0)
            return closest_enemy, damage

        return None, 0

    @staticmethod
    def max_health_for_level(level):
        """Returns the maximum health for a given level."""
        return min(200, 100 + (level - 1) * 10)

    def _check_level_up(self):
        """Simple XP-based level-up."""
        xp_needed = self.level * 100
        if self.xp >= xp_needed:
            self.xp -= xp_needed
            self.level += 1
            self.max_health = self.max_health_for_level(self.level)
            self.health = self.max_health
            print(f"🎉 Niveau {self.level} atteint! Santé max: {self.max_health}")

    def eat_food(self, food_item, heal_amount):
        if self.inventory.has_item(food_item, 1):
            self.inventory.remove_item(food_item, 1)
            self.health = min(self.max_health, self.health + heal_amount)
            self.hunger = min(self.max_hunger, self.hunger + heal_amount // 2)
            return True
        return False

    def eat_best_food(self):
        """Eats the best available food item. Returns (item_name, heal) or None."""
        # Uses French display names since inventory.has_item checks by item.name
        food_priority = [
            ("Pain", 20),
            ("Viande", 15),
            ("Pomme", 10),
            ("Baie", 5),
        ]
        for food_name, heal in food_priority:
            if self.eat_food(food_name, heal):
                return food_name, heal
        return None

    def update(self, keys, dt, controls=None):
        """Met à jour l'état du joueur"""
        # Diminuer la faim au fil du temps (beaucoup plus lentement)
        self.hunger = max(0, self.hunger - 0.3 * dt)  # Encore plus lent
        
        # Si le joueur a faim, perdre de la santé (plus lentement)
        if self.hunger <= 0:
            self.health = max(0, self.health - 1.5 * dt)  # Réduit encore plus
        
        # Régénération naturelle si le joueur n'a pas faim
        elif self.hunger > 30 and self.health < self.max_health:
            self.health = min(self.max_health, self.health + 3 * dt)  # Un peu plus de régénération

        # Décrémenter le feedback d'attaque
        if self.attack_feedback:
            text, timer = self.attack_feedback
            timer -= dt
            if timer <= 0:
                self.attack_feedback = None
            else:
                self.attack_feedback = (text, timer)
        
        # Gestion du déplacement avec les contrôles configurés
        if controls is None:
            # Contrôles par défaut si aucun contrôle personnalisé n'est fourni
            import pygame
            controls = {
                "move_up": pygame.K_w,
                "move_down": pygame.K_s,
                "move_left": pygame.K_a,
                "move_right": pygame.K_d
            }
        
        dx = 0
        dy = 0
        
        if keys[controls["move_up"]]:
            dy -= 1
        if keys[controls["move_down"]]:
            dy += 1
        if keys[controls["move_left"]]:
            dx -= 1
        if keys[controls["move_right"]]:
            dx += 1
        
        # Normaliser le vecteur de déplacement si mouvement diagonal
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2)
            dy *= 0.707
            
        return dx, dy

    def handle_mouse_click(self, mouse_pos, world_map, camera_x, camera_y, items):
        """Gère les clics de souris du joueur"""
        if self.build_mode:
            # Mode construction
            return self.build_structure(world_map, mouse_pos, camera_x, camera_y)
        else:
            # Mode récolte
            self.harvest_resource(world_map, mouse_pos, camera_x, camera_y, items)
    
    def is_dead(self):
        """Vérifie si le joueur est mort"""
        return self.health <= 0
    
    def die(self):
        """Fait mourir le joueur et retourne son inventaire"""
        if self.health <= 0:
            # Sauvegarder l'inventaire à déposer
            dropped_inventory = DroppedInventory(self.x, self.y, self.inventory)
            
            # Respawn du joueur
            self.respawn()
            
            return dropped_inventory
        return None
    
    def respawn(self):
        """Fait respawn le joueur"""
        # Position de spawn (centre de la carte)
        self.x = MAP_WIDTH * TILE_SIZE // 2
        self.y = MAP_HEIGHT * TILE_SIZE // 2
        
        # Restaurer les stats
        self.health = self.max_health
        self.hunger = self.max_hunger
        
        # Nouvel inventaire vide
        self.inventory = Inventory(36)
        
        print("💀 Vous êtes mort ! Vous avez respawn au centre de la carte.")
        print("🎒 Votre inventaire a été déposé à l'endroit de votre mort.")
