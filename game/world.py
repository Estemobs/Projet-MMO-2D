from .tiletype import TileType
from .constants import MAP_WIDTH, MAP_HEIGHT
from .natural_world import NaturalWorldGenerator
import random
import math

class WorldGenerator:
    @staticmethod
    def generate_map():
        """Génère une carte naturelle style Stardew Valley/Pokémon"""
        print("🌍 Génération d'un monde naturel...")
        return NaturalWorldGenerator.generate_natural_map()
    
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
