"""
Générateur de sprites pixel art pour le jeu MMO 2D
Génère tous les sprites PNG en 32x32 (tiles), 48x48 (entités), 24x24 (items)
"""

import pygame
import os
import sys

# Init Pygame sans affichage
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
screen = pygame.display.set_mode((1, 1))

# Chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TILES_DIR = os.path.join(BASE_DIR, "assets", "sprites", "tiles")
ITEMS_DIR = os.path.join(BASE_DIR, "assets", "sprites", "items")
ENTITIES_DIR = os.path.join(BASE_DIR, "assets", "sprites", "entities")

# Créer les dossiers
for d in [TILES_DIR, ITEMS_DIR, ENTITIES_DIR]:
    os.makedirs(d, exist_ok=True)


def save_sprite(surface, directory, name):
    """Sauvegarde un sprite PNG."""
    path = os.path.join(directory, f"{name}.png")
    pygame.image.save(surface, path)
    print(f"  -> {name}.png")


def pixel(surf, x, y, color):
    """Dessine un pixel."""
    if 0 <= x < surf.get_width() and 0 <= y < surf.get_height():
        surf.set_at((x, y), color)


def rect(surf, x, y, w, h, color):
    """Dessine un rectangle filled."""
    pygame.draw.rect(surf, color, (x, y, w, h))


# ============================================================
# TILES 32x32
# ============================================================

def generate_grass():
    """Herbe avec détails de herbe haute et fleurs."""
    surf = pygame.Surface((32, 32))
    # Base verte
    surf.fill((74, 190, 110))
    # Variations de couleur
    for x in range(32):
        for y in range(32):
            noise = ((x * 7 + y * 13) % 11) - 5
            base_g = 190 + noise
            pixel(surf, x, y, (74 + noise // 2, max(0, min(255, base_g)), 110 + noise // 3))
    # Herbe haute (lignes vertes plus foncées)
    import random
    rng = random.Random(42)
    for _ in range(15):
        x = rng.randint(2, 29)
        y = rng.randint(4, 28)
        h = rng.randint(3, 6)
        color = (60 + rng.randint(-10, 10), 170 + rng.randint(-10, 10), 90)
        for dy in range(h):
            pixel(surf, x, y - dy, color)
    # Petites fleurs jaunes
    for _ in range(3):
        x = rng.randint(3, 28)
        y = rng.randint(3, 28)
        pixel(surf, x, y, (255, 230, 80))
        pixel(surf, x + 1, y, (255, 240, 120))
    save_sprite(surf, TILES_DIR, "grass_1")


def generate_dirt(variant=1):
    """Terre avec cailloux."""
    surf = pygame.Surface((32, 32))
    colors = [
        (139, 117, 78),  # Brun base
        (145, 125, 85),  # Plus clair
        (130, 110, 72),  # Plus foncé
    ]
    base = colors[variant - 1]
    surf.fill(base)
    # Bruit
    for x in range(32):
        for y in range(32):
            noise = ((x * 11 + y * 7 + variant * 37) % 9) - 4
            c = tuple(max(0, min(255, v + noise)) for v in base)
            pixel(surf, x, y, c)
    # Cailloux
    import random
    rng = random.Random(variant * 100)
    for _ in range(4):
        x = rng.randint(2, 28)
        y = rng.randint(2, 28)
        gray = rng.randint(150, 180)
        pixel(surf, x, y, (gray, gray, gray))
        pixel(surf, x + 1, y, (gray - 20, gray - 20, gray - 20))
    save_sprite(surf, TILES_DIR, f"dirt_{variant}")


def generate_water(variant=1):
    """Eau avec vagues."""
    surf = pygame.Surface((32, 32))
    base_colors = [
        (40, 120, 190),
        (50, 135, 200),
        (45, 128, 195),
    ]
    base = base_colors[variant - 1]
    surf.fill(base)
    # Vagues
    for x in range(32):
        wave_y = int(8 * ((x + variant * 5) % 16) / 16)
        for dy in range(3):
            y = 10 + wave_y + dy
            if 0 <= y < 32:
                light = (base[0] + 30, base[1] + 40, min(255, base[2] + 50))
                pixel(surf, x, y, light)
    # Reflets
    import random
    rng = random.Random(variant * 50)
    for _ in range(5):
        x = rng.randint(2, 28)
        y = rng.randint(2, 28)
        pixel(surf, x, y, (100, 180, 240))
    save_sprite(surf, TILES_DIR, f"water_{variant}")


def generate_tree(variant="oak"):
    """Arbre avec tronc et feuillage."""
    surf = pygame.Surface((32, 32))
    surf.fill((0, 0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    
    if variant == "oak":
        # Tronc
        rect(surf, 13, 18, 6, 12, (101, 67, 33))
        rect(surf, 14, 19, 4, 10, (120, 80, 40))
        # Feuillage
        leaf_colors = [(45, 140, 65), (55, 160, 75), (35, 120, 55)]
        for cx, cy, r in [(16, 10, 10), (12, 12, 7), (20, 12, 7), (16, 8, 6)]:
            color = leaf_colors[(cx + cy) % 3]
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    if dx * dx + dy * dy <= r * r:
                        px, py = cx + dx, cy + dy
                        if 0 <= px < 32 and 0 <= py < 32:
                            noise = ((px * 3 + py * 7) % 5) - 2
                            c = tuple(max(0, min(255, v + noise)) for v in color)
                            pixel(surf, px, py, c)
    elif variant == "birch":
        # Tronc blanc
        rect(surf, 14, 18, 4, 12, (200, 190, 170))
        rect(surf, 15, 19, 2, 10, (220, 210, 190))
        # Taches noires sur le tronc
        pixel(surf, 15, 22, (60, 50, 40))
        pixel(surf, 16, 25, (60, 50, 40))
        # Feuillage claire
        leaf_colors = [(100, 180, 80), (110, 195, 90), (90, 170, 70)]
        for cx, cy, r in [(16, 10, 9), (12, 12, 6), (20, 12, 6), (16, 7, 5)]:
            color = leaf_colors[(cx + cy) % 3]
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    if dx * dx + dy * dy <= r * r:
                        px, py = cx + dx, cy + dy
                        if 0 <= px < 32 and 0 <= py < 32:
                            noise = ((px * 5 + py * 3) % 5) - 2
                            c = tuple(max(0, min(255, v + noise)) for v in color)
                            pixel(surf, px, py, c)
    elif variant == "pine":
        # Tronc
        rect(surf, 14, 20, 4, 10, (90, 60, 30))
        # Feuillage en triangle
        leaf_colors = [(30, 100, 50), (40, 120, 60), (25, 90, 45)]
        for row in range(15):
            width = max(1, 12 - row)
            y = 5 + row
            color = leaf_colors[row % 3]
            for dx in range(-width, width + 1):
                px = 16 + dx
                if 0 <= px < 32 and 0 <= y < 32:
                    noise = ((px * 3 + y * 7) % 5) - 2
                    c = tuple(max(0, min(255, v + noise)) for v in color)
                    pixel(surf, px, y, c)
    
    save_sprite(surf, TILES_DIR, f"tree_{variant}")


def generate_stones(variant=1):
    """Pierre avec fissures."""
    surf = pygame.Surface((32, 32))
    base = [(140, 140, 145), (150, 148, 152), (135, 135, 140)][variant - 1]
    surf.fill(base)
    # Bruit
    for x in range(32):
        for y in range(32):
            noise = ((x * 13 + y * 7 + variant * 23) % 11) - 5
            c = tuple(max(0, min(255, v + noise)) for v in base)
            pixel(surf, x, y, c)
    # Fissures
    import random
    rng = random.Random(variant * 200)
    for _ in range(3):
        x1 = rng.randint(4, 28)
        y1 = rng.randint(4, 28)
        for i in range(rng.randint(3, 8)):
            x1 += rng.choice([-1, 0, 1])
            y1 += rng.choice([-1, 0, 1])
            if 0 <= x1 < 32 and 0 <= y1 < 32:
                pixel(surf, x1, y1, (100, 100, 105))
    # Reflets
    for _ in range(3):
        x = rng.randint(2, 28)
        y = rng.randint(2, 28)
        pixel(surf, x, y, (170, 170, 175))
    save_sprite(surf, TILES_DIR, f"stones_{variant}")


def generate_ore(name, color, highlight):
    """Minerai avec éclats de couleur."""
    surf = pygame.Surface((32, 32))
    # Base roche
    surf.fill((100, 100, 105))
    for x in range(32):
        for y in range(32):
            noise = ((x * 11 + y * 7) % 9) - 4
            c = tuple(max(0, min(255, v + noise)) for v in (100, 100, 105))
            pixel(surf, x, y, c)
    # Éclats du minerai
    import random
    rng = random.Random(hash(name))
    for _ in range(8):
        x = rng.randint(4, 27)
        y = rng.randint(4, 27)
        pixel(surf, x, y, color)
        pixel(surf, x + 1, y, highlight)
        pixel(surf, x, y + 1, highlight)
    save_sprite(surf, TILES_DIR, name)


def generate_apple_tree():
    """Arbre avec pommes."""
    surf = pygame.Surface((32, 32))
    surf.fill((0, 0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    # Tronc
    rect(surf, 13, 18, 6, 12, (101, 67, 33))
    rect(surf, 14, 19, 4, 10, (120, 80, 40))
    # Feuillage verte
    for cx, cy, r in [(16, 10, 10), (12, 12, 7), (20, 12, 7)]:
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r:
                    px, py = cx + dx, cy + dy
                    if 0 <= px < 32 and 0 <= py < 32:
                        noise = ((px * 3 + py * 7) % 5) - 2
                        g = 160 + noise
                        pixel(surf, px, py, (55 + noise, max(0, min(255, g)), 75 + noise))
    # Pommes rouges
    apples = [(10, 8), (20, 9), (14, 6), (22, 11), (8, 12)]
    for ax, ay in apples:
        pixel(surf, ax, ay, (220, 40, 40))
        pixel(surf, ax + 1, ay, (240, 60, 60))
    save_sprite(surf, TILES_DIR, "apple_tree")


def generate_berry_bush():
    """Buisson avec baies."""
    surf = pygame.Surface((32, 32))
    # Buissson vert foncé
    for cx, cy, r in [(16, 18, 10), (12, 16, 7), (20, 16, 7), (16, 14, 6)]:
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r:
                    px, py = cx + dx, cy + dy
                    if 0 <= px < 32 and 0 <= py < 32:
                        noise = ((px * 5 + py * 3) % 7) - 3
                        g = 100 + noise
                        pixel(surf, px, py, (40 + noise, max(0, min(255, g)), 50 + noise))
    # Baies violettes
    berries = [(10, 15), (18, 14), (14, 18), (20, 18), (12, 12), (22, 16)]
    for bx, by in berries:
        pixel(surf, bx, by, (160, 40, 180))
        pixel(surf, bx + 1, by, (180, 60, 200))
    save_sprite(surf, TILES_DIR, "berry_bush")


def generate_foundation():
    """Planches de bois."""
    surf = pygame.Surface((32, 32))
    surf.fill((160, 130, 80))
    # Planches horizontales
    for y in range(0, 32, 8):
        pygame.draw.rect(surf, (140, 110, 65), (0, y, 32, 7))
        pygame.draw.line(surf, (120, 95, 55), (0, y), (31, y), 1)
        # Clous
        pixel(surf, 4, y + 3, (180, 180, 180))
        pixel(surf, 16, y + 3, (180, 180, 180))
        pixel(surf, 28, y + 3, (180, 180, 180))
    save_sprite(surf, TILES_DIR, "foundation")


def generate_wall():
    """Mur de pierre."""
    surf = pygame.Surface((32, 32))
    surf.fill((130, 120, 110))
    # Briques
    for row in range(4):
        y = row * 8
        offset = 8 if row % 2 else 0
        for x in range(-8, 40, 16):
            bx = x + offset
            pygame.draw.rect(surf, (120 + row * 5, 110 + row * 5, 100 + row * 5), (bx, y, 14, 7))
            pygame.draw.rect(surf, (100, 95, 85), (bx, y, 14, 7), 1)
    save_sprite(surf, TILES_DIR, "wall")


# ============================================================
# ENTITIES 48x48
# ============================================================

def generate_player():
    """Joueur pixel art face."""
    surf = pygame.Surface((48, 48), pygame.SRCALPHA)
    # Tête
    rect(surf, 18, 6, 12, 12, (220, 180, 140))  # Peau
    rect(surf, 19, 7, 10, 10, (230, 190, 150))
    # Yeux
    pixel(surf, 21, 10, (40, 40, 60))
    pixel(surf, 26, 10, (40, 40, 60))
    pixel(surf, 21, 11, (255, 255, 255))
    pixel(surf, 26, 11, (255, 255, 255))
    # Bouche
    pixel(surf, 23, 14, (180, 100, 80))
    pixel(surf, 24, 14, (180, 100, 80))
    # Cheveux
    rect(surf, 17, 4, 14, 4, (80, 50, 30))
    rect(surf, 17, 5, 3, 6, (80, 50, 30))
    rect(surf, 28, 5, 3, 6, (80, 50, 30))
    # Corps (tunique bleue)
    rect(surf, 16, 18, 16, 14, (50, 80, 160))
    rect(surf, 17, 19, 14, 12, (60, 95, 180))
    # Ceinture
    rect(surf, 16, 30, 16, 3, (120, 80, 40))
    pixel(surf, 24, 30, (200, 180, 60))  # Boucle
    # Bras
    rect(surf, 10, 19, 6, 12, (50, 80, 160))
    rect(surf, 32, 19, 6, 12, (50, 80, 160))
    # Mains
    rect(surf, 11, 30, 4, 4, (220, 180, 140))
    rect(surf, 33, 30, 4, 4, (220, 180, 140))
    # Jambes
    rect(surf, 17, 33, 6, 10, (40, 50, 100))
    rect(surf, 25, 33, 6, 10, (40, 50, 100))
    # Bottes
    rect(surf, 16, 42, 8, 5, (80, 50, 30))
    rect(surf, 24, 42, 8, 5, (80, 50, 30))
    save_sprite(surf, ENTITIES_DIR, "player")


def generate_player_walk(frame):
    """Joueur en mouvement."""
    surf = pygame.Surface((48, 48), pygame.SRCALPHA)
    # Même base que player mais avec jambes décalées
    rect(surf, 18, 6, 12, 12, (220, 180, 140))
    rect(surf, 19, 7, 10, 10, (230, 190, 150))
    pixel(surf, 21, 10, (40, 40, 60))
    pixel(surf, 26, 10, (40, 40, 60))
    pixel(surf, 21, 11, (255, 255, 255))
    pixel(surf, 26, 11, (255, 255, 255))
    pixel(surf, 23, 14, (180, 100, 80))
    pixel(surf, 24, 14, (180, 100, 80))
    rect(surf, 17, 4, 14, 4, (80, 50, 30))
    rect(surf, 17, 5, 3, 6, (80, 50, 30))
    rect(surf, 28, 5, 3, 6, (80, 50, 30))
    rect(surf, 16, 18, 16, 14, (50, 80, 160))
    rect(surf, 17, 19, 14, 12, (60, 95, 180))
    rect(surf, 16, 30, 16, 3, (120, 80, 40))
    pixel(surf, 24, 30, (200, 180, 60))
    # Bras balancés
    if frame == 1:
        rect(surf, 8, 20, 6, 10, (50, 80, 160))
        rect(surf, 34, 18, 6, 10, (50, 80, 160))
    else:
        rect(surf, 10, 18, 6, 10, (50, 80, 160))
        rect(surf, 32, 20, 6, 10, (50, 80, 160))
    rect(surf, 11, 30, 4, 4, (220, 180, 140))
    rect(surf, 33, 30, 4, 4, (220, 180, 140))
    # Jambes décalées
    if frame == 1:
        rect(surf, 15, 33, 6, 10, (40, 50, 100))
        rect(surf, 27, 33, 6, 10, (40, 50, 100))
        rect(surf, 14, 42, 8, 5, (80, 50, 30))
        rect(surf, 26, 42, 8, 5, (80, 50, 30))
    else:
        rect(surf, 19, 33, 6, 10, (40, 50, 100))
        rect(surf, 23, 33, 6, 10, (40, 50, 100))
        rect(surf, 18, 42, 8, 5, (80, 50, 30))
        rect(surf, 22, 42, 8, 5, (80, 50, 30))
    save_sprite(surf, ENTITIES_DIR, f"player_walk{frame}")


def generate_enemy():
    """Ennemi (squelette/gobelin)."""
    surf = pygame.Surface((48, 48), pygame.SRCALPHA)
    # Tête verte (gobelin)
    rect(surf, 17, 4, 14, 14, (80, 140, 60))
    rect(surf, 18, 5, 12, 12, (90, 160, 70))
    # Yeux rouges
    pixel(surf, 20, 9, (220, 40, 40))
    pixel(surf, 26, 9, (220, 40, 40))
    pixel(surf, 20, 10, (255, 80, 80))
    pixel(surf, 26, 10, (255, 80, 80))
    # Cornes
    rect(surf, 16, 2, 3, 4, (100, 80, 50))
    rect(surf, 29, 2, 3, 4, (100, 80, 50))
    # Bouche
    pixel(surf, 22, 13, (60, 100, 40))
    pixel(surf, 23, 13, (60, 100, 40))
    pixel(surf, 24, 13, (60, 100, 40))
    # Dents
    pixel(surf, 22, 14, (220, 220, 200))
    pixel(surf, 24, 14, (220, 220, 200))
    # Corps
    rect(surf, 15, 18, 18, 16, (60, 100, 50))
    rect(surf, 16, 19, 16, 14, (70, 120, 60))
    # Ceinture
    rect(surf, 15, 32, 18, 3, (100, 70, 40))
    # Bras
    rect(surf, 9, 19, 6, 12, (60, 100, 50))
    rect(surf, 33, 19, 6, 12, (60, 100, 50))
    # Mains (griffes)
    rect(surf, 8, 30, 5, 5, (80, 140, 60))
    rect(surf, 35, 30, 5, 5, (80, 140, 60))
    pixel(surf, 8, 30, (200, 200, 180))
    pixel(surf, 10, 30, (200, 200, 180))
    pixel(surf, 35, 30, (200, 200, 180))
    pixel(surf, 37, 30, (200, 200, 180))
    # Jambes
    rect(surf, 17, 35, 6, 8, (50, 85, 40))
    rect(surf, 25, 35, 6, 8, (50, 85, 40))
    # Pieds
    rect(surf, 16, 42, 8, 5, (70, 50, 30))
    rect(surf, 24, 42, 8, 5, (70, 50, 30))
    save_sprite(surf, ENTITIES_DIR, "enemy")


def generate_enemy_move():
    """Ennemi en mouvement."""
    surf = pygame.Surface((48, 48), pygame.SRCALPHA)
    # Même base que enemy mais avec animation
    rect(surf, 17, 4, 14, 14, (80, 140, 60))
    rect(surf, 18, 5, 12, 12, (90, 160, 70))
    pixel(surf, 20, 9, (220, 40, 40))
    pixel(surf, 26, 9, (220, 40, 40))
    pixel(surf, 20, 10, (255, 80, 80))
    pixel(surf, 26, 10, (255, 80, 80))
    rect(surf, 16, 2, 3, 4, (100, 80, 50))
    rect(surf, 29, 2, 3, 4, (100, 80, 50))
    pixel(surf, 22, 13, (60, 100, 40))
    pixel(surf, 23, 13, (60, 100, 40))
    pixel(surf, 24, 13, (60, 100, 40))
    pixel(surf, 22, 14, (220, 220, 200))
    pixel(surf, 24, 14, (220, 220, 200))
    rect(surf, 15, 18, 18, 16, (60, 100, 50))
    rect(surf, 16, 19, 16, 14, (70, 120, 60))
    rect(surf, 15, 32, 18, 3, (100, 70, 40))
    # Bras décalés
    rect(surf, 7, 20, 6, 10, (60, 100, 50))
    rect(surf, 35, 18, 6, 10, (60, 100, 50))
    rect(surf, 6, 30, 5, 5, (80, 140, 60))
    rect(surf, 37, 28, 5, 5, (80, 140, 60))
    # Jambes décalées
    rect(surf, 15, 35, 6, 8, (50, 85, 40))
    rect(surf, 27, 35, 6, 8, (50, 85, 40))
    rect(surf, 14, 42, 8, 5, (70, 50, 30))
    rect(surf, 26, 42, 8, 5, (70, 50, 30))
    save_sprite(surf, ENTITIES_DIR, "enemy_move1")


def generate_tombstone():
    """Tombe."""
    surf = pygame.Surface((32, 32))
    surf.fill((0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    # Base
    pygame.draw.ellipse(surf, (50, 45, 40), (6, 22, 20, 8))
    # Pierre
    pygame.draw.rect(surf, (110, 105, 95), (10, 6, 12, 18), border_radius=3)
    pygame.draw.rect(surf, (90, 85, 75), (10, 6, 12, 18), 1, border_radius=3)
    # Croix
    pygame.draw.line(surf, (180, 175, 165), (16, 9), (16, 19), 2)
    pygame.draw.line(surf, (180, 175, 165), (12, 13), (20, 13), 2)
    # Texte RIP
    small = pygame.font.Font(None, 10)
    rip = small.render("RIP", True, (160, 155, 145))
    surf.blit(rip, (12, 20))
    save_sprite(surf, ENTITIES_DIR, "tombstone")


def generate_death_marker():
    """Marqueur de mort au sol."""
    surf = pygame.Surface((32, 32))
    surf.fill((0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    # Croix au sol
    pygame.draw.rect(surf, (180, 160, 80), (12, 8, 8, 16))
    pygame.draw.rect(surf, (180, 160, 80), (8, 12, 16, 8))
    # Lueur
    for r in range(14, 0, -1):
        alpha = max(0, 80 - r * 5)
        glow = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 200, 80, alpha), (r, r), r)
        surf.blit(glow, (16 - r, 16 - r))
    save_sprite(surf, ENTITIES_DIR, "death_marker")


# ============================================================
# ITEMS 24x24
# ============================================================

def generate_item_wood():
    surf = pygame.Surface((24, 24))
    surf.fill((0, 0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    # Bûche
    rect(surf, 4, 8, 16, 8, (120, 80, 40))
    rect(surf, 5, 9, 14, 6, (140, 95, 50))
    # Anneaux
    pixel(surf, 4, 11, (100, 65, 30))
    pixel(surf, 19, 11, (100, 65, 30))
    # Écorce
    for x in range(5, 19, 3):
        pixel(surf, x, 8, (100, 65, 30))
    save_sprite(surf, ITEMS_DIR, "wood")


def generate_item_stone():
    surf = pygame.Surface((24, 24))
    surf.fill((0, 0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    # Pierre
    points = [(8, 6), (16, 5), (20, 10), (18, 18), (10, 19), (4, 14)]
    pygame.draw.polygon(surf, (160, 160, 165), points)
    lighter = [(9, 7), (15, 6), (18, 10), (16, 17), (11, 18), (5, 13)]
    pygame.draw.polygon(surf, (180, 180, 185), lighter)
    # Reflet
    pixel(surf, 10, 8, (200, 200, 205))
    pixel(surf, 11, 8, (200, 200, 205))
    save_sprite(surf, ITEMS_DIR, "stone")


def generate_item_ore(name, base_color, highlight_color):
    surf = pygame.Surface((24, 24))
    surf.fill((0, 0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    # Base roche
    points = [(7, 7), (17, 5), (21, 11), (18, 19), (9, 20), (3, 14)]
    pygame.draw.polygon(surf, (120, 120, 125), points)
    # Éclats
    pixel(surf, 10, 9, base_color)
    pixel(surf, 11, 10, highlight_color)
    pixel(surf, 14, 8, base_color)
    pixel(surf, 15, 9, highlight_color)
    pixel(surf, 12, 14, base_color)
    pixel(surf, 13, 15, highlight_color)
    pixel(surf, 16, 13, base_color)
    save_sprite(surf, ITEMS_DIR, name)


def generate_item_sword(name, blade_color, handle_color):
    surf = pygame.Surface((24, 24))
    surf.fill((0, 0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    # Lame
    for i in range(14):
        x = 4 + i
        y = 3 + i // 2
        width = max(1, 3 - i // 5)
        rect(surf, x, y, width, 2, blade_color)
    # Pointe
    pixel(surf, 17, 10, blade_color)
    pixel(surf, 18, 11, blade_color)
    # Manche
    rect(surf, 2, 16, 4, 2, handle_color)
    rect(surf, 1, 18, 6, 2, (100, 70, 40))
    # Guard
    rect(surf, 3, 15, 3, 1, (200, 180, 60))
    save_sprite(surf, ITEMS_DIR, name)


def generate_item_pickaxe(name, head_color, handle_color):
    surf = pygame.Surface((24, 24))
    surf.fill((0, 0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    # Manche
    for i in range(12):
        x = 4 + i
        y = 14 - i
        rect(surf, x, y, 2, 2, handle_color)
    # Tête
    rect(surf, 2, 4, 10, 3, head_color)
    rect(surf, 1, 5, 12, 2, head_color)
    pixel(surf, 12, 5, head_color)
    pixel(surf, 13, 6, head_color)
    # Reflet
    pixel(surf, 4, 5, (min(255, head_color[0] + 40), min(255, head_color[1] + 40), min(255, head_color[2] + 40)))
    save_sprite(surf, ITEMS_DIR, name)


def generate_item_armor(name, color, highlight):
    surf = pygame.Surface((24, 24))
    surf.fill((0, 0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    # Armure (plastron)
    rect(surf, 6, 4, 12, 16, color)
    rect(surf, 7, 5, 10, 14, highlight)
    # Épaules
    rect(surf, 3, 5, 4, 5, color)
    rect(surf, 17, 5, 4, 5, color)
    # Ceinture
    rect(surf, 6, 17, 12, 2, (120, 80, 40))
    pixel(surf, 12, 17, (200, 180, 60))
    save_sprite(surf, ITEMS_DIR, name)


def generate_item_food(name, color, highlight):
    surf = pygame.Surface((24, 24))
    surf.fill((0, 0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    if name == "apple":
        # Pomme ronde
        for cx, cy, r in [(12, 12, 7)]:
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    if dx * dx + dy * dy <= r * r:
                        px, py = cx + dx, cy + dy
                        if 0 <= px < 24 and 0 <= py < 24:
                            noise = ((px * 3 + py * 7) % 5) - 2
                            c = tuple(max(0, min(255, v + noise)) for v in color)
                            pixel(surf, px, py, c)
        # Tige
        pixel(surf, 12, 4, (80, 50, 30))
        pixel(surf, 12, 3, (80, 50, 30))
        # Feuille
        pixel(surf, 13, 3, (60, 140, 50))
        pixel(surf, 14, 2, (70, 160, 60))
        # Reflet
        pixel(surf, 9, 9, highlight)
        pixel(surf, 10, 9, highlight)
    elif name == "berry":
        # Baie
        for cx, cy, r in [(12, 13, 5)]:
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    if dx * dx + dy * dy <= r * r:
                        px, py = cx + dx, cy + dy
                        if 0 <= px < 24 and 0 <= py < 24:
                            noise = ((px * 5 + py * 3) % 5) - 2
                            c = tuple(max(0, min(255, v + noise)) for v in color)
                            pixel(surf, px, py, c)
        pixel(surf, 12, 7, highlight)
        pixel(surf, 11, 8, highlight)
    elif name == "bread":
        # Pain
        rect(surf, 4, 10, 16, 8, (200, 170, 100))
        rect(surf, 5, 11, 14, 6, (220, 190, 120))
        # Croûte
        rect(surf, 4, 10, 16, 2, (180, 140, 70))
        # Reflets
        pixel(surf, 8, 12, highlight)
        pixel(surf, 14, 13, highlight)
    elif name == "meat":
        # Viande
        rect(surf, 5, 8, 14, 10, (180, 60, 50))
        rect(surf, 6, 9, 12, 8, (200, 80, 60))
        # Os
        rect(surf, 16, 10, 4, 3, (220, 210, 190))
        pixel(surf, 20, 11, (220, 210, 190))
        pixel(surf, 16, 13, (220, 210, 190))
        # Reflet
        pixel(surf, 8, 10, highlight)
    save_sprite(surf, ITEMS_DIR, name)


def generate_item_ingot(name, color, highlight):
    surf = pygame.Surface((24, 24))
    surf.fill((0, 0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    # Lingot
    rect(surf, 4, 8, 16, 8, color)
    rect(surf, 5, 9, 14, 6, highlight)
    # Reflet
    pixel(surf, 7, 10, (min(255, highlight[0] + 30), min(255, highlight[1] + 30), min(255, highlight[2] + 30)))
    pixel(surf, 8, 10, (min(255, highlight[0] + 30), min(255, highlight[1] + 30), min(255, highlight[2] + 30)))
    # Ombre
    rect(surf, 4, 15, 16, 1, (max(0, color[0] - 30), max(0, color[1] - 30), max(0, color[2] - 30)))
    save_sprite(surf, ITEMS_DIR, name)


def generate_item_diamond():
    surf = pygame.Surface((24, 24))
    surf.fill((0, 0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    # Diamant (forme losange)
    points = [(12, 3), (20, 10), (12, 20), (4, 10)]
    pygame.draw.polygon(surf, (100, 200, 240), points)
    lighter = [(12, 5), (18, 10), (12, 18), (6, 10)]
    pygame.draw.polygon(surf, (140, 220, 255), lighter)
    # Reflets
    pixel(surf, 10, 8, (200, 240, 255))
    pixel(surf, 11, 7, (200, 240, 255))
    pixel(surf, 8, 10, (200, 240, 255))
    save_sprite(surf, ITEMS_DIR, "diamond")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=== Génération des sprites pixel art ===\n")
    
    print("--- TILES ---")
    generate_grass()
    for v in range(1, 4):
        generate_dirt(v)
    for v in range(1, 4):
        generate_water(v)
    generate_tree("oak")
    generate_tree("birch")
    generate_tree("pine")
    for v in range(1, 4):
        generate_stones(v)
    generate_ore("iron_ore", (160, 110, 95), (200, 150, 130))
    generate_ore("gold_ore", (220, 185, 60), (255, 220, 100))
    generate_ore("diamond_ore", (100, 200, 240), (150, 230, 255))
    generate_ore("coal_ore", (40, 40, 45), (70, 70, 75))
    generate_apple_tree()
    generate_berry_bush()
    generate_foundation()
    generate_wall()
    
    print("\n--- ENTITIES ---")
    generate_player()
    generate_player_walk(1)
    generate_player_walk(2)
    generate_enemy()
    generate_enemy_move()
    generate_tombstone()
    generate_death_marker()
    
    print("\n--- ITEMS ---")
    generate_item_wood()
    generate_item_stone()
    generate_item_ore("iron_ore", (160, 110, 95), (200, 150, 130))
    generate_item_ore("gold_ore", (220, 185, 60), (255, 220, 100))
    generate_item_ore("coal_ore", (40, 40, 45), (70, 70, 75))
    generate_item_sword("wooden_sword", (160, 120, 60), (100, 70, 40))
    generate_item_sword("iron_sword", (180, 180, 190), (100, 70, 40))
    generate_item_sword("gold_sword", (220, 190, 60), (100, 70, 40))
    generate_item_sword("diamond_sword", (100, 200, 240), (100, 70, 40))
    generate_item_pickaxe("wooden_pickaxe", (160, 120, 60), (100, 70, 40))
    generate_item_armor("leather_armor", (140, 100, 50), (170, 130, 70))
    generate_item_armor("iron_armor", (160, 160, 170), (190, 190, 200))
    generate_item_food("apple", (200, 40, 40), (240, 80, 80))
    generate_item_food("berry", (140, 30, 160), (180, 60, 200))
    generate_item_food("bread", (200, 170, 100), (240, 210, 140))
    generate_item_food("meat", (180, 60, 50), (220, 100, 80))
    generate_item_ingot("iron_ingot", (160, 160, 170), (190, 190, 200))
    generate_item_ingot("gold_ingot", (220, 190, 60), (255, 220, 100))
    generate_item_diamond()
    
    print(f"\n=== Terminé ! Tous les sprites ont été générés dans assets/sprites/ ===")
