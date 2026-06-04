# Constantes globales du jeu
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
TILE_SIZE = 32
MAP_WIDTH = 100
MAP_HEIGHT = 100

# Paramètres de jeu
ENEMY_COUNT = 20
TARGET_FPS = 60

# Système de scale adaptatif
REFERENCE_WIDTH = 1920
REFERENCE_HEIGHT = 1080
SCALE_FACTOR = 1.0
SCREEN_WIDTH = WINDOW_WIDTH
SCREEN_HEIGHT = WINDOW_HEIGHT


def update_scale(screen_width, screen_height):
    """Met à jour le scale factor selon la taille de l'écran."""
    global SCALE_FACTOR, SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH = screen_width
    SCREEN_HEIGHT = screen_height
    SCALE_FACTOR = min(screen_width / REFERENCE_WIDTH, screen_height / REFERENCE_HEIGHT)


def s(value):
    """Scale une valeur selon la taille de l'écran."""
    return int(value * SCALE_FACTOR)

# Palette de couleurs moderne
COLORS = {
    # Base
    'BLACK': (8, 12, 24),
    'WHITE': (245, 247, 255),
    'TRANSPARENT': (0, 0, 0, 0),

    # Neutres
    'DARK_GRAY': (36, 44, 68),
    'GRAY': (132, 144, 170),
    'LIGHT_GRAY': (200, 208, 228),

    # Nature
    'GREEN': (84, 214, 125),
    'DARK_GREEN': (52, 160, 92),
    'LIGHT_GREEN': (134, 235, 172),
    'BROWN': (139, 100, 62),
    'DARK_BROWN': (101, 67, 33),
    'LIGHT_BROWN': (180, 140, 80),

    # Actions
    'RED': (245, 98, 98),
    'DARK_RED': (215, 52, 52),
    'LIGHT_RED': (255, 140, 140),

    'BLUE': (88, 138, 255),
    'DARK_BLUE': (50, 90, 200),
    'LIGHT_BLUE': (140, 180, 255),

    'YELLOW': (255, 221, 129),
    'DARK_YELLOW': (220, 180, 60),
    'LIGHT_YELLOW': (255, 235, 170),

    'ORANGE': (255, 165, 0),
    'PURPLE': (200, 120, 255),

    # UI
    'PANEL': (16, 22, 40),
    'BUTTON_DEFAULT': (62, 88, 148),
    'BUTTON_SELECTED': (112, 165, 255),
    'BUTTON_BORDER': (189, 214, 255),
    'SHADOW': (0, 0, 0, 110),

    # Biomes
    'GRASS': (84, 214, 125),
    'WATER': (64, 164, 223),
    'SAND': (238, 214, 175),
    'STONE': (169, 169, 169),
    'DIRT': (139, 117, 78),
}

# Backward compatibility
BLACK = COLORS['BLACK']
WHITE = COLORS['WHITE']
GREEN = COLORS['GREEN']
BROWN = COLORS['BROWN']
GRAY = COLORS['GRAY']
DARK_GRAY = COLORS['DARK_GRAY']
RED = COLORS['RED']
BLUE = COLORS['BLUE']
YELLOW = COLORS['YELLOW']
ORANGE = COLORS['ORANGE']
PURPLE = COLORS['PURPLE']
