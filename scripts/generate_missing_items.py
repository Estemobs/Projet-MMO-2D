#!/usr/bin/env python3
"""
Générateur de sprites d'items supplémentaires pour l'inventaire
"""

import pygame
import os
from PIL import Image, ImageDraw

def create_missing_items():
    """Crée les sprites d'items manquants"""
    items = {}
    
    # === LINGOTS ET MÉTAUX ===
    
    # Lingot de fer
    iron_ingot = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(iron_ingot)
    
    # Forme de lingot
    draw.rectangle([8, 12, 24, 20], fill=(139, 139, 139))
    draw.rectangle([10, 14, 22, 18], fill=(169, 169, 169))
    
    # Reflets métalliques
    draw.rectangle([11, 15, 13, 17], fill=(200, 200, 200))
    draw.rectangle([19, 15, 21, 17], fill=(200, 200, 200))
    
    items['iron_ingot'] = iron_ingot
    
    # Lingot d'or
    gold_ingot = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gold_ingot)
    
    draw.rectangle([8, 12, 24, 20], fill=(255, 215, 0))
    draw.rectangle([10, 14, 22, 18], fill=(255, 255, 0))
    
    # Brillance dorée
    draw.rectangle([11, 15, 13, 17], fill=(255, 255, 255))
    draw.rectangle([19, 15, 21, 17], fill=(255, 255, 255))
    
    items['gold_ingot'] = gold_ingot
    
    # Diamant
    diamond = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(diamond)
    
    # Forme de diamant
    points = [(16, 8), (12, 16), (16, 24), (20, 16)]
    draw.polygon(points, fill=(185, 242, 255))
    
    # Facettes
    draw.polygon([(16, 8), (14, 12), (16, 16), (18, 12)], fill=(220, 250, 255))
    draw.polygon([(16, 16), (12, 16), (14, 20), (16, 24)], fill=(150, 220, 240))
    
    # Brillance
    draw.polygon([(15, 10), (17, 10), (16, 14)], fill=(255, 255, 255))
    
    items['diamond'] = diamond
    
    # === NOURRITURE ===
    
    # Pain
    bread = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bread)
    
    # Pain ovale
    draw.ellipse([6, 14, 26, 22], fill=(210, 180, 140))
    draw.ellipse([8, 15, 24, 21], fill=(245, 222, 179))
    
    # Texture du pain
    for i in range(3):
        x = 10 + i * 4
        draw.ellipse([x, 16, x+2, 18], fill=(200, 170, 130))
    
    items['bread'] = bread
    
    # === ARMES ===
    
    # Épée en bois
    wooden_sword = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(wooden_sword)
    
    # Lame en bois
    draw.rectangle([14, 4, 18, 24], fill=(139, 69, 19))
    draw.rectangle([15, 5, 17, 23], fill=(160, 82, 45))
    
    # Garde
    draw.rectangle([12, 20, 20, 22], fill=(101, 67, 33))
    
    # Poignée
    draw.rectangle([14, 22, 18, 28], fill=(139, 69, 19))
    
    # Pommeau
    draw.ellipse([13, 26, 19, 30], fill=(101, 67, 33))
    
    items['wooden_sword'] = wooden_sword
    
    # Épée en fer
    iron_sword = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(iron_sword)
    
    # Lame en fer
    draw.rectangle([14, 4, 18, 24], fill=(169, 169, 169))
    draw.rectangle([15, 5, 17, 23], fill=(200, 200, 200))
    
    # Reflet sur la lame
    draw.rectangle([15, 6, 16, 22], fill=(220, 220, 220))
    
    # Garde
    draw.rectangle([12, 20, 20, 22], fill=(139, 139, 139))
    
    # Poignée en cuir
    draw.rectangle([14, 22, 18, 28], fill=(139, 69, 19))
    
    # Pommeau en métal
    draw.ellipse([13, 26, 19, 30], fill=(169, 169, 169))
    
    items['iron_sword'] = iron_sword
    
    # === OUTILS ===
    
    # Pioche en bois
    wooden_pickaxe = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(wooden_pickaxe)
    
    # Manche
    draw.rectangle([14, 8, 18, 28], fill=(139, 69, 19))
    draw.rectangle([15, 9, 17, 27], fill=(160, 82, 45))
    
    # Tête de pioche
    draw.rectangle([8, 6, 24, 12], fill=(101, 67, 33))
    draw.rectangle([9, 7, 23, 11], fill=(139, 69, 19))
    
    # Pointes
    draw.polygon([(8, 9), (4, 9), (6, 7), (6, 11)], fill=(101, 67, 33))
    draw.polygon([(24, 9), (28, 9), (26, 7), (26, 11)], fill=(101, 67, 33))
    
    items['wooden_pickaxe'] = wooden_pickaxe
    
    # === ARMURES ===
    
    # Armure en cuir
    leather_armor = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(leather_armor)
    
    # Torse
    draw.ellipse([10, 8, 22, 24], fill=(139, 69, 19))
    draw.ellipse([12, 10, 20, 22], fill=(160, 82, 45))
    
    # Sangles
    draw.rectangle([15, 12, 17, 20], fill=(101, 67, 33))
    draw.rectangle([11, 14, 21, 16], fill=(101, 67, 33))
    
    # Boucles
    draw.ellipse([14, 13, 18, 17], fill=(139, 139, 139))
    
    items['leather_armor'] = leather_armor
    
    # Armure en fer
    iron_armor = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(iron_armor)
    
    # Plastron
    draw.ellipse([10, 8, 22, 24], fill=(139, 139, 139))
    draw.ellipse([12, 10, 20, 22], fill=(169, 169, 169))
    
    # Reflets métalliques
    draw.ellipse([13, 11, 19, 17], fill=(200, 200, 200))
    
    # Rivets
    positions = [(12, 10), (20, 10), (12, 22), (20, 22)]
    for x, y in positions:
        draw.ellipse([x-1, y-1, x+1, y+1], fill=(120, 120, 120))
    
    items['iron_armor'] = iron_armor
    
    return items

def create_mineral_ores():
    """Crée les minerais manquants avec de beaux sprites"""
    ores = {}
    
    # Minerai de diamant
    diamond_ore = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(diamond_ore)
    
    # Roche de base
    draw.ellipse([6, 8, 26, 26], fill=(64, 64, 64))
    draw.ellipse([8, 10, 24, 24], fill=(96, 96, 96))
    
    # Cristaux de diamant incrustés
    diamond_spots = [(12, 14), (18, 12), (16, 18), (20, 16)]
    for x, y in diamond_spots:
        # Petit diamant
        points = [(x, y-2), (x-2, y), (x, y+2), (x+2, y)]
        draw.polygon(points, fill=(185, 242, 255))
        draw.polygon([(x, y-2), (x-1, y-1), (x, y), (x+1, y-1)], fill=(220, 250, 255))
    
    ores['diamond_ore'] = diamond_ore
    
    # Charbon amélioré
    coal_ore = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(coal_ore)
    
    # Roche de base
    draw.ellipse([6, 8, 26, 26], fill=(96, 96, 96))
    draw.ellipse([8, 10, 24, 24], fill=(128, 128, 128))
    
    # Veines de charbon
    coal_spots = [(10, 12), (16, 14), (12, 18), (20, 16), (14, 20)]
    for x, y in coal_spots:
        draw.ellipse([x-2, y-2, x+2, y+2], fill=(36, 36, 36))
        draw.ellipse([x-1, y-2, x+1, y-1], fill=(64, 64, 64))  # Reflet
    
    ores['coal_ore'] = coal_ore
    
    return ores

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
    """Génère tous les sprites d'items manquants"""
    pygame.init()
    
    print("🎨 Génération des sprites d'items manquants...")
    
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites")
    
    # Items manquants
    print("🔧 Création des items manquants...")
    missing_items = create_missing_items()
    items_dir = os.path.join(base_dir, "items")
    save_sprites_to_pygame(missing_items, items_dir)
    
    # Minerais
    print("⛏️ Création des minerais...")
    ores = create_mineral_ores()
    tiles_dir = os.path.join(base_dir, "tiles")
    save_sprites_to_pygame(ores, tiles_dir)
    
    print("🎉 Tous les sprites manquants ont été créés!")

if __name__ == "__main__":
    main()
