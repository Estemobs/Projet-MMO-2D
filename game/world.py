from .tiletype import TileType
from .constants import MAP_WIDTH, MAP_HEIGHT
import random
import math

class WorldGenerator:
    @staticmethod
    def generate_map():
        # Créer une carte remplie d'herbe
        world_map = [[TileType.GRASS for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        
        # Génération par clusters plus organique (comme Surviv.io)
        
        # Forêts en clusters (5% au lieu de 15%)
        WorldGenerator._generate_clusters(world_map, TileType.TREE, 8, 3, 7)
        
        # Zones rocheuses en clusters (3% au lieu de 8%)
        WorldGenerator._generate_clusters(world_map, TileType.STONE, 5, 2, 5)
        
        # Minerais en petits clusters
        WorldGenerator._generate_clusters(world_map, TileType.IRON_ORE, 3, 1, 3)
        WorldGenerator._generate_clusters(world_map, TileType.GOLD_ORE, 2, 1, 2)
        WorldGenerator._generate_clusters(world_map, TileType.DIAMOND_ORE, 1, 1, 2)
        WorldGenerator._generate_clusters(world_map, TileType.COAL_ORE, 2, 1, 3)
        
        # Arbres fruitiers dispersés
        WorldGenerator._generate_scattered(world_map, TileType.APPLE_TREE, 15)
        WorldGenerator._generate_scattered(world_map, TileType.BERRY_BUSH, 10)
        
        return world_map
    
    @staticmethod
    def _generate_clusters(world_map, tile_type, num_clusters, min_size, max_size):
        """Génère des clusters organiques de tiles"""
        for _ in range(num_clusters):
            # Point central du cluster
            center_x = random.randint(10, MAP_WIDTH - 10)
            center_y = random.randint(10, MAP_HEIGHT - 10)
            cluster_size = random.randint(min_size, max_size)
            
            # Générer un cluster organique
            for _ in range(cluster_size * cluster_size):
                # Distance aléatoire du centre (distribution normale)
                distance = random.gauss(0, cluster_size / 3)
                angle = random.uniform(0, 2 * math.pi)
                
                x = int(center_x + distance * math.cos(angle))
                y = int(center_y + distance * math.sin(angle))
                
                if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                    # Probabilité décroissante avec la distance
                    distance_factor = max(0, 1 - abs(distance) / cluster_size)
                    if random.random() < distance_factor * 0.7:
                        world_map[y][x] = tile_type
    
    @staticmethod
    def _generate_scattered(world_map, tile_type, count):
        """Génère des éléments dispersés aléatoirement"""
        for _ in range(count):
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            if world_map[y][x] == TileType.GRASS:  # Ne remplace que l'herbe
                world_map[y][x] = tile_type
            world_map[y][x] = TileType.APPLE_TREE
        
        # Ajouter des buissons de baies (0.5% de la carte)
        for _ in range(int(MAP_WIDTH * MAP_HEIGHT * 0.005)):
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            world_map[y][x] = TileType.BERRY_BUSH
        
        return world_map
