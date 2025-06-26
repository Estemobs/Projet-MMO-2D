#!/usr/bin/env python3
"""
Script de test pour vérifier l'intégration des nouveaux modules
"""

import sys
import os
import pygame

# Ajouter le répertoire principal au path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_imports():
    """Test des imports des nouveaux modules"""
    print("🧪 Test des imports...")
    
    try:
        from game.sprite_manager import SpriteManager
        print("  ✅ SpriteManager importé")
    except Exception as e:
        print(f"  ❌ Erreur SpriteManager: {e}")
    
    try:
        from game.render_manager import RenderManager
        print("  ✅ RenderManager importé")
    except Exception as e:
        print(f"  ❌ Erreur RenderManager: {e}")
    
    try:
        from game.gameplay_manager import GameplayManager
        print("  ✅ GameplayManager importé")
    except Exception as e:
        print(f"  ❌ Erreur GameplayManager: {e}")
    
    try:
        from game.minimap import MiniMap
        print("  ✅ MiniMap importé")
    except Exception as e:
        print(f"  ❌ Erreur MiniMap: {e}")

def test_sprite_loading():
    """Test du chargement des sprites"""
    print("\n🎨 Test du chargement des sprites...")
    
    pygame.init()
    
    try:
        from game.sprite_manager import get_sprite_manager
        sprite_manager = get_sprite_manager()
        
        # Test de quelques sprites
        grass_sprite = sprite_manager.get_tile_sprite("grass")
        if grass_sprite:
            print("  ✅ Sprite grass chargé")
        else:
            print("  ⚠️ Sprite grass non trouvé")
            
        player_sprite = sprite_manager.get_entity_sprite("player")
        if player_sprite:
            print("  ✅ Sprite player chargé")
        else:
            print("  ⚠️ Sprite player non trouvé")
            
        apple_sprite = sprite_manager.get_item_sprite("apple")
        if apple_sprite:
            print("  ✅ Sprite apple chargé")
        else:
            print("  ⚠️ Sprite apple non trouvé")
            
    except Exception as e:
        print(f"  ❌ Erreur lors du test des sprites: {e}")

def test_assets_structure():
    """Test de la structure des assets"""
    print("\n📁 Test de la structure des assets...")
    
    assets_dir = os.path.join(current_dir, "assets")
    if os.path.exists(assets_dir):
        print("  ✅ Dossier assets trouvé")
        
        sprites_dir = os.path.join(assets_dir, "sprites")
        if os.path.exists(sprites_dir):
            print("  ✅ Dossier sprites trouvé")
            
            for subdir in ["tiles", "items", "entities"]:
                subdir_path = os.path.join(sprites_dir, subdir)
                if os.path.exists(subdir_path):
                    files = [f for f in os.listdir(subdir_path) if f.endswith('.png')]
                    print(f"  ✅ {subdir}/: {len(files)} sprites")
                else:
                    print(f"  ❌ {subdir}/ non trouvé")
        else:
            print("  ❌ Dossier sprites non trouvé")
    else:
        print("  ❌ Dossier assets non trouvé")

def test_game_creation():
    """Test de la création des gestionnaires de jeu"""
    print("\n🎮 Test de la création des gestionnaires...")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        
        from game.render_manager import RenderManager
        from game.gameplay_manager import GameplayManager
        from game.minimap import MiniMap
        
        render_manager = RenderManager(screen)
        gameplay_manager = GameplayManager()
        minimap = MiniMap(200, 200)
        
        print("  ✅ RenderManager créé")
        print("  ✅ GameplayManager créé")
        print("  ✅ MiniMap créé")
        
        # Test d'initialisation d'une partie
        gameplay_manager.init_new_game(800, 600)
        print("  ✅ Nouvelle partie initialisée")
        
        pygame.quit()
        
    except Exception as e:
        print(f"  ❌ Erreur lors de la création: {e}")

if __name__ == "__main__":
    print("🧪 TEST D'INTÉGRATION DES NOUVEAUX MODULES")
    print("=" * 50)
    
    test_imports()
    test_sprite_loading()
    test_assets_structure()
    test_game_creation()
    
    print("\n✅ Tests terminés!")
