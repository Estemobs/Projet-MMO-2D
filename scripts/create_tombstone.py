#!/usr/bin/env python3
"""
Script pour générer un sprite de tombe pour les marqueurs de mort
"""

import pygame
import os

def create_tombstone_sprite():
    """Créer un sprite de tombe pour les marqueurs de mort"""
    size = 32
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Fond transparent
    surface.fill((0, 0, 0, 0))
    
    # Base de la tombe (rectangle gris foncé)
    base_rect = pygame.Rect(8, 20, 16, 8)
    pygame.draw.rect(surface, (80, 80, 80), base_rect)
    
    # Pierre tombale (rectangle gris clair)
    stone_rect = pygame.Rect(10, 8, 12, 16)
    pygame.draw.rect(surface, (120, 120, 120), stone_rect)
    
    # Bordure de la pierre tombale
    pygame.draw.rect(surface, (60, 60, 60), stone_rect, 1)
    
    # Croix sur la tombe
    # Ligne verticale
    pygame.draw.line(surface, (200, 200, 200), (16, 10), (16, 18), 2)
    # Ligne horizontale
    pygame.draw.line(surface, (200, 200, 200), (13, 13), (19, 13), 2)
    
    # Petites fleurs à côté (optionnel)
    pygame.draw.circle(surface, (255, 100, 100), (7, 26), 2)  # Fleur rouge
    pygame.draw.circle(surface, (100, 255, 100), (25, 26), 2)  # Fleur verte
    
    return surface

def main():
    pygame.init()
    
    # Créer le sprite de tombe
    tombstone = create_tombstone_sprite()
    
    # Sauvegarder le sprite
    entities_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "entities")
    os.makedirs(entities_dir, exist_ok=True)
    
    tombstone_path = os.path.join(entities_dir, "tombstone.png")
    pygame.image.save(tombstone, tombstone_path)
    
    print(f"✅ Sprite de tombe créé : {tombstone_path}")
    
    pygame.quit()

if __name__ == "__main__":
    main()
