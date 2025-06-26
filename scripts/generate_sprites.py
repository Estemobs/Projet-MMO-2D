#!/usr/bin/env python3
"""
Générateur de sprites simples pour le jeu MMO 2D
Crée des sprites basiques en attendant de vrais assets
"""

import pygame
import os
import sys

# Ajouter le répertoire parent au path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

pygame.init()

def create_tile_sprite(color, size=32, name="tile.png"):
    """Crée un sprite de tile simple"""
    surface = pygame.Surface((size, size))
    surface.fill(color)
    # Ajouter une bordure plus foncée
    darker = tuple(max(0, c - 50) for c in color)
    pygame.draw.rect(surface, darker, (0, 0, size, size), 2)
    return surface

def create_item_sprite(color, size=24, name="item.png", shape="circle"):
    """Crée un sprite d'item simple"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    if shape == "circle":
        pygame.draw.circle(surface, color, (center, center), center - 2)
        pygame.draw.circle(surface, (0, 0, 0), (center, center), center - 2, 2)
    elif shape == "square":
        pygame.draw.rect(surface, color, (2, 2, size-4, size-4))
        pygame.draw.rect(surface, (0, 0, 0), (2, 2, size-4, size-4), 2)
    elif shape == "diamond":
        points = [(center, 2), (size-2, center), (center, size-2), (2, center)]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, (0, 0, 0), points, 2)
    
    return surface

def create_entity_sprite(color, size=32, name="entity.png", shape="circle"):
    """Crée un sprite d'entité simple"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    if shape == "circle":
        pygame.draw.circle(surface, color, (center, center), center - 4)
        pygame.draw.circle(surface, (255, 255, 255), (center, center), center - 4, 2)
        # Yeux
        pygame.draw.circle(surface, (0, 0, 0), (center - 6, center - 4), 2)
        pygame.draw.circle(surface, (0, 0, 0), (center + 6, center - 4), 2)
    elif shape == "square":
        pygame.draw.rect(surface, color, (4, 4, size-8, size-8))
        pygame.draw.rect(surface, (255, 255, 255), (4, 4, size-8, size-8), 2)
    
    return surface

def generate_all_sprites():
    """Génère tous les sprites nécessaires"""
    sprites_dir = os.path.join(parent_dir, "assets", "sprites")
    
    # Tiles
    tiles_dir = os.path.join(sprites_dir, "tiles")
    sprites = {
        "grass.png": create_tile_sprite((34, 139, 34)),  # Vert herbe
        "tree.png": create_tile_sprite((101, 67, 33)),   # Brun arbre
        "stone.png": create_tile_sprite((128, 128, 128)), # Gris pierre
        "iron_ore.png": create_tile_sprite((139, 69, 19)), # Brun fer
        "gold_ore.png": create_tile_sprite((255, 215, 0)), # Or
        "diamond_ore.png": create_tile_sprite((185, 242, 255)), # Bleu diamant
        "coal_ore.png": create_tile_sprite((64, 64, 64)),   # Noir charbon
        "fruit_tree.png": create_tile_sprite((34, 139, 34)), # Vert avec fruits
        "foundation.png": create_tile_sprite((160, 160, 160)), # Gris clair
        "wall.png": create_tile_sprite((139, 69, 19)),      # Brun mur
    }
    
    for name, surface in sprites.items():
        pygame.image.save(surface, os.path.join(tiles_dir, name))
    
    # Items
    items_dir = os.path.join(sprites_dir, "items")
    items = {
        "wood.png": create_item_sprite((101, 67, 33), shape="square"),
        "stone.png": create_item_sprite((128, 128, 128), shape="square"),
        "iron_ore.png": create_item_sprite((139, 69, 19), shape="diamond"),
        "gold_ore.png": create_item_sprite((255, 215, 0), shape="diamond"),
        "diamond.png": create_item_sprite((185, 242, 255), shape="diamond"),
        "coal.png": create_item_sprite((64, 64, 64), shape="square"),
        "apple.png": create_item_sprite((255, 0, 0), shape="circle"),
        "bread.png": create_item_sprite((245, 222, 179), shape="square"),
        "meat.png": create_item_sprite((139, 69, 19), shape="square"),
    }
    
    for name, surface in items.items():
        pygame.image.save(surface, os.path.join(items_dir, name))
    
    # Entities
    entities_dir = os.path.join(sprites_dir, "entities")
    entities = {
        "player.png": create_entity_sprite((0, 100, 255), shape="circle"),
        "enemy.png": create_entity_sprite((255, 0, 0), shape="circle"),
        "death_marker.png": create_entity_sprite((128, 128, 128), shape="square"),
    }
    
    for name, surface in entities.items():
        pygame.image.save(surface, os.path.join(entities_dir, name))
    
    print("✅ Tous les sprites ont été générés!")
    print(f"📁 Dossier: {sprites_dir}")
    print("🎨 Sprites créés:")
    print("  - Tiles: grass, tree, stone, ores, buildings")
    print("  - Items: wood, stone, ores, food")
    print("  - Entities: player, enemy, death marker")

if __name__ == "__main__":
    generate_all_sprites()
