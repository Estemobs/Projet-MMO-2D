#!/usr/bin/env python3
"""
Script de test pour vérifier que le jeu fonctionne correctement
"""

import sys
import os
import importlib.util

def test_imports():
    """Test que tous les modules requis peuvent être importés"""
    print("🔍 Test des imports...")
    
    required_modules = [
        'pygame', 'numpy', 'psutil', 'json', 'random', 'math', 'enum', 'os'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Modules manquants: {', '.join(missing_modules)}")
        print("💡 Installez avec: pip install -r requirements.txt")
        return False
    else:
        print("✅ Tous les modules requis sont disponibles")
        return True

def test_game_files():
    """Test que tous les fichiers du jeu sont présents"""
    print("\n📁 Test des fichiers...")
    
    required_files = [
        'main.py', 'menu.py', 'inventory.py', 'launch.py',
        'requirements.txt', 'config.py', 'README.md'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Fichiers manquants: {', '.join(missing_files)}")
        return False
    else:
        print("✅ Tous les fichiers requis sont présents")
        return True

def test_game_initialization():
    """Test que le jeu peut s'initialiser sans erreur"""
    print("\n🎮 Test d'initialisation du jeu...")
    
    try:
        # Import des modules du jeu
        from main import Game, TileType, WorldGenerator
        from menu import Menu
        from inventory import Item, Inventory, InventoryUI
        
        print("  ✅ Imports des modules du jeu réussis")
        
        # Test de création d'objets de base
        pygame_imported = False
        try:
            import pygame
            pygame.init()
            pygame_imported = True
            print("  ✅ Pygame initialisé")
        except:
            print("  ⚠️  Pygame non disponible (normal en mode headless)")
        
        # Test de génération de monde
        world = WorldGenerator.generate_map()
        print("  ✅ Génération de monde réussie")
        
        # Test de création d'items
        item = Item("Test", "resource", "Test item")
        inventory = Inventory(10)
        inventory.add_item(item, 5)
        print("  ✅ Système d'inventaire fonctionnel")
        
        if pygame_imported:
            # Nettoyage pygame
            pygame.quit()
        
        print("✅ Initialisation du jeu réussie")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors de l'initialisation: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 TEST DU JEU MMO 2D")
    print("=" * 50)
    
    # Changer vers le répertoire du script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Imports
    if test_imports():
        tests_passed += 1
    
    # Test 2: Fichiers
    if test_game_files():
        tests_passed += 1
    
    # Test 3: Initialisation
    if test_game_initialization():
        tests_passed += 1
    
    # Résultats
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS DES TESTS")
    print("=" * 50)
    print(f"Tests réussis: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 Tous les tests sont passés!")
        print("✅ Le jeu devrait fonctionner correctement")
        print("\n🚀 Pour lancer le jeu:")
        print("   python main.py")
        print("   ou")
        print("   python launch.py")
        return True
    else:
        print("❌ Certains tests ont échoué")
        print("💡 Vérifiez les erreurs ci-dessus avant de lancer le jeu")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrompus par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        sys.exit(1)
