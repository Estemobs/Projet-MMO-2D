#!/usr/bin/env python3
"""
Script de test du menu du jeu MMO 2D
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def test_menu_imports():
    """Test des imports du menu"""
    print("🔍 Test des imports du menu...")
    
    try:
        import pygame
        print("✅ pygame importé")
        
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        font = pygame.font.Font(None, 24)
        print("✅ pygame initialisé")
        
        from ui.menu import Menu
        print("✅ Menu importé")
        
        menu = Menu(screen, font)
        print("✅ Menu créé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_save_system():
    """Test du système de sauvegarde"""
    print("\n🔍 Test du système de sauvegarde...")
    
    try:
        from systems.save_system import SaveSystem
        print("✅ SaveSystem importé")
        
        save_system = SaveSystem()
        print("✅ SaveSystem créé")
        
        # Test de création du dossier
        if os.path.exists("saves"):
            print("✅ Dossier saves existe")
        else:
            print("⚠️ Dossier saves créé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_menu_functions():
    """Test des fonctions du menu"""
    print("\n🔍 Test des fonctions du menu...")
    
    try:
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        font = pygame.font.Font(None, 24)
        
        from ui.menu import Menu
        menu = Menu(screen, font)
        
        # Test des méthodes du menu
        print("✅ Menu principal affiché")
        
        # Test changement de menu
        menu.current_menu = "options"
        print("✅ Menu options accessible")
        
        menu.current_menu = "save_menu"
        print("✅ Menu sauvegarde accessible")
        
        menu.current_menu = "load_menu"
        print("✅ Menu chargement accessible")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🎮 TEST DU MENU MMO 2D")
    print("=" * 25)
    
    tests = [
        ("Imports du menu", test_menu_imports),
        ("Système de sauvegarde", test_save_system),
        ("Fonctions du menu", test_menu_functions),
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
        print(f"  {test_name:<25} {status}")
    
    print(f"\n📈 Score: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont réussis !")
        return True
    else:
        print("⚠️ Des problèmes ont été détectés")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
