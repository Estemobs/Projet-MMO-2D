"""
Gestionnaire de sprites pour le jeu MMO 2D
"""

import pygame
import os

class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.sprite_size = 32
        self.item_size = 24
        self.entity_size = 48  # Nouvelle taille pour les entités
        self.load_all_sprites()
    
    def load_all_sprites(self):
        """Charge tous les sprites depuis le dossier assets"""
        sprites_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites")
        
        # Charger les tiles
        tiles_dir = os.path.join(sprites_dir, "tiles")
        if os.path.exists(tiles_dir):
            for filename in os.listdir(tiles_dir):
                if filename.endswith('.png'):
                    name = filename[:-4]  # Enlever .png
                    path = os.path.join(tiles_dir, filename)
                    self.sprites[f"tile_{name}"] = pygame.image.load(path)
        
        # Charger les items
        items_dir = os.path.join(sprites_dir, "items")
        if os.path.exists(items_dir):
            for filename in os.listdir(items_dir):
                if filename.endswith('.png'):
                    name = filename[:-4]  # Enlever .png
                    path = os.path.join(items_dir, filename)
                    self.sprites[f"item_{name}"] = pygame.image.load(path)
        
        # Charger les entités
        entities_dir = os.path.join(sprites_dir, "entities")
        if os.path.exists(entities_dir):
            for filename in os.listdir(entities_dir):
                if filename.endswith('.png'):
                    name = filename[:-4]  # Enlever .png
                    path = os.path.join(entities_dir, filename)
                    self.sprites[f"entity_{name}"] = pygame.image.load(path)
        
        print(f"✅ {len(self.sprites)} sprites chargés")
    
    def get_tile_sprite(self, tile_name):
        """Retourne le sprite d'une tile"""
        key = f"tile_{tile_name}"
        return self.sprites.get(key, None)
    
    def get_item_sprite(self, item_name):
        """Retourne le sprite d'un item"""
        key = f"item_{item_name}"
        return self.sprites.get(key, None)
    
    def get_entity_sprite(self, entity_name):
        """Retourne le sprite d'une entité"""
        key = f"entity_{entity_name}"
        return self.sprites.get(key, None)
    
    def draw_tile(self, screen, tile_name, x, y):
        """Dessine une tile avec son sprite"""
        sprite = self.get_tile_sprite(tile_name)
        if sprite:
            screen.blit(sprite, (x, y))
            return True
        return False
    
    def draw_item(self, screen, item_name, x, y, centered=True):
        """Dessine un item avec son sprite"""
        sprite = self.get_item_sprite(item_name)
        if sprite:
            if centered:
                # Centrer l'item dans la tile
                offset_x = (self.sprite_size - self.item_size) // 2
                offset_y = (self.sprite_size - self.item_size) // 2
                screen.blit(sprite, (x + offset_x, y + offset_y))
            else:
                screen.blit(sprite, (x, y))
            return True
        return False
    
    def draw_entity(self, screen, entity_name, x, y):
        """Dessine une entité avec son sprite"""
        sprite = self.get_entity_sprite(entity_name)
        if sprite:
            screen.blit(sprite, (x, y))
            return True
        return False

# Instance globale
sprite_manager = None

def get_sprite_manager():
    """Retourne l'instance du gestionnaire de sprites"""
    global sprite_manager
    if sprite_manager is None:
        sprite_manager = SpriteManager()
    return sprite_manager
