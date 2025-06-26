from .tiletype import TileType
from .constants import MAP_WIDTH, MAP_HEIGHT
import random
import math

class NaturalWorldGenerator:
    """Générateur de monde naturel style Stardew Valley/Pokémon"""
    
    @staticmethod
    def generate_natural_map():
        """Génère une carte avec des biomes naturels"""
        # Initialiser avec de l'herbe de base
        world_map = [[TileType.GRASS for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        
        print("🌱 Génération d'un monde naturel...")
        
        # 1. Créer des biomes avec du bruit de Perlin
        NaturalWorldGenerator._generate_biomes(world_map)
        
        # 2. Ajouter des chemins naturels
        NaturalWorldGenerator._generate_natural_paths(world_map)
        
        # 3. Placer des plans d'eau
        NaturalWorldGenerator._generate_water_bodies(world_map)
        
        # 4. Ajouter de la végétation naturelle (beaucoup moins dense)
        NaturalWorldGenerator._add_natural_vegetation(world_map)
        
        # 5. Disperser des ressources de façon naturelle
        NaturalWorldGenerator._place_natural_resources(world_map)
        
        print("🎉 Monde naturel généré avec succès!")
        return world_map
    
    @staticmethod
    def _generate_biomes(world_map):
        """Génère des biomes naturels avec variation d'herbe"""
        # Créer des zones avec différents types d'herbe
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                # Utiliser une fonction de bruit simple pour varier l'herbe
                seed_value = (x * 12345 + y * 67890) % 1000
                random.seed(seed_value)
                
                # 80% herbe normale, 20% variations
                if random.random() < 0.8:
                    world_map[y][x] = TileType.GRASS
                else:
                    # Petit pourcentage de terre naturelle pour la variété
                    world_map[y][x] = TileType.DIRT if random.random() < 0.3 else TileType.GRASS
    
    @staticmethod
    def _generate_natural_paths(world_map):
        """Génère des chemins de terre naturels serpentant"""
        # Créer 2-3 chemins principaux qui serpentent
        num_paths = 2
        
        for _ in range(num_paths):
            # Point de départ aléatoire sur un bord
            if random.choice([True, False]):
                # Chemin horizontal
                start_x = 0
                start_y = random.randint(MAP_HEIGHT // 4, 3 * MAP_HEIGHT // 4)
                end_x = MAP_WIDTH - 1
                end_y = random.randint(MAP_HEIGHT // 4, 3 * MAP_HEIGHT // 4)
            else:
                # Chemin vertical
                start_x = random.randint(MAP_WIDTH // 4, 3 * MAP_WIDTH // 4)
                start_y = 0
                end_x = random.randint(MAP_WIDTH // 4, 3 * MAP_WIDTH // 4)
                end_y = MAP_HEIGHT - 1
            
            # Créer le chemin serpentant
            NaturalWorldGenerator._create_winding_path(world_map, start_x, start_y, end_x, end_y)
    
    @staticmethod
    def _create_winding_path(world_map, start_x, start_y, end_x, end_y):
        """Crée un chemin serpentant entre deux points"""
        steps = max(abs(end_x - start_x), abs(end_y - start_y))
        
        for i in range(steps + 1):
            progress = i / max(1, steps)
            
            # Position de base (ligne droite)
            base_x = start_x + (end_x - start_x) * progress
            base_y = start_y + (end_y - start_y) * progress
            
            # Ajouter de la sinuosité
            wave = math.sin(progress * math.pi * 4) * 8
            x = int(base_x + wave * math.cos(progress * math.pi * 2))
            y = int(base_y + wave * math.sin(progress * math.pi * 2))
            
            # Placer de la terre sur le chemin (largeur 2-3 cases)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                        if random.random() < 0.7:  # Pas 100% régulier
                            world_map[ny][nx] = TileType.DIRT
    
    @staticmethod
    def _generate_water_bodies(world_map):
        """Génère quelques plans d'eau naturels"""
        # 1-2 petits lacs
        for _ in range(random.randint(1, 2)):
            center_x = random.randint(20, MAP_WIDTH - 20)
            center_y = random.randint(20, MAP_HEIGHT - 20)
            lake_size = random.randint(5, 12)
            
            # Créer un lac de forme organique
            for dy in range(-lake_size, lake_size + 1):
                for dx in range(-lake_size, lake_size + 1):
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance <= lake_size:
                        x, y = center_x + dx, center_y + dy
                        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                            # Probabilité basée sur la distance du centre
                            prob = 1 - (distance / lake_size) ** 2
                            if random.random() < prob:
                                world_map[y][x] = TileType.WATER
        
        # Quelques rivières
        for _ in range(random.randint(0, 1)):
            start_x = random.randint(0, MAP_WIDTH - 1)
            start_y = 0
            NaturalWorldGenerator._create_river(world_map, start_x, start_y)
    
    @staticmethod
    def _create_river(world_map, start_x, start_y):
        """Crée une rivière serpentant vers le bas"""
        x, y = start_x, start_y
        
        while y < MAP_HEIGHT - 1:
            # Placer de l'eau
            if 0 <= x < MAP_WIDTH:
                world_map[y][x] = TileType.WATER
                # Elargir parfois la rivière
                if random.random() < 0.3:
                    for dx in [-1, 1]:
                        if 0 <= x + dx < MAP_WIDTH:
                            world_map[y][x + dx] = TileType.WATER
            
            # Avancer avec dérive
            y += 1
            x += random.randint(-1, 1)
            x = max(1, min(MAP_WIDTH - 2, x))  # Rester dans les limites
    
    @staticmethod
    def _add_natural_vegetation(world_map):
        """Ajoute de la végétation de manière naturelle (BEAUCOUP moins dense)"""
        # Forêts clairsemées (seulement 3-4 petites zones)
        for _ in range(random.randint(3, 4)):
            center_x = random.randint(15, MAP_WIDTH - 15)
            center_y = random.randint(15, MAP_HEIGHT - 15)
            forest_size = random.randint(8, 15)
            
            # Densité très faible dans les forêts
            for _ in range(forest_size * 2):  # Beaucoup moins d'arbres
                angle = random.uniform(0, 2 * math.pi)
                distance = random.gauss(0, forest_size / 2)
                
                x = int(center_x + distance * math.cos(angle))
                y = int(center_y + distance * math.sin(angle))
                
                if (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and 
                    world_map[y][x] == TileType.GRASS):
                    # Seulement 30% de chance de placer un arbre
                    if random.random() < 0.3:
                        tree_type = random.choice([TileType.TREE, TileType.TREE, TileType.APPLE_TREE])
                        world_map[y][x] = tree_type
        
        # Arbres isolés très rares
        for _ in range(random.randint(10, 20)):
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            if world_map[y][x] == TileType.GRASS:
                if random.random() < 0.5:  # 50% de chance seulement
                    world_map[y][x] = TileType.TREE
        
        # Buissons de baies très dispersés
        for _ in range(random.randint(5, 10)):
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            if world_map[y][x] == TileType.GRASS:
                world_map[y][x] = TileType.BERRY_BUSH
    
    @staticmethod
    def _place_natural_resources(world_map):
        """Place des ressources minérales de façon naturelle"""
        # Zones rocheuses rares
        for _ in range(random.randint(2, 4)):
            center_x = random.randint(10, MAP_WIDTH - 10)
            center_y = random.randint(10, MAP_HEIGHT - 10)
            
            # Petit amas de rochers
            for _ in range(random.randint(3, 8)):
                x = center_x + random.randint(-5, 5)
                y = center_y + random.randint(-5, 5)
                
                if (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and 
                    world_map[y][x] == TileType.GRASS):
                    world_map[y][x] = TileType.STONE
        
        # Minerais très rares et dispersés
        minerals = [
            (TileType.IRON_ORE, 8),
            (TileType.COAL_ORE, 6),
            (TileType.GOLD_ORE, 3),
            (TileType.DIAMOND_ORE, 1),
        ]
        
        for mineral_type, count in minerals:
            for _ in range(count):
                x = random.randint(0, MAP_WIDTH - 1)
                y = random.randint(0, MAP_HEIGHT - 1)
                if world_map[y][x] == TileType.GRASS:
                    world_map[y][x] = mineral_type
