#!/usr/bin/env python3
"""
Générateur de sprites de personnages style Stardew Valley/Pokémon
"""

import pygame
import os
from PIL import Image, ImageDraw

def create_player_sprite():
    """Crée un sprite de joueur style Stardew Valley"""
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Couleurs du personnage
    skin_color = (255, 220, 177)
    hair_color = (139, 69, 19)
    shirt_color = (70, 130, 180)
    pants_color = (139, 69, 19)
    
    # Corps (chemise)
    draw.ellipse([10, 16, 22, 26], fill=shirt_color)
    
    # Jambes (pantalon)
    draw.rectangle([12, 24, 15, 30], fill=pants_color)
    draw.rectangle([17, 24, 20, 30], fill=pants_color)
    
    # Chaussures
    draw.ellipse([11, 28, 16, 32], fill=(0, 0, 0))
    draw.ellipse([16, 28, 21, 32], fill=(0, 0, 0))
    
    # Tête (peau)
    draw.ellipse([12, 8, 20, 16], fill=skin_color)
    
    # Cheveux
    draw.ellipse([11, 6, 21, 14], fill=hair_color)
    
    # Yeux
    draw.ellipse([14, 11, 15, 12], fill=(0, 0, 0))
    draw.ellipse([17, 11, 18, 12], fill=(0, 0, 0))
    
    # Nez
    draw.ellipse([15, 12, 17, 13], fill=(255, 200, 160))
    
    # Bras
    draw.ellipse([8, 18, 12, 24], fill=shirt_color)
    draw.ellipse([20, 18, 24, 24], fill=shirt_color)
    
    # Mains
    draw.ellipse([7, 22, 11, 26], fill=skin_color)
    draw.ellipse([21, 22, 25, 26], fill=skin_color)
    
    return img

def create_enemy_sprite():
    """Crée un sprite d'ennemi style slime/gobelin"""
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Corps principal (slime vert)
    body_color = (34, 139, 34)
    darker_green = (20, 100, 20)
    
    # Corps ovale
    draw.ellipse([8, 12, 24, 28], fill=body_color)
    draw.ellipse([10, 14, 22, 26], fill=darker_green)
    
    # Yeux méchants
    draw.ellipse([12, 16, 16, 20], fill=(255, 0, 0))
    draw.ellipse([16, 16, 20, 20], fill=(255, 0, 0))
    
    # Pupilles
    draw.ellipse([13, 17, 15, 19], fill=(0, 0, 0))
    draw.ellipse([17, 17, 19, 19], fill=(0, 0, 0))
    
    # Bouche méchante
    draw.arc([13, 20, 19, 24], 0, 180, fill=(0, 0, 0))
    
    # Dents
    draw.rectangle([14, 21, 15, 23], fill=(255, 255, 255))
    draw.rectangle([17, 21, 18, 23], fill=(255, 255, 255))
    
    # Reflet pour aspect gluant
    draw.ellipse([11, 15, 15, 19], fill=(100, 200, 100, 100))
    
    return img

def create_beautiful_items():
    """Crée de beaux sprites d'items 2D"""
    items = {}
    
    # === POMME ===
    apple = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(apple)
    
    # Corps de la pomme
    draw.ellipse([10, 12, 22, 26], fill=(220, 20, 60))  # Rouge
    draw.ellipse([12, 14, 20, 24], fill=(255, 69, 0))   # Rouge-orange
    
    # Reflet
    draw.ellipse([13, 15, 17, 19], fill=(255, 182, 193))
    
    # Tige
    draw.rectangle([15, 8, 17, 12], fill=(139, 69, 19))
    
    # Feuille
    draw.ellipse([17, 9, 21, 13], fill=(34, 139, 34))
    
    items['apple'] = apple
    
    # === BOIS ===
    wood = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(wood)
    
    # Bûche
    draw.ellipse([6, 14, 26, 18], fill=(160, 82, 45))
    draw.ellipse([8, 15, 24, 17], fill=(139, 69, 19))
    
    # Anneaux de croissance
    draw.ellipse([24, 14, 26, 18], fill=(101, 67, 33))
    draw.ellipse([25, 15, 26, 17], fill=(160, 82, 45))
    
    items['wood'] = wood
    
    # === PIERRE ===
    stone = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(stone)
    
    # Pierre principale
    points = [(8, 20), (16, 8), (24, 20), (20, 24), (12, 24)]
    draw.polygon(points, fill=(128, 128, 128))
    
    # Reflets
    draw.polygon([(10, 18), (16, 10), (20, 16)], fill=(169, 169, 169))
    
    # Ombres
    draw.polygon([(16, 18), (24, 20), (20, 24), (12, 24)], fill=(105, 105, 105))
    
    items['stone'] = stone
    
    # === MINERAI DE FER ===
    iron = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(iron)
    
    # Roche de base
    draw.ellipse([8, 10, 24, 26], fill=(128, 128, 128))
    
    # Veines de fer
    draw.ellipse([12, 14, 20, 22], fill=(139, 69, 19))
    draw.ellipse([14, 16, 18, 20], fill=(160, 82, 45))
    
    items['iron_ore'] = iron
    
    # === OR ===
    gold = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gold)
    
    # Roche de base
    draw.ellipse([8, 10, 24, 26], fill=(128, 128, 128))
    
    # Veines d'or
    draw.ellipse([12, 14, 20, 22], fill=(255, 215, 0))
    draw.ellipse([14, 16, 18, 20], fill=(255, 255, 0))
    
    # Brillance
    draw.ellipse([13, 15, 17, 19], fill=(255, 255, 255, 150))
    
    items['gold_ore'] = gold
    
    # === BAIES ===
    berry = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(berry)
    
    # Plusieurs baies
    positions = [(12, 14), (18, 12), (15, 18), (20, 16)]
    for x, y in positions:
        draw.ellipse([x-2, y-2, x+2, y+2], fill=(128, 0, 128))
        draw.ellipse([x-1, y-2, x+1, y-1], fill=(255, 20, 147))  # Reflet
    
    # Tige
    draw.line([(16, 8), (16, 12)], fill=(34, 139, 34), width=2)
    
    items['berry'] = berry
    
    # === CHARBON ===
    coal = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(coal)
    
    # Morceaux de charbon
    points = [(10, 12), (22, 10), (24, 22), (8, 20)]
    draw.polygon(points, fill=(36, 36, 36))
    
    # Reflets brillants
    draw.polygon([(12, 14), (18, 12), (16, 16)], fill=(64, 64, 64))
    
    items['coal'] = coal
    
    return items

def create_better_trees():
    """Crée des arbres avec fond transparent"""
    trees = {}
    
    # Chêne
    oak = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(oak)
    
    # Tronc
    draw.rectangle([14, 20, 18, 32], fill=(101, 67, 33))
    
    # Feuillage (plusieurs cercles superposés)
    leaf_color = (34, 139, 34)
    leaf_dark = (20, 100, 20)
    
    # Couronne d'arbre
    draw.ellipse([8, 8, 24, 24], fill=leaf_dark)
    draw.ellipse([10, 10, 22, 22], fill=leaf_color)
    
    # Détails du feuillage
    draw.ellipse([6, 14, 14, 22], fill=leaf_color)
    draw.ellipse([18, 14, 26, 22], fill=leaf_color)
    draw.ellipse([12, 6, 20, 14], fill=leaf_color)
    
    # Reflets sur les feuilles
    draw.ellipse([11, 11, 15, 15], fill=(50, 180, 50))
    draw.ellipse([17, 13, 21, 17], fill=(50, 180, 50))
    
    trees['tree_oak'] = oak
    
    # Pin
    pine = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pine)
    
    # Tronc
    draw.rectangle([14, 22, 18, 32], fill=(101, 67, 33))
    
    # Forme triangulaire du pin
    points = [(16, 4), (6, 24), (26, 24)]
    draw.polygon(points, fill=(20, 100, 20))
    
    # Couches de branches
    points2 = [(16, 8), (10, 20), (22, 20)]
    draw.polygon(points2, fill=(34, 139, 34))
    
    points3 = [(16, 12), (12, 22), (20, 22)]
    draw.polygon(points3, fill=(20, 100, 20))
    
    trees['tree_pine'] = pine
    
    # Arbre à pommes
    apple_tree = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(apple_tree)
    
    # Copier le chêne de base
    draw.rectangle([14, 20, 18, 32], fill=(101, 67, 33))
    draw.ellipse([8, 8, 24, 24], fill=(20, 100, 20))
    draw.ellipse([10, 10, 22, 22], fill=(34, 139, 34))
    
    # Ajouter des pommes
    apple_positions = [(12, 14), (20, 12), (18, 18), (14, 16)]
    for x, y in apple_positions:
        draw.ellipse([x-2, y-2, x+2, y+2], fill=(220, 20, 60))
        draw.ellipse([x-1, y-2, x+1, y-1], fill=(255, 69, 0))  # Reflet
    
    trees['apple_tree'] = apple_tree
    
    return trees

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
    """Génère tous les nouveaux sprites"""
    pygame.init()
    
    print("🎨 Génération des sprites de personnages et items...")
    
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites")
    
    # Sprites de personnages
    print("👤 Création du joueur...")
    player_sprite = create_player_sprite()
    entities_dir = os.path.join(base_dir, "entities")
    save_sprites_to_pygame({"player": player_sprite}, entities_dir)
    
    print("👹 Création des ennemis...")
    enemy_sprite = create_enemy_sprite()
    save_sprites_to_pygame({"enemy": enemy_sprite}, entities_dir)
    
    # Sprites d'items
    print("🍎 Création des items...")
    items = create_beautiful_items()
    items_dir = os.path.join(base_dir, "items")
    save_sprites_to_pygame(items, items_dir)
    
    # Arbres améliorés
    print("🌳 Création des arbres transparents...")
    trees = create_better_trees()
    tiles_dir = os.path.join(base_dir, "tiles")
    save_sprites_to_pygame(trees, tiles_dir)
    
    print("🎉 Tous les sprites ont été créés avec succès!")

if __name__ == "__main__":
    main()
