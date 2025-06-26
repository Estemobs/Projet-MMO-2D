from .tiletype import TileType
from .constants import MAP_WIDTH, MAP_HEIGHT
import random

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
        
        # Ajouter des minerais d'or (1% de la carte)
        for _ in range(int(MAP_WIDTH * MAP_HEIGHT * 0.01)):
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            world_map[y][x] = TileType.GOLD_ORE
        
        # Ajouter des diamants (0.5% de la carte)
        for _ in range(int(MAP_WIDTH * MAP_HEIGHT * 0.005)):
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            world_map[y][x] = TileType.DIAMOND_ORE
        
        # Ajouter du charbon (2% de la carte)
        for _ in range(int(MAP_WIDTH * MAP_HEIGHT * 0.02)):
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            world_map[y][x] = TileType.COAL_ORE
        
        # Ajouter des arbres fruitiers (1% de la carte)
        for _ in range(int(MAP_WIDTH * MAP_HEIGHT * 0.01)):
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            world_map[y][x] = TileType.APPLE_TREE
        
        # Ajouter des buissons de baies (0.5% de la carte)
        for _ in range(int(MAP_WIDTH * MAP_HEIGHT * 0.005)):
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            world_map[y][x] = TileType.BERRY_BUSH
        
        return world_map
