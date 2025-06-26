#!/usr/bin/env python3
"""
Créer des sprites pour les entités (joueur, ennemis)
"""

import pygame
import os
from PIL import Image, ImageDraw

def create_player_sprite():
    """Crée un sprite pour le joueur"""
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Corps (cercle bleu)
    draw.ellipse([8, 8, 24, 24], fill=(0, 100, 255, 255))
    
    # Contour plus foncé
    draw.ellipse([8, 8, 24, 24], outline=(0, 80, 200, 255), width=2)
    
    # Yeux
    draw.ellipse([12, 12, 14, 14], fill=(255, 255, 255, 255))
    draw.ellipse([18, 12, 20, 14], fill=(255, 255, 255, 255))
    draw.ellipse([12, 12, 13, 13], fill=(0, 0, 0, 255))
    draw.ellipse([18, 12, 19, 13], fill=(0, 0, 0, 255))
    
    return img

def create_enemy_sprite():
    """Crée un sprite pour les ennemis"""
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Corps (cercle rouge)
    draw.ellipse([10, 10, 22, 22], fill=(255, 0, 0, 255))
    
    # Contour plus foncé
    draw.ellipse([10, 10, 22, 22], outline=(200, 0, 0, 255), width=2)
    
    # Yeux méchants
    draw.ellipse([13, 13, 15, 15], fill=(255, 255, 0, 255))
    draw.ellipse([17, 13, 19, 15], fill=(255, 255, 0, 255))
    draw.ellipse([13, 13, 14, 14], fill=(0, 0, 0, 255))
    draw.ellipse([17, 13, 18, 14], fill=(0, 0, 0, 255))
    
    # Crocs
    draw.polygon([(14, 17), (16, 19), (18, 17)], fill=(255, 255, 255, 255))
    
    return img

def create_tombstone_sprite():
    """Crée un sprite de pierre tombale"""
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Base de la tombe
    draw.rectangle([12, 20, 20, 28], fill=(100, 100, 100, 255))
    
    # Pierre tombale
    draw.rectangle([10, 8, 22, 22], fill=(150, 150, 150, 255))
    draw.ellipse([10, 8, 22, 16], fill=(150, 150, 150, 255))
    
    # Contour
    draw.rectangle([10, 8, 22, 22], outline=(80, 80, 80, 255), width=1)
    draw.ellipse([10, 8, 22, 16], outline=(80, 80, 80, 255), width=1)
    
    # Croix
    draw.line([16, 12, 16, 18], fill=(80, 80, 80, 255), width=2)
    draw.line([13, 15, 19, 15], fill=(80, 80, 80, 255), width=2)
    
    return img

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
    """Génère tous les sprites d'entités"""
    pygame.init()
    
    print("🎨 Génération des sprites d'entités...")
    
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites")
    entities_dir = os.path.join(base_dir, "entities")
    
    all_sprites = {}
    
    print("Génération du sprite du joueur...")
    all_sprites['player'] = create_player_sprite()
    
    print("Génération du sprite d'ennemi...")
    all_sprites['enemy'] = create_enemy_sprite()
    
    print("Génération du sprite de tombe...")
    all_sprites['tombstone'] = create_tombstone_sprite()
    
    # Sauvegarder
    save_sprites_to_pygame(all_sprites, entities_dir)
    
    print(f"🎉 {len(all_sprites)} sprites d'entités générés avec succès!")
    print(f"📁 Sauvegardés dans: {entities_dir}")

if __name__ == "__main__":
    main()
