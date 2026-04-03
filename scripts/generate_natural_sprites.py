#!/usr/bin/env python3
"""
Générateur de sprites naturels pour un monde type Stardew Valley/Pokémon
"""

import pygame
import os
import random
from PIL import Image, ImageDraw, ImageFilter

def create_natural_grass_variants():
    """Crée plusieurs variantes d'herbe naturelle"""
    sprites = {}
    
    # Couleurs d'herbe variées
    grass_colors = [
        (34, 139, 34),   # Vert forêt
        (50, 150, 50),   # Vert prairie
        (40, 180, 40),   # Vert clair
        (60, 130, 60),   # Vert sombre
    ]
    
    for i, base_color in enumerate(grass_colors):
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Base d'herbe
        draw.rectangle([0, 0, 32, 32], fill=base_color + (255,))
        
        # Ajouter des brins d'herbe
        for _ in range(15):
            x = random.randint(2, 30)
            y = random.randint(2, 30)
            # Couleur légèrement différente
            r, g, b = base_color
            grass_color = (
                min(255, r + random.randint(-20, 20)),
                min(255, g + random.randint(-20, 20)),
                min(255, b + random.randint(-10, 10))
            )
            draw.ellipse([x-1, y-1, x+1, y+1], fill=grass_color + (255,))
        
        # Effet de texture
        img = img.filter(ImageFilter.GaussianBlur(0.5))
        
        sprites[f'grass_{i+1}'] = img
    
    return sprites

def create_natural_dirt_paths():
    """Crée des chemins de terre naturels"""
    sprites = {}
    
    # Couleurs de terre
    dirt_colors = [
        (139, 117, 78),  # Terre brune
        (160, 130, 90),  # Terre claire
        (120, 100, 70),  # Terre sombre
    ]
    
    for i, base_color in enumerate(dirt_colors):
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Base de terre
        draw.rectangle([0, 0, 32, 32], fill=base_color + (255,))
        
        # Ajouter des cailloux et texture
        for _ in range(8):
            x = random.randint(2, 30)
            y = random.randint(2, 30)
            size = random.randint(1, 3)
            # Couleur de caillou
            r, g, b = base_color
            stone_color = (
                min(255, r + random.randint(10, 40)),
                min(255, g + random.randint(10, 40)),
                min(255, b + random.randint(10, 40))
            )
            draw.ellipse([x-size, y-size, x+size, y+size], fill=stone_color + (255,))
        
        sprites[f'dirt_{i+1}'] = img
    
    return sprites

def create_natural_water():
    """Crée des tiles d'eau animées"""
    sprites = {}
    
    # Couleurs d'eau
    water_colors = [
        (64, 164, 223),   # Bleu eau
        (72, 172, 231),   # Bleu clair
        (56, 156, 215),   # Bleu foncé
    ]
    
    for i, base_color in enumerate(water_colors):
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Base d'eau
        draw.rectangle([0, 0, 32, 32], fill=base_color + (255,))
        
        # Ajouter des reflets
        for _ in range(5):
            x = random.randint(4, 28)
            y = random.randint(4, 28)
            w = random.randint(3, 8)
            h = random.randint(1, 3)
            # Couleur de reflet
            r, g, b = base_color
            reflect_color = (
                min(255, r + 30),
                min(255, g + 30),
                min(255, b + 30)
            )
            draw.ellipse([x-w//2, y-h//2, x+w//2, y+h//2], fill=reflect_color + (180,))
        
        sprites[f'water_{i+1}'] = img
    
    return sprites

def create_natural_trees():
    """Crée des arbres plus naturels"""
    sprites = {}
    
    # Différents types d'arbres
    tree_types = [
        {'trunk': (101, 67, 33), 'leaves': (34, 139, 34), 'name': 'oak'},
        {'trunk': (120, 80, 40), 'leaves': (50, 150, 50), 'name': 'birch'},
        {'trunk': (80, 50, 25), 'leaves': (20, 100, 20), 'name': 'pine'},
    ]
    
    for tree_type in tree_types:
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        trunk_color = tree_type['trunk']
        leaves_color = tree_type['leaves']
        
        # Dessiner le tronc
        draw.rectangle([13, 20, 19, 32], fill=trunk_color + (255,))
        
        # Dessiner les feuilles (plusieurs cercles)
        for offset in [(-3, -8), (3, -8), (0, -12), (-2, -5), (2, -5)]:
            x, y = 16 + offset[0], 20 + offset[1]
            size = random.randint(4, 7)
            # Variation de couleur des feuilles
            r, g, b = leaves_color
            leaf_color = (
                max(0, r + random.randint(-15, 15)),
                max(0, g + random.randint(-15, 15)),
                max(0, b + random.randint(-10, 10))
            )
            draw.ellipse([x-size, y-size, x+size, y+size], fill=leaf_color + (255,))
        
        sprites[f'tree_{tree_type["name"]}'] = img
    
    return sprites

def create_natural_stones():
    """Crée des rochers naturels"""
    sprites = {}
    
    stone_colors = [
        (128, 128, 128),  # Gris
        (100, 100, 100),  # Gris foncé
        (150, 150, 150),  # Gris clair
    ]
    
    for i, base_color in enumerate(stone_colors):
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Dessiner plusieurs rochers de tailles différentes
        rocks = [
            {'pos': (8, 12), 'size': 6},
            {'pos': (20, 8), 'size': 4},
            {'pos': (16, 20), 'size': 5},
            {'pos': (24, 18), 'size': 3},
        ]
        
        for rock in rocks:
            x, y = rock['pos']
            size = rock['size']
            # Variation de couleur
            r, g, b = base_color
            rock_color = (
                r + random.randint(-20, 20),
                g + random.randint(-20, 20),
                b + random.randint(-20, 20)
            )
            draw.ellipse([x-size, y-size, x+size, y+size], fill=rock_color + (255,))
        
        sprites[f'stones_{i+1}'] = img
    
    return sprites

def save_sprites_to_pygame(sprites, output_dir):
    """Sauvegarde les sprites au format pygame"""
    os.makedirs(output_dir, exist_ok=True)
    
    for name, pil_image in sprites.items():
        # Convertir PIL vers pygame
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        
        pygame_image = pygame.image.fromstring(data, size, mode)
        
        # Sauvegarder
        filepath = os.path.join(output_dir, f"{name}.png")
        pygame.image.save(pygame_image, filepath)
        print(f"✅ Sprite sauvegardé: {filepath}")

def main():
    """Génère tous les sprites naturels"""
    pygame.init()
    
    print("🎨 Génération des sprites naturels...")
    
    # Créer les répertoires
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites")
    
    # Générer tous les types de sprites
    all_sprites = {}
    
    print("Génération de l'herbe naturelle...")
    all_sprites.update(create_natural_grass_variants())
    
    print("Génération des chemins de terre...")
    all_sprites.update(create_natural_dirt_paths())
    
    print("Génération de l'eau...")
    all_sprites.update(create_natural_water())
    
    print("Génération des arbres naturels...")
    all_sprites.update(create_natural_trees())
    
    print("Génération des rochers naturels...")
    all_sprites.update(create_natural_stones())
    
    # Sauvegarder dans le dossier tiles
    tiles_dir = os.path.join(base_dir, "tiles")
    save_sprites_to_pygame(all_sprites, tiles_dir)
    
    print(f"🎉 {len(all_sprites)} sprites naturels générés avec succès!")
    print(f"📁 Sauvegardés dans: {tiles_dir}")

if __name__ == "__main__":
    main()
