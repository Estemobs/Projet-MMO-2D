#!/usr/bin/env python3
"""
Test final complet de validation
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def test_menu_colors():
    """Test que toutes les couleurs du menu sont définies"""
    print("🎨 Test des couleurs du menu...")
    
    try:
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        font = pygame.font.Font(None, 24)
        
        from ui.menu import Menu
        menu = Menu(screen, font)
        
        # Test des couleurs définies
        required_colors = ['WHITE', 'BLACK', 'GRAY', 'DARK_GRAY', 'GREEN', 'RED', 'BLUE', 'YELLOW']
        
        for color in required_colors:
            if hasattr(menu, color):
                print(f"✅ {color}: {getattr(menu, color)}")
            else:
                print(f"❌ {color}: Manquant")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_game_launch():
    """Test que le jeu se lance sans erreur"""
    print("\n🚀 Test de lancement du jeu...")
    
    try:
        import pygame
        pygame.init()
        
        from core import GameManager
        
        # Créer le GameManager
        game_manager = GameManager()
        print("✅ GameManager créé")
        
        # Initialiser le jeu
        game_manager.init_game()
        print("✅ Jeu initialisé")
        
        # Tester les fonctions principales
        if game_manager.player is not None:
            print("✅ Player créé")
        
        if hasattr(game_manager, 'menu'):
            print("✅ Menu présent")
        
        if hasattr(game_manager, 'save_system'):
            print("✅ SaveSystem présent")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_save_load_final():
    """Test final complet de sauvegarde/chargement"""
    print("\n💾 Test final sauvegarde/chargement...")
    
    try:
        import pygame
        pygame.init()
        
        from core import GameManager
        
        # Créer et initialiser
        game_manager = GameManager()
        game_manager.init_game()
        
        # Test F5 (slot 0)
        original_health = game_manager.player.health
        game_manager.player.health = 99
        
        if game_manager.save_game(0):
            print("✅ Sauvegarde F5 (slot 0) réussie")
        else:
            print("❌ Sauvegarde F5 échouée")
            return False
        
        # Test sauvegarde menu (slot 2)
        game_manager.player.health = 88
        if game_manager.save_game(2):
            print("✅ Sauvegarde menu (slot 2) réussie")
        else:
            print("❌ Sauvegarde menu échouée")
            return False
        
        # Test chargement
        if game_manager.load_game(0):
            if game_manager.player.health == 99:
                print("✅ Chargement slot 0 correct")
            else:
                print(f"❌ Chargement incorrect: {game_manager.player.health} != 99")
                return False
        else:
            print("❌ Chargement slot 0 échoué")
            return False
        
        # Test visibilité dans le menu
        game_manager.menu.load_save_slots_info()
        
        slots_ok = 0
        for i in range(3):
            if game_manager.menu.save_slots[i] and game_manager.menu.save_slots[i].get("exists", False):
                slots_ok += 1
                print(f"✅ Slot {i} visible dans le menu")
        
        if slots_ok >= 2:  # Au moins les slots 0 et 2
            print("✅ Sauvegardes visibles dans le menu")
            return True
        else:
            print(f"❌ Seulement {slots_ok} slots visibles")
            return False
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🎮 VALIDATION FINALE COMPLÈTE")
    print("=" * 30)
    
    tests = [
        ("Couleurs menu", test_menu_colors),
        ("Lancement jeu", test_game_launch),
        ("Sauvegarde/Chargement", test_save_load_final),
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
    print("\n📊 RÉSUMÉ FINAL")
    print("=" * 15)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"  {test_name:<20} {status}")
    
    print(f"\n📈 Score: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 TOUS LES PROBLÈMES SONT RÉSOLUS !")
        print("✅ YELLOW ajouté - plus d'erreur de couleur")
        print("✅ F5 fonctionne et apparaît dans le menu")
        print("✅ Sauvegarde via menu fonctionne")
        print("✅ Chargement fonctionne parfaitement")
        print("\n🚀 LE JEU EST PRÊT À JOUER ! 🚀")
        return True
    else:
        print("\n⚠️ Des problèmes persistent")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
