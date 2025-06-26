#!/usr/bin/env python3
"""
Créer des sprites de personnages plus gros avec animations de marche
"""

import pygame
import os
from PIL import Image, ImageDraw

def create_large_player_sprites():
    """Crée des sprites de joueur plus gros avec différentes poses de marche"""
    sprites = {}
    
    # Couleurs du personnage
    skin_color = (255, 220, 177)
    hair_color = (139, 69, 19)
    shirt_color = (70, 130, 180)
    pants_color = (139, 69, 19)
    shoe_color = (0, 0, 0)
    
    # === SPRITE FACE (pose normale) ===
    player_front = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(player_front)
    
    # Corps (chemise) - plus gros
    draw.ellipse([16, 24, 32, 36], fill=shirt_color)
    
    # Jambes (pantalon)
    draw.rectangle([18, 34, 22, 42], fill=pants_color)
    draw.rectangle([26, 34, 30, 42], fill=pants_color)
    
    # Chaussures
    draw.ellipse([16, 40, 24, 46], fill=shoe_color)
    draw.ellipse([24, 40, 32, 46], fill=shoe_color)
    
    # Tête (peau) - plus grosse
    draw.ellipse([18, 12, 30, 24], fill=skin_color)
    
    # Cheveux
    draw.ellipse([16, 8, 32, 20], fill=hair_color)
    
    # Yeux
    draw.ellipse([21, 16, 23, 18], fill=(0, 0, 0))
    draw.ellipse([25, 16, 27, 18], fill=(0, 0, 0))
    
    # Nez
    draw.ellipse([23, 18, 25, 19], fill=(255, 200, 160))
    
    # Bouche
    draw.ellipse([22, 20, 26, 21], fill=(200, 100, 100))
    
    # Bras
    draw.ellipse([12, 26, 18, 34], fill=shirt_color)
    draw.ellipse([30, 26, 36, 34], fill=shirt_color)
    
    # Mains
    draw.ellipse([10, 32, 16, 38], fill=skin_color)
    draw.ellipse([32, 32, 38, 38], fill=skin_color)
    
    sprites['player'] = player_front
    
    # === ANIMATION DE MARCHE 1 ===
    player_walk1 = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(player_walk1)
    
    # Copier le corps de base
    draw.ellipse([16, 24, 32, 36], fill=shirt_color)
    draw.ellipse([18, 12, 30, 24], fill=skin_color)
    draw.ellipse([16, 8, 32, 20], fill=hair_color)
    draw.ellipse([21, 16, 23, 18], fill=(0, 0, 0))
    draw.ellipse([25, 16, 27, 18], fill=(0, 0, 0))
    draw.ellipse([23, 18, 25, 19], fill=(255, 200, 160))
    draw.ellipse([22, 20, 26, 21], fill=(200, 100, 100))
    
    # Jambes en mouvement (jambe gauche en avant)
    draw.rectangle([16, 34, 20, 42], fill=pants_color)  # Jambe gauche avancée
    draw.rectangle([28, 34, 32, 42], fill=pants_color)  # Jambe droite normale
    
    # Chaussures en mouvement
    draw.ellipse([14, 40, 22, 46], fill=shoe_color)  # Pied gauche en avant
    draw.ellipse([26, 40, 34, 46], fill=shoe_color)  # Pied droit normal
    
    # Bras en mouvement (bras droit en avant)
    draw.ellipse([10, 26, 16, 34], fill=shirt_color)  # Bras gauche en arrière
    draw.ellipse([32, 26, 38, 34], fill=shirt_color)  # Bras droit en avant
    
    # Mains
    draw.ellipse([8, 32, 14, 38], fill=skin_color)
    draw.ellipse([34, 32, 40, 38], fill=skin_color)
    
    sprites['player_walk1'] = player_walk1
    
    # === ANIMATION DE MARCHE 2 ===
    player_walk2 = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(player_walk2)
    
    # Copier le corps de base
    draw.ellipse([16, 24, 32, 36], fill=shirt_color)
    draw.ellipse([18, 12, 30, 24], fill=skin_color)
    draw.ellipse([16, 8, 32, 20], fill=hair_color)
    draw.ellipse([21, 16, 23, 18], fill=(0, 0, 0))
    draw.ellipse([25, 16, 27, 18], fill=(0, 0, 0))
    draw.ellipse([23, 18, 25, 19], fill=(255, 200, 160))
    draw.ellipse([22, 20, 26, 21], fill=(200, 100, 100))
    
    # Jambes en mouvement (jambe droite en avant)
    draw.rectangle([20, 34, 24, 42], fill=pants_color)  # Jambe gauche normale
    draw.rectangle([26, 34, 30, 42], fill=pants_color)  # Jambe droite avancée
    
    # Chaussures en mouvement
    draw.ellipse([18, 40, 26, 46], fill=shoe_color)  # Pied gauche normal
    draw.ellipse([24, 40, 32, 46], fill=shoe_color)  # Pied droit en avant
    
    # Bras en mouvement (bras gauche en avant)
    draw.ellipse([12, 26, 18, 34], fill=shirt_color)  # Bras gauche en avant
    draw.ellipse([30, 26, 36, 34], fill=shirt_color)  # Bras droit en arrière
    
    # Mains
    draw.ellipse([10, 32, 16, 38], fill=skin_color)
    draw.ellipse([32, 32, 38, 38], fill=skin_color)
    
    sprites['player_walk2'] = player_walk2
    
    return sprites

def create_large_enemy_sprites():
    """Crée des sprites d'ennemis plus gros avec animations"""
    sprites = {}
    
    # === ENNEMI DE BASE ===
    enemy = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(enemy)
    
    # Corps principal (slime vert) - plus gros
    body_color = (34, 139, 34)
    darker_green = (20, 100, 20)
    
    # Corps ovale plus gros
    draw.ellipse([12, 18, 36, 42], fill=body_color)
    draw.ellipse([14, 20, 34, 40], fill=darker_green)
    
    # Yeux méchants plus gros
    draw.ellipse([18, 24, 24, 30], fill=(255, 0, 0))
    draw.ellipse([24, 24, 30, 30], fill=(255, 0, 0))
    
    # Pupilles
    draw.ellipse([19, 25, 23, 29], fill=(0, 0, 0))
    draw.ellipse([25, 25, 29, 29], fill=(0, 0, 0))
    
    # Bouche méchante plus grande
    draw.arc([19, 30, 29, 36], 0, 180, fill=(0, 0, 0), width=2)
    
    # Dents plus visibles
    draw.rectangle([21, 32, 23, 35], fill=(255, 255, 255))
    draw.rectangle([25, 32, 27, 35], fill=(255, 255, 255))
    
    # Reflet pour aspect gluant
    draw.ellipse([16, 22, 22, 28], fill=(100, 200, 100, 100))
    
    sprites['enemy'] = enemy
    
    # === ANIMATION ENNEMI 1 ===
    enemy_move1 = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(enemy_move1)
    
    # Corps légèrement déformé (mouvement)
    draw.ellipse([11, 18, 37, 42], fill=body_color)  # Légèrement étiré
    draw.ellipse([13, 20, 35, 40], fill=darker_green)
    
    # Yeux plissés (en mouvement)
    draw.ellipse([17, 24, 23, 30], fill=(255, 0, 0))
    draw.ellipse([25, 24, 31, 30], fill=(255, 0, 0))
    
    # Pupilles décalées
    draw.ellipse([18, 25, 22, 29], fill=(0, 0, 0))
    draw.ellipse([26, 25, 30, 29], fill=(0, 0, 0))
    
    # Bouche ouverte
    draw.ellipse([20, 30, 28, 36], fill=(0, 0, 0))
    
    # Dents visibles
    draw.rectangle([21, 31, 23, 34], fill=(255, 255, 255))
    draw.rectangle([25, 31, 27, 34], fill=(255, 255, 255))
    
    # Reflet déplacé
    draw.ellipse([15, 22, 21, 28], fill=(100, 200, 100, 100))
    
    sprites['enemy_move1'] = enemy_move1
    
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
    """Génère les sprites de personnages plus gros avec animations"""
    pygame.init()
    
    print("🎨 Génération des sprites de personnages plus gros...")
    
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites")
    entities_dir = os.path.join(base_dir, "entities")
    
    # Personnages plus gros
    print("👤 Création des sprites de joueur avec animations...")
    player_sprites = create_large_player_sprites()
    save_sprites_to_pygame(player_sprites, entities_dir)
    
    print("👹 Création des sprites d'ennemis plus gros...")
    enemy_sprites = create_large_enemy_sprites()
    save_sprites_to_pygame(enemy_sprites, entities_dir)
    
    print(f"🎉 Sprites de personnages plus gros créés avec succès!")

if __name__ == "__main__":
    main()
