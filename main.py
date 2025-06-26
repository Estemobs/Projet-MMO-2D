import pygame
import random
import numpy as np
from enum import Enum
import math

# Initialisation de Pygame
pygame.init()

# Constantes du jeu
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
TILE_SIZE = 32
MAP_WIDTH = 100
MAP_HEIGHT = 100

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BROWN = (101, 67, 33)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

class TileType(Enum):
    GRASS = 0
    TREE = 1
    STONE = 2
    IRON_ORE = 3
    WALL = 4  # Nouvelle structure constructible
    FOUNDATION = 5  # Base constructible

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 100  # pixels par seconde
        self.health = 100
        self.max_health = 100
        self.inventory = {
            'wood': 0,
            'stone': 0,
            'iron': 0
        }
        self.faction = "player"
        self.build_mode = False
        self.selected_building = "foundation"
        
    def move(self, dx, dy, dt, world_map):
        # Calculer la nouvelle position
        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt
        
        # Vérifier les limites de la carte
        if 0 <= new_x < MAP_WIDTH * TILE_SIZE and 0 <= new_y < MAP_HEIGHT * TILE_SIZE:
            # Vérifier s'il n'y a pas d'obstacle
            tile_x = int(new_x // TILE_SIZE)
            tile_y = int(new_y // TILE_SIZE)
            
            if world_map[tile_y][tile_x] == TileType.GRASS:
                self.x = new_x
                self.y = new_y
    
    def harvest_resource(self, world_map, mouse_pos, camera_x, camera_y):
        # Convertir la position de la souris en coordonnées du monde
        world_x = mouse_pos[0] + camera_x
        world_y = mouse_pos[1] + camera_y
        
        tile_x = int(world_x // TILE_SIZE)
        tile_y = int(world_y // TILE_SIZE)
        
        # Vérifier si le joueur est assez proche de la ressource
        player_tile_x = int(self.x // TILE_SIZE)
        player_tile_y = int(self.y // TILE_SIZE)
        
        distance = math.sqrt((tile_x - player_tile_x)**2 + (tile_y - player_tile_y)**2)
        
        if distance <= 2:  # Portée de récolte
            if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
                tile_type = world_map[tile_y][tile_x]
                
                if tile_type == TileType.TREE:
                    self.inventory['wood'] += 1
                    world_map[tile_y][tile_x] = TileType.GRASS
                    return True
                elif tile_type == TileType.STONE:
                    self.inventory['stone'] += 1
                    world_map[tile_y][tile_x] = TileType.GRASS
                    return True
                elif tile_type == TileType.IRON_ORE:
                    self.inventory['iron'] += 1
                    world_map[tile_y][tile_x] = TileType.GRASS
                    return True
        
        return False
    
    def build_structure(self, world_map, mouse_pos, camera_x, camera_y):
        # Convertir la position de la souris en coordonnées du monde
        world_x = mouse_pos[0] + camera_x
        world_y = mouse_pos[1] + camera_y
        
        tile_x = int(world_x // TILE_SIZE)
        tile_y = int(world_y // TILE_SIZE)
        
        # Vérifier si le joueur est assez proche pour construire
        player_tile_x = int(self.x // TILE_SIZE)
        player_tile_y = int(self.y // TILE_SIZE)
        
        distance = math.sqrt((tile_x - player_tile_x)**2 + (tile_y - player_tile_y)**2)
        
        if distance <= 3:  # Portée de construction
            if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
                if world_map[tile_y][tile_x] == TileType.GRASS:
                    # Coûts de construction
                    building_costs = {
                        "foundation": {"wood": 2, "stone": 1},
                        "wall": {"wood": 1, "stone": 2}
                    }
                    
                    if self.selected_building in building_costs:
                        cost = building_costs[self.selected_building]
                        
                        # Vérifier si le joueur a assez de ressources
                        can_build = all(self.inventory[resource] >= amount 
                                      for resource, amount in cost.items())
                        
                        if can_build:
                            # Déduire les ressources
                            for resource, amount in cost.items():
                                self.inventory[resource] -= amount
                            
                            # Placer la structure
                            if self.selected_building == "foundation":
                                world_map[tile_y][tile_x] = TileType.FOUNDATION
                            elif self.selected_building == "wall":
                                world_map[tile_y][tile_x] = TileType.WALL
                            
                            return True
        
        return False

class WorldGenerator:
    @staticmethod
    def generate_map():
        # Créer une carte remplie d'herbe
        world_map = [[TileType.GRASS for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        
        # Ajouter des arbres (15% de la carte)
        for _ in range(int(MAP_WIDTH * MAP_HEIGHT * 0.15)):
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            world_map[y][x] = TileType.TREE
        
        # Ajouter des pierres (8% de la carte)
        for _ in range(int(MAP_WIDTH * MAP_HEIGHT * 0.08)):
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            world_map[y][x] = TileType.STONE
        
        # Ajouter des minerais de fer (3% de la carte)
        for _ in range(int(MAP_WIDTH * MAP_HEIGHT * 0.03)):
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            world_map[y][x] = TileType.IRON_ORE
        
        return world_map

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def update(self, player_x, player_y):
        # Centrer la caméra sur le joueur
        self.x = player_x - WINDOW_WIDTH // 2
        self.y = player_y - WINDOW_HEIGHT // 2
        
        # Limiter la caméra aux bordures de la carte
        self.x = max(0, min(self.x, MAP_WIDTH * TILE_SIZE - WINDOW_WIDTH))
        self.y = max(0, min(self.y, MAP_HEIGHT * TILE_SIZE - WINDOW_HEIGHT))

class HUD:
    def __init__(self, font):
        self.font = font
    
    def draw(self, screen, player):
        # Fond semi-transparent pour le HUD
        hud_surface = pygame.Surface((WINDOW_WIDTH, 100))
        hud_surface.set_alpha(180)
        hud_surface.fill(BLACK)
        screen.blit(hud_surface, (0, 0))
        
        # Afficher la santé
        health_text = self.font.render(f"Santé: {player.health}/{player.max_health}", True, WHITE)
        screen.blit(health_text, (10, 10))
        
        # Barre de santé
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = player.health / player.max_health
        
        pygame.draw.rect(screen, RED, (10, 35, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (10, 35, health_bar_width * health_ratio, health_bar_height))
        pygame.draw.rect(screen, WHITE, (10, 35, health_bar_width, health_bar_height), 2)
        
        # Afficher l'inventaire
        inventory_y = 60
        wood_text = self.font.render(f"Bois: {player.inventory['wood']}", True, WHITE)
        stone_text = self.font.render(f"Pierre: {player.inventory['stone']}", True, WHITE)
        iron_text = self.font.render(f"Fer: {player.inventory['iron']}", True, WHITE)
        
        screen.blit(wood_text, (10, inventory_y))
        screen.blit(stone_text, (120, inventory_y))
        screen.blit(iron_text, (250, inventory_y))

class Building:
    def __init__(self, x, y, building_type, resources_needed):
        self.x = x
        self.y = y
        self.building_type = building_type
        self.resources_needed = resources_needed
        self.health = 100
        self.max_health = 100

class Enemy:
    def __init__(self, x, y, faction="hostile"):
        self.x = x
        self.y = y
        self.health = 50
        self.max_health = 50
        self.speed = 50
        self.damage = 10
        self.faction = faction
        self.last_attack_time = 0
        self.attack_cooldown = 1.0  # 1 seconde entre les attaques
        self.detection_range = 3  # tiles de portée de détection
    
    def move_towards_player(self, player_x, player_y, dt, world_map):
        # Calculer la direction vers le joueur
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normaliser la direction
            dx /= distance
            dy /= distance
            
            # Calculer la nouvelle position
            new_x = self.x + dx * self.speed * dt
            new_y = self.y + dy * self.speed * dt
            
            # Vérifier les limites et obstacles
            if 0 <= new_x < MAP_WIDTH * TILE_SIZE and 0 <= new_y < MAP_HEIGHT * TILE_SIZE:
                tile_x = int(new_x // TILE_SIZE)
                tile_y = int(new_y // TILE_SIZE)
                
                if world_map[tile_y][tile_x] in [TileType.GRASS, TileType.FOUNDATION]:
                    self.x = new_x
                    self.y = new_y
    
    def attack_player(self, player, current_time):
        if current_time - self.last_attack_time >= self.attack_cooldown:
            player.health -= self.damage
            self.last_attack_time = current_time
            return True
        return False

class Faction:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.members = []
        self.enemies = []
        self.allies = []

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("MMO 2D - Jeu de survie")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        # Initialiser les composants du jeu
        self.world_map = WorldGenerator.generate_map()
        self.player = Player(MAP_WIDTH * TILE_SIZE // 2, MAP_HEIGHT * TILE_SIZE // 2)
        self.camera = Camera()
        self.hud = HUD(self.font)
        
        # Générer quelques ennemis
        self.enemies = []
        for _ in range(5):
            # Placer les ennemis loin du joueur
            while True:
                enemy_x = random.randint(0, MAP_WIDTH - 1) * TILE_SIZE
                enemy_y = random.randint(0, MAP_HEIGHT - 1) * TILE_SIZE
                
                # Vérifier que l'ennemi est sur de l'herbe et loin du joueur
                tile_x = int(enemy_x // TILE_SIZE)
                tile_y = int(enemy_y // TILE_SIZE)
                distance_from_player = math.sqrt((enemy_x - self.player.x)**2 + (enemy_y - self.player.y)**2)
                
                if (self.world_map[tile_y][tile_x] == TileType.GRASS and 
                    distance_from_player > 200):
                    self.enemies.append(Enemy(enemy_x, enemy_y))
                    break
        
        self.running = True
    
    def get_tile_color(self, tile_type):
        color_map = {
            TileType.GRASS: GREEN,
            TileType.TREE: BROWN,
            TileType.STONE: GRAY,
            TileType.IRON_ORE: DARK_GRAY,
            TileType.WALL: ORANGE,
            TileType.FOUNDATION: YELLOW
        }
        return color_map[tile_type]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    mouse_pos = pygame.mouse.get_pos()
                    if self.player.build_mode:
                        if self.player.build_structure(self.world_map, mouse_pos, self.camera.x, self.camera.y):
                            print(f"Structure {self.player.selected_building} construite!")
                    else:
                        if self.player.harvest_resource(self.world_map, mouse_pos, self.camera.x, self.camera.y):
                            print("Ressource récoltée!")
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.player.build_mode = not self.player.build_mode
                    print(f"Mode construction: {'Activé' if self.player.build_mode else 'Désactivé'}")
                elif event.key == pygame.K_1:
                    self.player.selected_building = "foundation"
                    print("Structure sélectionnée: Fondation")
                elif event.key == pygame.K_2:
                    self.player.selected_building = "wall"
                    print("Structure sélectionnée: Mur")
    
    def update(self, dt):
        # Gestion des inputs du clavier
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        
        # Normaliser le mouvement diagonal
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707
        
        # Déplacer le joueur
        self.player.move(dx, dy, dt, self.world_map)
        
        # Mettre à jour la caméra
        self.camera.update(self.player.x, self.player.y)
        
        # Mettre à jour les ennemis
        current_time = pygame.time.get_ticks() / 1000.0
        for enemy in self.enemies:
            # Calculer la distance au joueur
            distance_to_player = math.sqrt((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)
            
            if distance_to_player <= enemy.detection_range * TILE_SIZE:
                # Si assez proche pour attaquer
                if distance_to_player <= TILE_SIZE:
                    if enemy.attack_player(self.player, current_time):
                        print(f"Le joueur a subi {enemy.damage} dégâts!")
                        if self.player.health <= 0:
                            print("Game Over!")
                            self.running = False
                else:
                    # Se déplacer vers le joueur
                    enemy.move_towards_player(self.player.x, self.player.y, dt, self.world_map)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Calculer les tiles visibles
        start_x = max(0, int(self.camera.x // TILE_SIZE))
        end_x = min(MAP_WIDTH, int((self.camera.x + WINDOW_WIDTH) // TILE_SIZE) + 1)
        start_y = max(0, int(self.camera.y // TILE_SIZE))
        end_y = min(MAP_HEIGHT, int((self.camera.y + WINDOW_HEIGHT) // TILE_SIZE) + 1)
        
        # Dessiner les tiles visibles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile_type = self.world_map[y][x]
                color = self.get_tile_color(tile_type)
                
                screen_x = x * TILE_SIZE - self.camera.x
                screen_y = y * TILE_SIZE - self.camera.y
                
                pygame.draw.rect(self.screen, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                
                # Ajouter des bordures pour mieux voir les tiles
                pygame.draw.rect(self.screen, BLACK, (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 1)
        
        # Dessiner le joueur
        player_screen_x = self.player.x - self.camera.x
        player_screen_y = self.player.y - self.camera.y
        
        pygame.draw.circle(self.screen, BLUE, 
                         (int(player_screen_x + TILE_SIZE // 2), 
                          int(player_screen_y + TILE_SIZE // 2)), 
                         TILE_SIZE // 3)
        
        # Dessiner les ennemis
        for enemy in self.enemies:
            enemy_screen_x = enemy.x - self.camera.x
            enemy_screen_y = enemy.y - self.camera.y
            
            # Ne dessiner que les ennemis visibles
            if (-TILE_SIZE <= enemy_screen_x <= WINDOW_WIDTH and 
                -TILE_SIZE <= enemy_screen_y <= WINDOW_HEIGHT):
                pygame.draw.circle(self.screen, RED,
                                 (int(enemy_screen_x + TILE_SIZE // 2),
                                  int(enemy_screen_y + TILE_SIZE // 2)),
                                 TILE_SIZE // 4)
        
        # Dessiner le HUD
        self.hud.draw(self.screen, self.player)
        
        # Instructions
        instructions = [
            "WASD ou flèches: Se déplacer",
            "Clic gauche: Récolter les ressources ou construire",
            "B: Activer/désactiver le mode construction",
            "1: Sélectionner fondation, 2: Sélectionner mur"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, WHITE)
            self.screen.blit(text, (10, WINDOW_HEIGHT - 80 + i * 25))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Delta time en secondes
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()