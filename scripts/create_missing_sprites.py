#!/usr/bin/env python3
"""
Créer les sprites manquants pour le jeu (arbres fruitiers, minerais, etc.)
"""

import pygame
import os
from PIL import Image, ImageDraw
import random

def create_apple_tree():
    """Crée un sprite d'arbre à pommes"""
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Tronc
    draw.rectangle([13, 20, 19, 32], fill=(101, 67, 33, 255))
    
    # Feuillage vert
    for offset in [(-3, -8), (3, -8), (0, -12), (-2, -5), (2, -5)]:
        x, y = 16 + offset[0], 20 + offset[1]
        size = random.randint(4, 7)
        draw.ellipse([x-size, y-size, x+size, y+size], fill=(34, 139, 34, 255))
    
    # Pommes rouges
    for _ in range(3):
        x = random.randint(10, 22)
        y = random.randint(8, 18)
        draw.ellipse([x-2, y-2, x+2, y+2], fill=(255, 0, 0, 255))
    
    return img

def create_berry_bush():
    """Crée un sprite de buisson de baies"""
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Base du buisson
    draw.ellipse([8, 16, 24, 30], fill=(50, 120, 50, 255))
    draw.ellipse([6, 12, 26, 28], fill=(34, 139, 34, 255))
    
    # Baies violettes
    for _ in range(8):
        x = random.randint(10, 22)
        y = random.randint(14, 26)
        draw.ellipse([x-1, y-1, x+1, y+1], fill=(128, 0, 128, 255))
    
    return img

def create_ore_sprites():
    """Crée les sprites de minerais"""
    sprites = {}
    
    # Couleurs des minerais
    ore_colors = {
        'iron_ore': (139, 69, 19),
        'gold_ore': (255, 215, 0),
        'diamond_ore': (185, 242, 255),
        'coal_ore': (64, 64, 64),
    }
    
    for ore_name, color in ore_colors.items():
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Base rocheuse
        draw.rectangle([0, 0, 32, 32], fill=(128, 128, 128, 255))
        
        # Veines de minerai
        for _ in range(6):
            x = random.randint(2, 30)
            y = random.randint(2, 30)
            size = random.randint(2, 4)
            draw.ellipse([x-size, y-size, x+size, y+size], fill=color + (255,))
        
        # Texture rocheuse
        for _ in range(20):
            x = random.randint(1, 31)
            y = random.randint(1, 31)
            r, g, b = 128, 128, 128
            rock_color = (
                r + random.randint(-30, 30),
                g + random.randint(-30, 30),
                b + random.randint(-30, 30)
            )
            draw.rectangle([x, y, x+1, y+1], fill=rock_color + (255,))
        
        sprites[ore_name] = img
    
    return sprites

def create_building_sprites():
    """Crée les sprites de construction"""
    sprites = {}
    
    # Fondation
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 32, 32], fill=(160, 160, 160, 255))
    # Lignes de mortier
    draw.line([0, 16, 32, 16], fill=(140, 140, 140, 255), width=2)
    draw.line([16, 0, 16, 32], fill=(140, 140, 140, 255), width=2)
    sprites['foundation'] = img
    
    # Mur
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 32, 32], fill=(139, 69, 19, 255))
    # Planches verticales
    for x in range(0, 32, 8):
        draw.line([x, 0, x, 32], fill=(120, 60, 15, 255), width=1)
    sprites['wall'] = img
    
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
    """Génère tous les sprites manquants"""
    pygame.init()
    
    print("🎨 Génération des sprites manquants...")
    
    # Créer les répertoires
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites")
    tiles_dir = os.path.join(base_dir, "tiles")
    
    # Générer tous les sprites manquants
    all_sprites = {}
    
    print("Génération de l'arbre à pommes...")
    all_sprites['apple_tree'] = create_apple_tree()
    
    print("Génération du buisson de baies...")
    all_sprites['berry_bush'] = create_berry_bush()
    
    print("Génération des minerais...")
    all_sprites.update(create_ore_sprites())
    
    print("Génération des éléments de construction...")
    all_sprites.update(create_building_sprites())
    
    # Sauvegarder
    save_sprites_to_pygame(all_sprites, tiles_dir)
    
    print(f"🎉 {len(all_sprites)} sprites manquants générés avec succès!")
    print(f"📁 Sauvegardés dans: {tiles_dir}")

if __name__ == "__main__":
    main()
