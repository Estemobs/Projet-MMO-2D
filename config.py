# Configuration du jeu MMO 2D

# Paramètres de la fenêtre
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
WINDOW_TITLE = "MMO 2D - Jeu de survie"

# Paramètres de la carte
TILE_SIZE = 32
MAP_WIDTH = 100
MAP_HEIGHT = 100

# Paramètres du joueur
PLAYER_SPEED = 100  # pixels par seconde
PLAYER_MAX_HEALTH = 100
PLAYER_HARVEST_RANGE = 2  # cases
PLAYER_BUILD_RANGE = 3    # cases

# Paramètres des ennemis
ENEMY_HEALTH = 50
ENEMY_SPEED = 50
ENEMY_DAMAGE = 10
ENEMY_DETECTION_RANGE = 3  # cases
ENEMY_ATTACK_COOLDOWN = 1.0  # secondes
ENEMY_COUNT = 5

# Paramètres de génération du monde
TREE_DENSITY = 0.15    # 15% de la carte
STONE_DENSITY = 0.08   # 8% de la carte
IRON_DENSITY = 0.03    # 3% de la carte

# Coûts de construction
BUILDING_COSTS = {
    "foundation": {"wood": 2, "stone": 1},
    "wall": {"wood": 1, "stone": 2}
}

# Paramètres de rendu
TARGET_FPS = 60
HUD_HEIGHT = 100
HUD_ALPHA = 180

# Couleurs (R, G, B)
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GREEN": (34, 139, 34),     # Herbe
    "BROWN": (101, 67, 33),     # Arbres
    "GRAY": (128, 128, 128),    # Pierres
    "DARK_GRAY": (64, 64, 64),  # Minerai de fer
    "RED": (255, 0, 0),         # Ennemis
    "BLUE": (0, 0, 255),        # Joueur
    "YELLOW": (255, 255, 0),    # Fondations
    "ORANGE": (255, 165, 0),    # Murs
    "PURPLE": (128, 0, 128)     # Réservé
}
