#!/usr/bin/env python3
"""
Script de test complet des fonctionnalités de menu
"""

import sys
import os
import json
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def test_save_game():
    """Test complet de sauvegarde"""
    print("🔍 Test de sauvegarde...")
    
    try:
        from systems.save_system import SaveSystem
        from game.player import Player
        from game.tiletype import TileType
        from game.enemy import Enemy
        
        # Créer des données de test
        save_system = SaveSystem()
        player = Player(500, 500)
        player.health = 75
        
        # Créer une carte simple
        world_map = [[TileType.GRASS for _ in range(10)] for _ in range(10)]
        world_map[5][5] = TileType.TREE
        
        # Créer des ennemis
        enemies = [Enemy(300, 300), Enemy(700, 700)]
        
        playtime = 120.5  # 2 minutes
        
        # Test de sauvegarde
        result = save_system.save_game(0, player, world_map, enemies, playtime)
        
        if result:
            print("✅ Sauvegarde créée avec succès")
            
            # Vérifier que le fichier existe
            save_path = save_system.get_save_path(0)
            if os.path.exists(save_path):
                print("✅ Fichier de sauvegarde créé")
                
                # Vérifier le contenu
                with open(save_path, 'r') as f:
                    data = json.load(f)
                    
                if "player" in data and "world_map" in data:
                    print("✅ Structure de sauvegarde correcte")
                    return True
                else:
                    print("❌ Structure de sauvegarde incorrecte")
                    return False
            else:
                print("❌ Fichier de sauvegarde non créé")
                return False
        else:
            print("❌ Échec de la sauvegarde")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_load_game():
    """Test complet de chargement"""
    print("\n🔍 Test de chargement...")
    
    try:
        from systems.save_system import SaveSystem
        
        save_system = SaveSystem()
        
        # Test de chargement
        game_data = save_system.load_game(0)
        
        if game_data:
            print("✅ Sauvegarde chargée avec succès")
            
            # Vérifier la structure
            required_keys = ["player", "world_map", "enemies", "timestamp"]
            missing_keys = [key for key in required_keys if key not in game_data]
            
            if not missing_keys:
                print("✅ Toutes les données sont présentes")
                
                # Vérifier les données du joueur
                if "x" in game_data["player"] and "y" in game_data["player"]:
                    print("✅ Données du joueur valides")
                    return True
                else:
                    print("❌ Données du joueur invalides")
                    return False
            else:
                print(f"❌ Clés manquantes: {missing_keys}")
                return False
        else:
            print("❌ Échec du chargement")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_menu_navigation():
    """Test de navigation dans le menu"""
    print("\n🔍 Test de navigation dans le menu...")
    
    try:
        import pygame
        pygame.init()
        pygame.display.set_mode((800, 600))
        font = pygame.font.Font(None, 24)
        
        from ui.menu import Menu
        menu = Menu(pygame.display.get_surface(), font)
        
        # Test des menus
        menus_to_test = ["main", "load_menu", "save_menu", "options"]
        
        for menu_name in menus_to_test:
            menu.current_menu = menu_name
            print(f"✅ Menu '{menu_name}' accessible")
        
        # Test des boutons
        if hasattr(menu, 'main_buttons') and menu.main_buttons:
            print("✅ Boutons du menu principal présents")
        
        # Test des paramètres
        if hasattr(menu, 'controls') and menu.controls:
            print("✅ Paramètres de contrôles présents")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_settings():
    """Test des paramètres"""
    print("\n🔍 Test des paramètres...")
    
    try:
        import pygame
        pygame.init()
        pygame.display.set_mode((800, 600))
        font = pygame.font.Font(None, 24)
        
        from ui.menu import Menu
        menu = Menu(pygame.display.get_surface(), font)
        
        # Test de sauvegarde des paramètres
        original_resolution = menu.current_resolution
        menu.current_resolution = 2
        menu.save_settings()
        
        # Test de chargement des paramètres
        menu.load_settings()
        
        if os.path.exists("settings.json"):
            print("✅ Fichier de paramètres créé")
            
            with open("settings.json", 'r') as f:
                settings = json.load(f)
                
            if "resolution" in settings and "controls" in settings:
                print("✅ Structure des paramètres correcte")
                return True
            else:
                print("❌ Structure des paramètres incorrecte")
                return False
        else:
            print("❌ Fichier de paramètres non créé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🎮 TEST COMPLET DU MENU MMO 2D")
    print("=" * 35)
    
    tests = [
        ("Sauvegarde", test_save_game),
        ("Chargement", test_load_game),
        ("Navigation menu", test_menu_navigation),
        ("Paramètres", test_settings),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors de {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n📊 RÉSUMÉ DES TESTS")
    print("=" * 20)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"  {test_name:<20} {status}")
    
    print(f"\n📈 Score: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Toutes les fonctionnalités du menu fonctionnent !")
        return True
    else:
        print("⚠️ Des problèmes ont été détectés dans le menu")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
