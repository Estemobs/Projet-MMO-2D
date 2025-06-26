#!/usr/bin/env python3
"""
Test rapide pour vérifier que le jeu peut être importé et initialisé
"""

def test_import():
    """Test d'importation du module game"""
    try:
        from game.core import Game
        print("✅ Import réussi")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_init():
    """Test d'initialisation du jeu"""
    try:
        from game.core import Game
        game = Game()
        print("✅ Initialisation réussie")
        return True
    except Exception as e:
        print(f"❌ Erreur d'initialisation: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Test de la structure modulaire")
    print("=" * 35)
    
    if test_import() and test_init():
        print("\n🎉 Tous les tests sont passés !")
        print("📍 Le jeu peut être lancé avec: python launch.py")
    else:
        print("\n❌ Certains tests ont échoué")
